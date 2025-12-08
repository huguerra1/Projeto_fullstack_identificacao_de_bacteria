from scipy.signal import savgol_filter
import numpy as np

def aplicar_savgol(espectros, window=15, poly=2):
    return savgol_filter(espectros, window_length=window, polyorder=poly, deriv=1, axis=1)