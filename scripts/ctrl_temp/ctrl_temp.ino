void setup() {
  Serial.begin(9600);
}

void loop() {
  if (Serial.available() > 0) {
    // Leer el dato enviado por el puerto serie
    int numeroRecibido = Serial.parseInt();
    Serial.println(numeroRecibido);

    delay(2000); // Esperar 2 segundos antes de la próxima lectura
  }
}