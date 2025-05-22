import numpy as np  # Libreria per i calcoli
import matplotlib.pyplot as plt  # Libreria per i grafici
import serial  # Per comunicare con Arduino
import time

# === Configurazione connessione con Arduino ===
porta = "/dev/tty.usbmodemF412FA9F963C2"  # Cambia in base al tuo sistema
velocita = 115200
arduino = serial.Serial(porta, velocita)
time.sleep(2)  # Aspetta che Arduino sia pronto

# === Parametri iniziali ===
capacita = 100e-6  # 100 microfarad
numero_campioni = 300
tempo = np.arange(numero_campioni)

# === Lettura dati da Arduino ===
dati_grezzi = []
while len(dati_grezzi) < numero_campioni:
    dati_grezzi.append(arduino.readline().decode('ascii').strip())

tensione_misurata = [float(val) for val in dati_grezzi]

# === Simulazione segnali ideali ===
tensione_simulata =  2.5 + 2.5 * np.sin(2 * np.pi * 3 * tempo / numero_campioni)
corrente_simulata =  2.5 * np.sin(2 * np.pi * 3 * tempo / numero_campioni + np.pi/2)

# === Calcolo corrente reale dal segnale misurato ===
from scipy.signal import savgol_filter
tensione_filtrata = savgol_filter(tensione_misurata, window_length=11, polyorder=2)
corrente_calcolata = capacita * np.gradient(tensione_filtrata)
corrente_calcolata -= np.mean(corrente_calcolata)  # Rimuove offset

# === Selezione porzione utile del segnale ===
inizio = 0
fine = 300
tempo_tagliato = tempo[inizio:fine]
tensione_sim_tagliata = tensione_simulata[inizio:fine]
corrente_sim_tagliata = corrente_simulata[inizio:fine] 
tensione_mis_tagliata = np.array(tensione_misurata)[inizio:fine]
corrente_calc_tagliata = corrente_calcolata[inizio:fine]

# === Scala la corrente per confrontarla visivamente ===
corrente_microA = corrente_calc_tagliata * 1e6
ampiezza_tensione = np.max(tensione_sim_tagliata) - np.min(tensione_sim_tagliata)
ampiezza_corrente = np.max(corrente_microA) - np.min(corrente_microA)
fattore_scala = ampiezza_tensione / ampiezza_corrente
corrente_scalata = corrente_microA * fattore_scala

# === Plot dei segnali ===
plt.figure()
plt.plot(tempo_tagliato, tensione_sim_tagliata, 'r-', label='Tensione Simulata')
#plt.plot(tempo_tagliato, corrente_sim_tagliata, 'b-', label='Corrente Simulata (sfasata)')
plt.plot(tempo_tagliato, tensione_mis_tagliata, 'g--', label='Tensione Misurata da Arduino')
#plt.plot(tempo_tagliato, corrente_scalata, 'm--', label='Corrente Calcolata')

 
#Abbellimenti vari
plt.xlabel('Tempo [campioni]')
plt.ylabel('Ampiezza')
plt.title('Segnali misurati e simulati')
plt.legend()
plt.grid()
plt.ylim(-5, 8)
plt.tight_layout()
plt.show()
