import numpy as np
import matplotlib.pyplot as plt

A = 8
f = 18
f_max = f
N = 144
fs = 144
delta_f = fs / N

freqs = np.arange(N) * (fs / N)
t = np.linspace(0, 1, N, endpoint=False)
t2 = np.linspace(0, 1, 500)
phi = 60


print("Максимальная частота:", f_max)
print("Минимальная частота дискретизации:", 2 * f_max)

x = A * np.sin(2 * np.pi * f * t + phi * np.pi / 180)
x2 = A * np.sin(2 * np.pi * f * t2 + phi * np.pi / 180)

fur = [0] * N  

#X[k] = Σ (n=0..N-1) x[n] * exp(-j * 2π * k * n / N)

for k in range(N):
    for n in range(N):
        fur[k] += x[n] * np.exp(-1j * 2 * np.pi * k * n / N)

absComp = np.abs(fur)

porog = 0.05 * np.max(absComp)


bins = []
for i in range((len(absComp) // 2) + 1):
    if absComp[i] > porog:
        bins.append(i)

f_low = freqs[bins[0]]
f_high = freqs[bins[-1]]
            
spectral_width = max(f_high - f_low, delta_f)

print("Ширина спектра:", spectral_width)

print("Память массива отсчетов(там float64): ", len(x) * 8, "байт")
print("Память массива сектра(массив комплексных чисел complex128):", len(fur) * 16, "байт")


plt.subplot(2, 1, 1)
plt.plot(t, x)
plt.xlabel('Time (t)')
plt.ylabel('Amplitude (V)')

plt.subplot(2, 1, 2)
plt.plot(t2, x2)
plt.xlabel('Time (t)')
plt.ylabel('Amplitude (V)')

plt.tight_layout()
plt.show()  