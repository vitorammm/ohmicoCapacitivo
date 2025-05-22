//Questo codice Arduino genera un segnale sinusoidale PWM sul pin 9 e misura la tensione sul condensatore (collegato a quel segnale) tramite il pin analogico A1.

const int pwmPin = 9;        // Pin PWM per generare il segnale
const int pinVC = A1;        // Pin analogico per leggere la tensione sul condensatore
const int campioni = 300;     // Numero di campioni del ciclo sinusoidale
const int maxPWM = 255;      // Valore massimo PWM
const int tempo_campionamento = 1000; // 1 ms di campionamento

void setup() {
  pinMode(pwmPin, OUTPUT);
  Serial.begin(115200);
}

void loop() {
  for (int i = 0; i < campioni; i++) {
    // Calcolo l’angolo per la sinusoide
    float angle = 2.0 * PI * 3 * i / campioni;

    // Converto in duty cycle PWM (0–255)
    int pwmValue = int((tensionePWM / 5.0) * maxPWM);
    analogWrite(pwmPin, pwmValue);

    // Leggo la tensione reale sul condensatore (VC)
    int grezzoVC = analogRead(pinVC);
    float VC = grezzoVC * 5.0 / 1023.0; //conversione valore grezzo tra 0 e 1023

    // Stampo solo: ; VC
    Serial.println(VC, 2);  // 3 cifre decimali

    delayMicroseconds(tempo_campionamento);
  }

  analogWrite(pwmPin, 0);  // Spegne il segnale PWM
  while (true);            // Fine esperimento
}
