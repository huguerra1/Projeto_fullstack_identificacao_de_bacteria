import numpy as np
import io
import base64
import matplotlib.pyplot as plt
import leitura
import snv
import savgol

def gerar_grafico_base64(dados, titulo, tipo="linha"):
    plt.figure(figsize=(6, 4))
    if tipo == "imagem":
        plt.imshow(dados)
        plt.axis('off')
    else:
        plt.plot(dados) # Plota espectro médio ou histograma
        plt.grid(True, alpha=0.3)
    
    plt.title(titulo)
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    img_str = base64.b64encode(buf.read()).decode('utf-8')
    plt.close()
    return img_str

def pipeline_completo(paths, options):
    """
    paths: dicionario com caminhos (sample_raw, sample_hdr, dark_raw...)
    options: dicionario com flags (snv, savgol)
    """
    resultados = {}

    # 1. Carregar Cubos
    print("Carregando cubos...")
    cubo_amostra = leitura.carregar_cubo(paths['sample_hdr'], paths['sample_raw'])
    cubo_dark = leitura.carregar_cubo(paths['dark_hdr'], paths['dark_raw'])
    cubo_white = leitura.carregar_cubo(paths['white_hdr'], paths['white_raw'])

    # 2. Calibrar
    print("Calibrando...")
    cubo_calibrado = leitura.calibrar_radiometria(cubo_amostra, cubo_dark, cubo_white)

    # 3. Detectar ROI
    print("Detectando ROI...")
    mask, rgb_preview, (x, y, r) = leitura.detectar_roi_hough(cubo_calibrado)
    
    # Gera imagem preview com círculo
    import cv2
    rgb_uint8 = (rgb_preview * 255).astype(np.uint8)
    img_preview = cv2.cvtColor(rgb_uint8, cv2.COLOR_RGB2BGR) # BGR para OpenCV
    cv2.circle(img_preview, (x, y), r, (0, 255, 0), 3)
    img_preview = cv2.cvtColor(img_preview, cv2.COLOR_BGR2RGB) # Volta pra RGB
    resultados['preview_roi'] = gerar_grafico_base64(img_preview, "ROI Detectada", tipo="imagem")

    # 4. Extrair Pixels (Flatten)
    # Pega apenas os pixels dentro da máscara
    pixels_validos = cubo_calibrado[mask == 1]
    
    # Para visualização, vamos pegar a média espectral (o "perfil" da bactéria)
    espectro_medio_antes = np.mean(pixels_validos, axis=0)
    resultados['grafico_antes'] = gerar_grafico_base64(espectro_medio_antes, "Espectro Médio (Calibrado)")

    # 5. Processamento
    dados_proc = pixels_validos.copy() # (N_pixels, N_bandas)
    
    if options['snv']:
        dados_proc = snv.aplicar_snv(dados_proc)
        
    if options['savgol']:
        dados_proc = savgol.aplicar_savgol(dados_proc)

    espectro_medio_depois = np.mean(dados_proc, axis=0)
    resultados['grafico_depois'] = gerar_grafico_base64(espectro_medio_depois, "Espectro Médio (Processado)")

    return resultados