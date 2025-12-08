import spectral.io.envi as envi
import numpy as np
import cv2
import os

def carregar_cubo(caminho_hdr, caminho_raw):
    """Carrega um cubo ENVI e garante que é float32"""
    if not os.path.exists(caminho_hdr) or not os.path.exists(caminho_raw):
        raise FileNotFoundError(f"Arquivos não encontrados: {caminho_hdr}")
    img = envi.open(str(caminho_hdr), str(caminho_raw))
    return img.load().astype(np.float32)

def calibrar_radiometria(amostra, dark, white):
    """
    Aplica a fórmula: (Amostra - Dark) / (White - Dark)
    """
    # Calcula a média espacial do Dark e White para reduzir ruído (opcional, mas recomendado)
    # Se quiser pixel a pixel (correção de campo plano), não use mean. 
    # Aqui usaremos a média para simplificar e evitar erros de dimensão se os cubos tiverem tamanhos levemente diferentes.
    mean_dark = np.mean(dark, axis=(0, 1))
    mean_white = np.mean(white, axis=(0, 1))
    
    numerador = amostra - mean_dark
    denominador = mean_white - mean_dark
    
    # Evita divisão por zero
    denominador[denominador == 0] = 1e-8
    
    refletancia = numerador / denominador
    
    # Corta valores fora de 0-1 (ruído físico)
    return np.clip(refletancia, 0, 1)

def detectar_roi_hough(cubo_refletancia):
    """Detecta o batoque na imagem calibrada"""
    # Gera RGB para detecção (Bandas centrais aproximadas)
    bandas = cubo_refletancia.shape[2]
    rgb_idx = [int(bandas*0.75), int(bandas*0.5), int(bandas*0.25)]
    
    rgb = cubo_refletancia[..., rgb_idx].copy()
    
    # OpenCV precisa de uint8 0-255
    gray = cv2.cvtColor((rgb * 255).astype(np.uint8), cv2.COLOR_RGB2GRAY)
    gray_blurred = cv2.GaussianBlur(gray, (7, 7), 2)
    
    # Hough
    circles = cv2.HoughCircles(
        gray_blurred, cv2.HOUGH_GRADIENT, dp=1.2, minDist=100,
        param1=100, param2=15, minRadius=50, maxRadius=200
    )
    
    if circles is None:
        raise ValueError("Nenhum batoque detectado.")
        
    x, y, r = circles[0][0]
    
    # Cria máscara
    mask = np.zeros(gray.shape, dtype=np.uint8)
    cv2.circle(mask, (int(x), int(y)), int(r), 1, thickness=-1)
    
    return mask, rgb, (int(x), int(y), int(r))