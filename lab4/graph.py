
import numpy as np
import matplotlib.pyplot as plt

gl = "1110000110000111110110101011011"

gl_n = "1011010010101100101010010110100"

gl = np.array([int(bit) for bit in gl])
gl_n = np.array([int(bit) for bit in gl_n])

if len(gl) != len(gl_n):
    print("Последовательности должны иметь одинаковую длину")

N = len(gl)

a = 2 * gl - 1
b = 2 * gl_n - 1
cross_corr = []

for s in range(N):
    shifted = np.roll(b, -s)
    corr = np.sum(a * shifted) / N
    cross_corr.append(corr)

shifts = np.arange(N)

plt.figure()

plt.stem(shifts, cross_corr)
plt.title("Взаимная корреляция gl и gl_n")
plt.xlabel("Сдвиг")
plt.ylabel("Корреляция")
plt.grid(True)

plt.tight_layout()
plt.show()
