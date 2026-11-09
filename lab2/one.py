import numpy as np
import matplotlib.pyplot as plt
from scipy.constants import Boltzmann, k


TxPowerBS = 46
TxPowerUE = 24 
AntGainBS = 21
PenetrationM = 15
MIMOGain = 3
IM = 1
FeederLoss = 2
NoiseFigureBS = 2.4
NoiseFigureUE = 6
ThermalNoiseUL = -174 + 10 * np.log10(10e6)

ThermalNoiseDL = -174 + 10 * np.log10(20e6)
ReqiredSINR_UL = 4
ReqiredSINR_DL = 2 # Мощность сигнала / мощность шумов

RxSensBS = NoiseFigureBS + ThermalNoiseUL + ReqiredSINR_UL #чувствительность
RxSensUE = NoiseFigureUE + ThermalNoiseDL + ReqiredSINR_DL

MAPL_UL = (TxPowerUE - FeederLoss + AntGainBS + MIMOGain - IM - PenetrationM) - RxSensBS
MAPL_DL = (TxPowerBS - FeederLoss + AntGainBS + MIMOGain - IM - PenetrationM) - RxSensUE

print(f"MAPL_UL = {MAPL_UL} дБ") #x
print(f"MAPL_DL = {MAPL_DL} дБ")

temps_C = np.array([0, 10, 20, 30, 40, 50])
temps_K = temps_C + 273.15

tDbm = []

for i in temps_K:
    tDbm.append(10*np.log10((i * Boltzmann) / 1e-3))


MAPL_UL_TEMP = []
MAPL_DL_TEMP = []

for i in tDbm:

    RxSensBS = NoiseFigureBS + (i + 10 * np.log10(10e6)) + ReqiredSINR_UL #чувствительность
    RxSensUE = NoiseFigureUE + (i + 10 * np.log10(20e6)) + ReqiredSINR_DL

    MAPL_UL_TEMP.append((TxPowerUE - FeederLoss + AntGainBS + MIMOGain - IM - PenetrationM) - RxSensBS)
    MAPL_DL_TEMP.append((TxPowerBS - FeederLoss + AntGainBS + MIMOGain - IM - PenetrationM) - RxSensUE)



def UMiNLOS(d_m):
    PL = 26 * np.log10(1.8) + 22.7 + 36.7 * np.log10(d_m)
    return PL

def COST231_Hata(d_km):
    h_bs=30
    h_ms=1.5
    f_mhz=1800
    A = 46.3
    B = 33.9
    a_hms = (1.1 * np.log10(f_mhz)) * h_ms - (1.56 * np.log10(f_mhz) - 0.8)
    L_clutter = 0
    s = 44.9 - 6.55 * np.log10(f_mhz)
    PL = A + B * np.log10(f_mhz) - 13.82 * np.log10(h_bs) - a_hms + s * np.log10(d_km) + L_clutter
    return PL


def Walfish_Ikegami_LOS(d_km):
    f_mhz=1800
    PL = 42.6 + 20 * np.log10(f_mhz) + 26 * np.log10(d_km)
    return PL

d_m = np.linspace(1, 2000, 6000)
PL_UMi = UMiNLOS(d_m)

d_km = np.linspace(0.1, 30, 1000)
PL_Hata = COST231_Hata(d_km)
PL_Walfish = Walfish_Ikegami_LOS(d_km)

plt.subplot(1, 2, 1)
plt.plot(d_m, PL_UMi, label='UMiNLOS', color='red')
plt.axhline(MAPL_UL, color='blue', linestyle='--', label='MAPL_UL')
plt.axhline(MAPL_DL, color='green', linestyle='--', label='MAPL_DL')
plt.title('Микросоты (UMiNLOS)')
plt.xlabel('Расстояние, м')
plt.ylabel('Потери, дБ')
plt.legend()
plt.grid()

plt.subplot(1, 2, 2)
plt.plot(d_km, PL_Hata, label='COST 231 Hata', color='purple')
plt.plot(d_km, PL_Walfish, label='Walfish-Ikegami (LOS)', color='orange')
plt.axhline(MAPL_UL, color='blue', linestyle='--', label='MAPL_UL')
plt.axhline(MAPL_DL, color='green', linestyle='--', label='MAPL_DL')
plt.title('Макросоты (Hata, Walfish-Ikegami)')
plt.xlabel('Расстояние, км')
plt.ylabel('Потери, дБ')
plt.legend()
plt.grid()
plt.show()

plt.figure(figsize=(10, 6))

plt.plot(d_km, PL_Hata)

for i in range(len(temps_C)):
    plt.axhline(MAPL_UL_TEMP[i])
    plt.axhline(MAPL_DL_TEMP[i])

plt.title('Модель Hata и сдвиг MAPL от температуры')
plt.xlabel('Расстояние, км')
plt.ylabel('Потери, дБ')
plt.legend()
plt.grid(True)

plt.show()

plt.figure(figsize=(8, 6)) 

plt.plot(temps_C, MAPL_UL_TEMP, color='blue')
plt.plot(temps_C, MAPL_DL_TEMP, color='green')

plt.axhline(MAPL_UL, color='blue')
plt.axhline(MAPL_DL, color='green')

plt.title('Зависимость MAPL от температуры')
plt.xlabel('Температура, °C')
plt.ylabel('MAPL, дБ')
plt.legend()
plt.grid(True)
plt.tight_layout()

plt.show()

print(f"\nРадиус в UL: 0.47 км")
print(f"Радиус в DL: 2.6 км")
print(f"Итоговый радиус: 0.47 км")

S_bs = 1.95 * (0.47 ** 2)
N_bs = np.ceil(100 / S_bs)

print(f"Площадь одной БС: {S_bs:.2f} кв. км")
print(f"Количество БС на 100 кв. км: {int(N_bs)} шт.")      

radius_UL = []
radius_DL = []

for i in range(len(temps_C)):
    r_ul = np.interp(
        MAPL_UL_TEMP[i],
        PL_UMi,
        d_m
    )

    r_dl = np.interp(
        MAPL_DL_TEMP[i],
        PL_UMi,
        d_m
    )

    radius_UL.append(r_ul / 1000)  # перевод в км
    radius_DL.append(r_dl / 1000)

plt.figure(figsize=(9, 6))
plt.plot(temps_C, radius_UL, marker='o', color='blue')
plt.plot(temps_C, radius_DL, marker='o', color='green')
plt.axhline(radius_UL[0], color='blue', linestyle='--')
plt.axhline(radius_DL[0], color='green', linestyle='--')
plt.title('Зависимость радиуса соты от температуры')
plt.xlabel('Температура, °C')
plt.ylabel('Радиус соты, км')
plt.xticks(temps_C)
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

for i in range(len(temps_C)):
    print(
        f"T = {temps_C[i]}°C: "
        f"R_UL = {radius_UL[i]:.3f} км, "
        f"R_DL = {radius_DL[i]:.3f} км"
    )