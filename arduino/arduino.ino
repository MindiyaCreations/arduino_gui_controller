/*
  V1.1 | 07/05/2024
  Getting Serial Commands and runnign functions accordingly
*/

bool debug = true;
String command = "";
bool commandProcessed = false;

void run_command(String command);
void setOutput(String command);
void getInput(String command);

void setup() {
  Serial.begin(115200);
}

void loop() {
  while(Serial.available()){
    char a = Serial.read();
    if(a == '|'){
      if(commandProcessed == false){
        command = "";
        commandProcessed = true;
      }
      else{
        run_command(command);
      }
    }else{
      command += a;
    }
  }
}

void run_command(String command){
  char type = command[0];
  command.remove(0,2);
  switch(type){
    case 'i':
      if(debug)
        Serial.println("Set input pin - " + command);
      pinMode(command.toInt(),INPUT);
    break;
    case 'o':
      if(debug)
        Serial.println("Set output pin - " + command);
      pinMode(command.toInt(),OUTPUT);
    break;
    case 's':
      if(debug)
        Serial.println("Set output value - " + command);
      setOutput(command);
    break;
    case 'g':
      if(debug)
        Serial.println("Get input value - " + command);
      getInput(command);
    break;
    default:
      Serial.println("Error Operation - " + type);
    break;
  }
  commandProcessed = false;
} 

void setOutput(String command){
  char type = command[0];
  command.remove(0,2);
  String pinS = "";
  while(command.length()!=0){
    char a = command[0];
    command.remove(0,1);
    if(a == '_')break;
    else{
      pinS += a;
    }
  }
  int value = command.toInt();
  switch(type){
    case 'A':
      if(debug)
        Serial.println("Set " + pinS + " analog value - " + String(value));
      analogWrite(pinS.toInt(),value);
    break;
    case 'D':
      if(debug)
        Serial.println("Set " + pinS + " digital value - " + String(value));
      digitalWrite(pinS.toInt(),value);
    break;
  }
}

void getInput(String command){
  int value;
  char type = command[0];
  command.remove(0,2);
  String pinS = command;
  switch(type){
    case 'A':
      value = analogRead(pinS.toInt());
      if(debug)
        Serial.println("Get " + pinS + " analog value - " + String(value));
      Serial.println("|r_A_"+pinS+"_"+value+"|");
    break;
    case 'D':
      value = digitalRead(pinS.toInt());
      if(debug)
        Serial.println("Get " + pinS + " digital value - " + String(value));
      Serial.println("|r_D_"+pinS+"_"+value+"|");
    break;
  }
}