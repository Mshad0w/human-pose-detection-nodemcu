#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>
#include <RCSwitch.h>

ESP8266WebServer server(8888);
 RCSwitch mySwitch = RCSwitch();
 
const char* ssid = "";
const char* password =  "";
 
void setup() {
 mySwitch.enableTransmit(D1);
    Serial.begin(9600);
    IPAddress ip(192,168,1,20);   
IPAddress gateway(192,168,1,1);   
IPAddress subnet(255,255,255,0); 
IPAddress primaryDNS(8, 8, 8, 8);  
WiFi.config(ip, gateway, subnet,primaryDNS);
    WiFi.begin(ssid, password);  //Connect to the WiFi network
 
    while (WiFi.status() != WL_CONNECTED) {  //Wait for connection
 
        delay(500);
        Serial.println("Waiting to connect...");
 
    }
 
    Serial.print("IP address: ");
    Serial.println(WiFi.localIP());  //Print the local IP
 
    server.on("/body", handleBody); //Associate the handler function to the path
 
    server.begin(); //Start the server
    Serial.println("Server listening");
//  
}
 
void loop() {
 
    server.handleClient(); //Handling of incoming requests
 
}
 
void handleBody() { //Handler for the body path
 
      if (server.hasArg("plain")== false){ //Check if body received
 
            server.send(200, "text/plain", "Body not received");
            return;
 
      }
 
      String message = "Body received:\n";
             message += server.arg("plain");
             message += "\n";
 
      server.send(200, "text/plain", message);
      Serial.println(message);
      if (server.arg("plain")=="hello buddy")
      {
        Serial.println("matched");
        mySwitch.send(0000, 24); //sending rcswitch control signal to remote relay or device
        server.stop();
        delay(20000);
       message="";
       server.begin(); 
      }
      
}
