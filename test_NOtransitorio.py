import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import shift
import serial
import time

#configurazione
porta_seriale = "/dev/tty.usbmodemF412FA9F963C2"
velocita_comunicazione = 115200
arduino = serial.Serial(porta_seriale, velocita_comunicazione)
time.sleep(2)
campioni = 300


data  = []

while len(data) < campioni:
    data.append(arduino.readline().decode('ascii').strip())
    print(data)

v_meas = []
for i in range(len(data)):
    v_meas.append(float(data[i]))
    print(v_meas)

# === Parametri ===
C = 100e-6
length = 300
t = np.arange(length)


# === Segnali ===
v_simulata = 2.5 + 2.5 * np.sin(2 * np.pi * 3 * t / length)                    
i_simulata = 2.5 + 2.5 * np.sin(2 * np.pi * 3 * t / length + np.pi/2)                                        
v_misurata = np.array(v_meas[:length])




from scipy.signal import savgol_filter
v_smooth = savgol_filter(v_misurata, window_length=11, polyorder=2)
i_calcolata = C * np.gradient(v_smooth)
i_calcolata = i_calcolata - np.mean(i_calcolata)


 

# Applichiamo il filtro hard: manteniamo solo i campioni da 50 in poi fino a 300 (max disponibile nel segnale)
start_idx = 50
end_idx = 300  # max length

# Slice dei dati
t_cut = t[start_idx:end_idx]
v_simulata_cut = v_simulata[start_idx:end_idx]
i_simulata_cut = i_simulata[start_idx:end_idx]
v_misurata_cut = v_misurata[start_idx:end_idx]
i_calcolata_cut = i_calcolata[start_idx:end_idx]

# Scala la corrente in µA
i_scaled = i_calcolata_cut * 1e6  # ora in µA

# Normalizza sul range della tensione
v_range = np.max(v_simulata_cut) - np.min(v_simulata_cut)
i_range = np.max(i_scaled) - np.min(i_scaled)
scaling_factor = v_range / i_range
i_scaled_final = i_scaled * scaling_factor

# Plot
fig, ax1 = plt.subplots()

ax1.plot(t_cut, v_simulata_cut, 'r-', label='v_simulata')
ax1.plot(t_cut, i_simulata_cut, 'b-', label='v_simulata sfasata 90°') 
ax1.plot(t_cut, v_misurata_cut, 'g--', label='v_misurata')
ax1.plot(t_cut, i_scaled_final, 'm--', label='i_calcolata scalata')

ax1.set_ylabel('Segnali comparabili (V o corrente scalata)')
ax1.set_xlabel('Tempo [campioni]')
ax1.set_ylim(-5, 8)
plt.legend()
plt.grid()
plt.title('Segnali comparabili su stesso asse (vito ramunno)')
plt.tight_layout()
plt.show()
