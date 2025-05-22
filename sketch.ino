const int pwmPin = 9;        // Pin PWM per generare il segnale
const int pinVC = A1;        // Pin analogico per leggere la tensione sul condensatore
const int samples = 300;     // Numero di campioni del ciclo sinusoidale
const int maxPWM = 255;      // Valore massimo PWM
const int delayMicro = 1000; // 1 ms = 1 kHz di campionamento

void setup() {
  pinMode(pwmPin, OUTPUT);
  Serial.begin(115200);
}

void loop() {
  for (int i = 0; i < samples; i++) {
    // Calcolo l’angolo per la sinusoide
    float angle = 2.0 * PI * 3 * i / samples;

    // Calcolo tensione PWM teorica tra 0 e 5V
    float tensionePWM = (sin(angle) + 1.0) / 2.0 * 5.0;

    // Converto in duty cycle PWM (0–255)
    int pwmValue = int((tensionePWM / 5.0) * maxPWM);
    analogWrite(pwmPin, pwmValue);

    // Leggo la tensione reale sul condensatore (VC)
    int rawVC = analogRead(pinVC);
    float VC = rawVC * 5.0 / 1023.0;

    // Stampo solo: ; VC
    Serial.println(VC, 2);  // 3 cifre decimali

    delayMicroseconds(delayMicro);
  }

  analogWrite(pwmPin, 0);  // Spegne il segnale PWM
  while (true);            // Fine esperimento
}
