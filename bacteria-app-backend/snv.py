import numpy as np

def aplicar_snv(espectros):
    espectros = np.array(espectros, dtype=np.float64)
    media = np.mean(espectros, axis=1, keepdims=True)
    desvio = np.std(espectros, axis=1, keepdims=True)
    desvio[desvio == 0] = 1e-8
    return (espectros - media) / desvio