#include <ESP8266WiFi.h>
#include <SimpleDHT.h>

#define relay1 2
const char *ssid     = "360WiFi-48681F";//这里是我的wifi，你使用时修改为你要连接的wifi ssid
const char *password = "dianxin151";//你要连接的wifi密码
//const char *host = "192.168.100.3";//修改为手机的的tcpServer服务端的IP地址，即手机在路由器上的ip
const char *host = "120.78.164.75";
WiFiClient client;
const int tcpPort = 8989;//修改为你建立的Server服务端的端口号

#define ID 1001

#define pinDHT22 2
#define pinLightCtrl 0
#define pinWindCtrl 4

SimpleDHT22 dht22;
float dhtHum = 0.0; //温度
float dhtTem = 0.0;//湿度

String temCtrlValue = "off"; // 将温控值保存问全局变量,默认关闭自动温控

void setup()
{ //pinMode(relay1,OUTPUT);
  Serial.begin(115200);
  delay(10);
  Serial.println();
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
  // 初始化引脚
  pinMode(pinLightCtrl, OUTPUT);
  pinMode(pinWindCtrl, OUTPUT);
  digitalWrite(pinLightCtrl, LOW);
  digitalWrite(pinWindCtrl, LOW);
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
  Serial.println(WiFi.localIP());//WiFi.localIP()返回8266获得的ip地址
}


void loop()
{
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
      // 向服务器返回每次操作后的状态值,确保在服务器上显示的状态是正确无误,具体col对应的值参考手册
      sendState(1, "water1Ctrl", "0");
      sendState(2, "water2Ctrl", "0");
      sendState(3, "windCtrl", "0");
      sendState(4, "doorCtrl", "0");
      sendState(5, "lightCrtl", "0");
      sendState(6, "temCrtl", "off");
    }

  }
  while (client.available())//，无线读取到的数据转发到到串口
  {
    String s = client.readString();  // 接收服务器的消息,eg:"windCtrl_1"
    Serial.println(s);
    int pos = s.indexOf('_'); // 找到"_"的位置
    if (pos != -1) {
      String msgFirst = s.substring(0, pos); // eg:"windCtrl"
      String msgSecond = s.substring(pos + 1, s.length()); // eg:"1"
      if (msgFirst == "temCtrl") {
        temCtrlFunc(msgSecond);
      }
      else if (msgFirst == "windCtrl") {
        windCtrlFunc(msgSecond);
      }
      else if (msgFirst == "doorCtrl") {}
      else if (msgFirst == "lightCtrl") {
        lightCtrlFunc(msgSecond);
      }
      else if (msgFirst == "water1Ctrl") {}
      else if (msgFirst == "water2Ctrl") {}
      else {
        Serial.println("No Such Ctrl!!!");
      }
    }
    delay(500);
  }

  if (Serial.available())//串口读取到的转发到wifi，因为串口是一位一位的发送所以在这里缓存完再发送
  {
    size_t counti = Serial.available();
    uint8_t sbuf[counti];
    Serial.readBytes(sbuf, counti);
    client.write(sbuf, counti);
    delay(500);
  }
  dht11Func();
  temAutoCtrlFunc();
}

unsigned long lastSend = 0;
void dht11Func() {
  if (lastSend == 0 || millis() - lastSend >= 3000) {
    lastSend = millis();

    int err = SimpleDHTErrSuccess;
    if ((err = dht22.read2(pinDHT22, &dhtTem, &dhtHum, NULL)) != SimpleDHTErrSuccess) {
      Serial.print("Read DHT22 failed, err=");
      Serial.println(err); delay(2000);
      return;
    }
    Serial.print("Humidity(%):");
    Serial.println(dhtHum);
    Serial.print("Temperature(℃):");
    Serial.println(dhtTem);
    Serial.println("Sending current DHT11 status ...");
    //    String sendData = "{\"ID\":" + String(ID) + ",\"Hum\":" + String(dhtHum) + ",\"Tem\":" + String(dhtTem) + "}\r\n";
    String sendData = "{\"M\":\"update\",\"ID\":\"" + String(ID) + "\",\"temIn\":" + String(dhtTem) + ",\"humIn\":" + String(dhtHum) + "}\n";
    client.print(sendData);

  }
}

unsigned long lastTemCtrl = 0;
void temAutoCtrlFunc() {
  if (temCtrlValue == "off") {

    // 以下是停止调温代码,关闭加热降温设备
    {}
  } else {
    if (millis() - lastTemCtrl >= 3000) {
      lastTemCtrl = millis();
      // 以下开始自动调温代码
      {}
    }

  }
}
void lightCtrlFunc(String value) {

  if (value == "1") {
    digitalWrite(pinLightCtrl, HIGH);

  }
  else if (value == "0") {
    digitalWrite(pinLightCtrl, LOW);
  }
  else {
    Serial.println("lightCtrlFunc Error!!!");
  }
  // 向服务器返回每次操作后的状态值,确保在服务器上显示的状态是正确无误,具体col对应的值参考手册
  sendState(5, "lightCrtl", value);
}

void windCtrlFunc(String value) {
  if (value == "1") {
    digitalWrite(pinWindCtrl, HIGH);

  }
  else if (value == "0") {
    digitalWrite(pinWindCtrl, LOW);
  }
  else {
    Serial.println("WindCtrlFunc Error!!!");
  }
  // 向服务器返回每次操作后的状态值,确保在服务器上显示的状态是正确无误,具体col对应的值参考手册
  sendState(3, "windCtrl", value);
}
void temCtrlFunc(String value) {
  if (value == "off") {
    temCtrlValue = "off";
    sendState(6, "temCtrl", "off");

  } else if (value != "off") { // 当value的值不为off时,说明开始自动调温,将全局变量temCtrlValue设为云端发来的温度值
    temCtrlValue = value;
    sendState(6, "temCtrl", temCtrlValue);  // 首次开启自动调温,temCtrlValue为on,然后才为温度值

  }
}
void sendState(int col, String key, String value) { // col填1,2,3... ,key 填 windCtrl, temCtrl,lightCtrl,value填:0,1,off
  // 向服务器返回每次操作后的状态值,确保在服务器上显示的状态是正确无误,具体col对应的值参考手册
  String sendData = "{\"M\":\"status\",\"ID\":\"" + String(ID) + "\",\"col" + String(col) + "\":\"" + String(key) + "_" + String(value) + "\"}\n";
  client.print(sendData);
  delay(200);
  Serial.println(sendData);
}
