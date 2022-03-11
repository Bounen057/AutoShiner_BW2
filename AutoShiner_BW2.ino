#include <Servo.h>

Servo myservo;
int pos = 0;
int diff = 60;

void setup() {
  Serial.begin(9600);

  pinMode(12, OUTPUT);
  digitalWrite(12, LOW);  //  初期化

  myservo.attach(9);
}

byte var;
void loop() {
  if (Serial.available() > 0) {
    var = Serial.read();
  }
  // デバッグ用メッセージ
  Serial.print("\n");
  Serial.print(var);
  
  switch(var){
    case '0':
      push_move();
      break;
    case '1':
      break;
    case '2':
      push_run();
      break;
    case '3':
      break;
    case '4':
      break;
     
    default:
      break;
  }


}

// 移動ボタン
void push_move() {
  Serial.print("Push Button");
  for (pos = 0; pos <= diff; pos += 1) {
    myservo.write(pos);              
    delay(15);                       
  }
  
  for (pos = diff; pos >= 0; pos -= 1) { 
    myservo.write(pos);              
    delay(15);                       
  }
}

// 逃げるボタン
void push_run(){
  Serial.print("Run: HIGH \n");
  digitalWrite(12, HIGH);
  delay(500);
  Serial.print("Run: LOW \n");
  digitalWrite(12,LOW);
  delay(1000);
}
