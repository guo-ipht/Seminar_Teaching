import numpy as np
from scipy.signal import savgol_filter
import scipy.interpolate as interp
from scipy.interpolate import splrep, splev
from numpy.polynomial.legendre import Legendre
import matplotlib.pyplot as plt

def snip(x, iterations=100, smoothing_window=9, lls=True, return_baseline=False):
    """
    Sensitive Nonlinear Iterative Peak (SNIP) clipping algorithm.

    """

    def snip_single(_x):  # SNIP baseline correction
        
        # BUG: in debug mode savgol_filter causes a ValueError error in python 3.10
        bg = savgol_filter(_x.copy(), smoothing_window, 2) if smoothing_window > 2 else np.asarray(_x.copy())

        bg[bg < 0] = 0
        if lls:                                           # log-log-square_root (LLS) operator
            bg = np.log(np.log(np.sqrt(bg + 1) + 1) + 1)

        for p in range(1, iterations + 1, 1):             # optimized snip loop (about 12 times faster)
            bg[p:-p] = np.minimum(bg[p:-p], (bg[p * 2:] + bg[:-p * 2]) / 2)

        if lls:                                           # back transformation of LLS operator
            bg = (np.exp(np.exp(bg) - 1) - 1) ** 2 - 1

        if return_baseline:
            return bg 
        else:
            return _x - bg         # return for a single spectrum

    
    if isinstance(x[0], (np.ndarray, list)):              
        return np.asarray([snip_single(xi) for xi in x])
    else:
        return snip_single(x)
                              
def do_interpolation(spectra, x_old, x_new):
    if spectra.ndim ==1:
        SPLINE = splrep(x=x_old, y=spectra)
        mat_new = splev(x_new, SPLINE)
    else:
        mat_new = np.zeros((spectra.shape[0], len(x_new)))
        for i in range(mat_new.shape[0]):
            SPLINE = splrep(x=x_old, y=spectra[i,])
            mat_new[i,] = splev(x_new, SPLINE)

    return x_new, mat_new

def norm_spectra(spectra, norm_method='vector'):
    if norm_method == 'vector':
        norm_spec = spectra / np.sqrt((spectra ** 2).sum(1))[:, None]
    elif norm_method == 'l1':
        norm_spec = spectra / np.abs(spectra).sum(1)[:, None]
    elif norm_method == 'max':
        norm_spec = spectra / spectra.max(1)[:, None]
    else:
        raise ValueError("Invalid normalization method...")
    return norm_spec