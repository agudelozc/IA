 //Cristian Agudelo Zapata -------//
 //Juan David Zapata------//
 //------------------------
 
 
 int cog;
 int digPin=5; // PIN DIGITAL 5 QUE ME ACEPTA EL PWM
 int vr_num;
// the setup routine runs once when you press reset:
void setup() {
  // initialize serial communication at 115200 bits per second:
  Serial.begin(115200);
}

void loop(){
  while(Serial.read() != 'k'){
  }
  vr_num= analogRead(A1);
  Serial.println(vr_num);
  delay(1000);
  
  while(Serial.read() != 't'){
  }
   cog=Serial.read();
   int duty;
   duty=map(cog,0,1023,0,255);
   
   analogWrite(digPin,duty);
}



