import ctypes
import numpy as np

dll = ctypes.CDLL("C:\\Users\\skyle\\OneDrive - Montana State University\\Desktop\\dev\\rolling_avg\\target\\x86_64-pc-windows-gnu\\release\\rolling_avg.dll")

rolling_average = dll.rolling_average
rolling_average.argtypes = [
    np.ctypeslib.ndpointer(dtype=np.float64, flags="C_CONTIGUOUS"),
    ctypes.c_size_t,
    ctypes.c_size_t,
    np.ctypeslib.ndpointer(dtype=np.float64, flags="C_CONTIGUOUS")
]

data = np.array([1, 2, 3, 4, 5], dtype=np.float64)
window = 3
out = np.zeros(len(data) - window + 1, dtype=np.float64)

rolling_average(data, len(data), window, out)
print(out)  # [2.0 3.0 4.0]