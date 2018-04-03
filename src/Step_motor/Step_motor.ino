#include <Stepper.h>
//steps:代表馬達轉完一圈需要多少步數。如果馬達上有標示每步的度數，
//將360除以這個角度，就可以得到所需要的步數(例如：360/3.6=100)。(int)

Stepper stepper(200, 11, 10, 9, 8);
int number;

void setup()
{
  stepper.setSpeed(50);     // 將馬達的速度設定成140RPM 最大  150~160
  Serial.begin(9600); 
  Serial.println("Your choice? "); //Prompt User for Input
}

void loop()
{
  if(Serial.available() > 0){
    number = Serial.read();
    Serial.println(number);
    stepper.step(520);
    delay(8000);
    stepper.step(1040);
    delay(8000);
    stepper.step(520);
    Serial.println("Your choice? "); //Prompt User for Input
  }
}
