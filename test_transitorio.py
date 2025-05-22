import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
from scipy.ndimage import uniform_filter1d, shift
import serial
import time

# === CONFIGURAZIONE:
porta_seriale = "/dev/tty.usbmodemF412FA9F963C2"
baudrate = 115200
campioni = 300
C = 100e-6

# === CONNESSIONE ARDUINO:
arduino = serial.Serial(porta_seriale, baudrate)
time.sleep(2)

# === LETTURA DATI:
data  = []

while len(data) < campioni:
    data.append(arduino.readline().decode('ascii').strip())
    print(data)

v_meas = []
for i in range(len(data)):
    v_meas.append(float(data[i]))
    print(v_meas)

v_misurata = np.array(data)

# === TEMPO ===
t = np.arange(campioni)

# === SEGNALI SIMULATI: 3 PERIODI ===
v_simulata = 2.5 + 2.5 * np.sin(2 * np.pi * 3 * t / campioni)
i_simulata = 2.5 + 2.5 * np.sin(2 * np.pi * 3 * t / campioni + np.pi / 2) #Sfasata di 90 gradi in anticipo

# === FILTRAGGIO + CENTRAGGIO ===
v_smooth = savgol_filter(v_misurata, window_length=5, polyorder=3)
v_centered = v_smooth - np.mean(v_smooth)

# === DERIVATA NUMERICA DI V:
i_calcolata = C * np.gradient(v_centered)

# === SCALATURA corrente ===
i_scaled = i_calcolata * 1e6  # da A a µA
v_range = np.max(v_simulata) - np.min(v_simulata)
i_range = np.max(i_scaled) - np.min(i_scaled)
scaling_factor = v_range / i_range
i_scaled_final = i_scaled * scaling_factor

# === RIMOZIONE OFFSET + SHIFT ===
i_scaled_final -= np.mean(i_scaled_final)
i_scaled_final = shift(i_scaled_final, shift=-3)

# === Grafico:
fig, ax1 = plt.subplots()
ax1.plot(t, v_simulata, 'r-', label='v_simulata')
ax1.plot(t, i_simulata, 'b-', label='v_simulata sfasata 90°')
ax1.plot(t, v_misurata, 'g--', label='v_misurata')
ax1.plot(t, i_scaled_final, 'm--', label='i_calcolata scalata')
ax1.set_ylabel('Segnali comparabili (V o corrente scalata)')
ax1.set_xlabel('Tempo [campioni]')
ax1.set_ylim(-4, 8)
plt.legend()
plt.grid()
plt.title('Segnali completi con transitorio (vito ramunno)')
plt.tight_layout()
plt.show()
