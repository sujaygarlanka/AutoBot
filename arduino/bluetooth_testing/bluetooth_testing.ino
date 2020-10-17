char data = 0;                //Variable for storing data

int MAX_SPEED = 220;
int FRONT_SPEED = 5;
int FRONT_1 = 6;
int FRONT_2 = 7;
int BACK_1 = 8;
int BACK_2 = 9;
int BACK_SPEED = 10;
int LED = 13;

void setup()
{
  Serial.begin(9600);         //Sets the data rate in bits per second (baud) for serial data transmission
  pinMode(LED, OUTPUT);
  pinMode(FRONT_SPEED, OUTPUT);
  pinMode(FRONT_1, OUTPUT);
  pinMode(FRONT_2, OUTPUT);
  pinMode(BACK_SPEED, OUTPUT);
  pinMode(BACK_1, OUTPUT);
  pinMode(BACK_2, OUTPUT);
}

void loop()
{
  if (Serial.available() > 0)
  {
    data = Serial.read();      //Read the incoming data and store it into variable data
    Serial.println(data);      //Print Value of data in Serial monitor
    
    
    if (data == 'L')
      left();
      
    else if (data == 'R')
      right();

    else if (data == 'F')
      forward();
      
    else if (data == 'B')
      reverse();

    else if (data == 'T') {
      Serial.println("Test");
      digitalWrite(LED, HIGH);
      delay(2000);
      digitalWrite(LED, LOW);
    }   
  }
}

void left() {
  Serial.println("LEFT");
  digitalWrite(FRONT_SPEED, MAX_SPEED);
  digitalWrite(FRONT_1, LOW);
  digitalWrite(FRONT_2, HIGH);
  delay(2000);
  neutral();
}

void right() {
  Serial.println("RIGHT");
  digitalWrite(FRONT_SPEED, MAX_SPEED);
  digitalWrite(FRONT_1, HIGH);
  digitalWrite(FRONT_2, LOW);
  delay(2000);
  neutral();
}

void forward() {
  Serial.println("FORWARD");
  digitalWrite(BACK_SPEED, MAX_SPEED);
  digitalWrite(BACK_1, HIGH);
  digitalWrite(BACK_2, LOW);
  delay(1000);
  neutral();
}

void reverse() {
  Serial.println("REVERSE");
  digitalWrite(BACK_SPEED, MAX_SPEED);
  digitalWrite(BACK_1, LOW);
  digitalWrite(BACK_2, HIGH);
  delay(1000);
  neutral();
}

void neutral() {
  digitalWrite(FRONT_SPEED, 0);
  digitalWrite(FRONT_1, LOW);
  digitalWrite(FRONT_2, LOW);
  digitalWrite(BACK_SPEED, 0);
  digitalWrite(BACK_1, LOW);
  digitalWrite(BACK_2, LOW);
}
