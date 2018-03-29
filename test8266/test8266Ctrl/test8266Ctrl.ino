#include <ESP8266WiFi.h>
#include <ArduinoJson.h>
char ssid[]     = "360WiFi-48681F";//这里是我的wifi，你使用时修改为你要连接的wifi ssid
char password[] = "dianxin151";//你要连接的wifi密码
char host[] = "192.168.100.3";//修改为手机的的tcpServer服务端的IP地址，即手机在路由器上的ip
//const char *host = "120.78.164.75";
WiFiClient client;
const int tcpPort = 8989;//修改为你建立的Server服务端的端口号


#define ID 2001
const String targetID = "1001";


void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  delay(10);
  Serial.println();
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
  // 连上WIFI
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED)//WiFi.status() ，这个函数是wifi连接状态，返回wifi链接状态
  {
    delay(500);
    Serial.print(".");
  }//如果没有连通向串口发送.....

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void loop() {
  // put your main code here, to run repeatedly:
  while (!client.connected())//几个非连接的异常处理
  {
    if (!client.connect(host, tcpPort))
    {
      Serial.print("disconnect");
      //client.stop();
      delay(500);
    } else {
      client.print("{\"M\":\"checkin\",\"ID\":\"" + String(ID) + "\"}\n");
      Serial.println("chickin");
      delay(500);
    }
  }
  while (client.available())//，无线读取到的数据转发到到串口
  {
    String s = client.readStringUntil('\n');  // 接收服务器的消息,eg:"windCtrl_1"
    Serial.println(s);
  }

  while (Serial.available())
  {
    String s = Serial.readStringUntil('*');
    int pos = s.indexOf('_'); // 找到"_"的位置
    if (pos != -1) {
      String msgFirst = s.substring(0, pos); // eg:"wind"
      String msgSecond = s.substring(pos + 1, s.length()); // eg:"1"
      Serial.println(msgFirst);
      Serial.println(msgSecond);
      if (msgFirst == "wind") {
        sendToServer(targetID, "windCtrl", msgSecond);
      }
      else if (msgFirst == "door") {
        sendToServer(targetID, "doorCtrl", msgSecond);
      }
      else if (msgFirst == "light") {
        sendToServer(targetID, "lightCtrl", msgSecond);
      }
      else if (msgFirst == "water1") {
        sendToServer(targetID, "water1Ctrl", msgSecond);
      }
      else if (msgFirst == "water2") {
        sendToServer(targetID, "water2Ctrl", msgSecond);
      }
      else if (msgFirst == "tem") {
        sendToServer(targetID, "temCtrl", msgSecond);
      }
      else {
        Serial.println("No such msgFirst");
      }
    }

  }
  beats(); // 心跳包

}

unsigned long lastTime = 0;
void beats() {
  if (millis() - lastTime > 5000) {
    lastTime = millis();
    String s = "{\"M\":\"b\"}\n";
    client.print(s);
    delay(100);
  }
}

void sendToServer(String targetID, String k, String v) {
  String s = "{\"M\":\"say\",\"SID\":\"" + String(ID) + "\",\"TID\":\"" + targetID + "\",\"K\":\"" + k + "_" + v + "\"}\n";
  client.print(s);
  delay(100);
}

