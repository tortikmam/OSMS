import numpy as np
import matplotlib.pyplot as plt

A = 8
f = 18
f_max = f
N = 2 * f_max
fs = N / 1
delta_f = fs / N

freqs = np.arange(N) * (fs / N)
t = np.linspace(0, 1, N, endpoint=False)
t2 = np.linspace(0, 1, 500)
phi = 60


print("Максимальная частота:", f_max)
print("Минимальная частота дискретизации:", N)

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


def quantize(signal, bits):

    levels = 2 ** bits

    signal_adc = (signal + A) / (2 * A) * (levels - 1)

    signal_adc = np.round(signal_adc)
    
    signal_adc = np.clip(signal_adc, 0, levels - 1)

    signal_quant = signal_adc / (levels - 1) * (2 * A) - A

    return signal_quant


def quantization_error(original, quantized):

    error = np.abs(original - quantized)

    return np.mean(error)


abs_original = np.abs(fur)


for bits in [3, 4, 5, 6]:

    # Квантованный сигнал
    x_quant = quantize(x, bits)

    # Ошибка квантования
    error = quantization_error(x, x_quant)

    print("Разрядность АЦП:", bits, "бит")
    print("Средняя ошибка квантования:", error)
    print()


for i, bits in enumerate([3, 4, 5, 6]):

    x_quant = quantize(x, bits)

    fur_quant = [0] * N

    for k in range(N):
        for n in range(N):
            fur_quant[k] += x_quant[n] * np.exp(-1j * 2 * np.pi * k * n / N)

    abs_quant = np.abs(fur_quant)

    plt.subplot(4, 1, i + 1)

    plt.stem(freqs[:N // 2 + 1], abs_quant[:N // 2 + 1])

    plt.title("Спектр при разрядности АЦП " + str(bits) + " бит")
    plt.xlabel("Частота (Гц)")
    plt.ylabel("Амплитуда")

plt.tight_layout()
plt.show()