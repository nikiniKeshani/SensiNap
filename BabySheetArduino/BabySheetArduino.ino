#define LED 12
#define Buzzer 11

byte signal;

void setup() {
  pinMode(LED, OUTPUT);
  pinMode(Buzzer, OUTPUT);

  Serial.begin(9600);
}

void loop() {
  if (Serial.available()) {
    signal = Serial.read();

    if (signal == 'T') {
      digitalWrite(LED, 1);
      digitalWrite(Buzzer, 1);
      delay(300);
      digitalWrite(LED, 0);
      digitalWrite(Buzzer, 0);
      delay(200);

    } else if (signal == 'F') {
      digitalWrite(LED, 0);
    }
  }
}
