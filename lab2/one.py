import numpy as np
import matplotlib.pyplot as plt

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
ReqiredSINR_DL = 2

RxSensBS = NoiseFigureBS + ThermalNoiseUL + ReqiredSINR_UL
RxSensUE = NoiseFigureUE + ThermalNoiseDL + ReqiredSINR_DL

MAPL_UL = (TxPowerUE - FeederLoss + AntGainBS + MIMOGain - IM - PenetrationM) - RxSensBS
MAPL_DL = (TxPowerBS - FeederLoss + AntGainBS + MIMOGain - IM - PenetrationM) - RxSensUE

print(f"MAPL_UL = {MAPL_UL} дБ")
print(f"MAPL_DL = {MAPL_DL} дБ")

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

d_m = np.linspace(1, 200, 1000)
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

plt.tight_layout()
plt.show()

print(f"\nРадиус в UL: 0.47 км")
print(f"Радиус в DL: 2.6 км")
print(f"Итоговый радиус: 0.47 км")

S_bs = 1.95 * (0.47 ** 2)
N_bs = np.ceil(100 / S_bs)

print(f"Площадь одной БС: {S_bs:.2f} кв. км")
print(f"Количество БС на 100 кв. км: {int(N_bs)} шт.")      