int command = 0;                //Variable for storing data
int power = 0;

int MAX_POWER = 220;
int FRONT_POWER = 5;
int FRONT_1 = 6;
int FRONT_2 = 7;
int BACK_1 = 8;
int BACK_2 = 9;
int BACK_POWER = 10;
int LED = 13;
int count = 0;
byte serialValues[2];

void setup()
{
  Serial.begin(9600);         //Sets the data rate in bits per second (baud) for serial data transmission
  pinMode(LED, OUTPUT);
  pinMode(FRONT_POWER, OUTPUT);
  pinMode(FRONT_1, OUTPUT);
  pinMode(FRONT_2, OUTPUT);
  pinMode(BACK_POWER, OUTPUT);
  pinMode(BACK_1, OUTPUT);
  pinMode(BACK_2, OUTPUT);
}

void loop()
{
  if (Serial.available() > 0)
  {
    Serial.readBytes(serialValues, 2);
    command = serialValues[0];
    power = serialValues[1];
    if (command == 'L')
      left(power);
      
    else if (command == 'R')
      right(power);

    else if (command == 'F')
      forward(power);
      
    else if (command == 'B')
      reverse(power);

    else if (command == 'C')
      center();

    else if (command == 'S')
      stopCar();
  }
}

void left(int power) {
  Serial.println("LEFT");
  analogWrite(FRONT_POWER, power);
  digitalWrite(FRONT_1, LOW);
  digitalWrite(FRONT_2, HIGH);
}

void right(int power) {
  Serial.println("RIGHT");
  analogWrite(FRONT_POWER, power);
  digitalWrite(FRONT_1, HIGH);
  digitalWrite(FRONT_2, LOW);
}

void forward(int power) {
  Serial.println("FORWARD");
  analogWrite(BACK_POWER, power);
  digitalWrite(BACK_1, HIGH);
  digitalWrite(BACK_2, LOW);
}

void reverse(int power) {
  Serial.println("REVERSE");
  analogWrite(BACK_POWER, power);
  digitalWrite(BACK_1, LOW);
  digitalWrite(BACK_2, HIGH);
}

void center() {
  Serial.println("CENTER");
  digitalWrite(FRONT_POWER, 0);
  digitalWrite(FRONT_1, LOW);
  digitalWrite(FRONT_2, LOW);

}

void stopCar() {
  Serial.println("STOP");
  digitalWrite(BACK_POWER, 0);
  digitalWrite(BACK_1, LOW);
  digitalWrite(BACK_2, LOW);
}
