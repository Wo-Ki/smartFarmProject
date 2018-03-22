#include <ESP8266WiFi.h>
char ssid[]     = "360WiFi-48681F";//这里是我的wifi，你使用时修改为你要连接的wifi ssid
char password[] = "dianxin151";//你要连接的wifi密码
char host[] = "192.168.100.3";//修改为手机的的tcpServer服务端的IP地址，即手机在路由器上的ip
//const char *host = "120.78.164.75";
WiFiClient client;
const int tcpPort = 8989;//修改为你建立的Server服务端的端口号


#define ID 2001



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
    String t = Serial.readStringUntil('\n');
    client.print(t);
    delay(100);
  }
  onChange();

}
unsigned long lastTime = 0;
void onChange() {
  if (millis() - lastTime > 5000) {
    lastTime = millis();
    String s = "{\"M\":\"say\",\"SID\":\"2001\",\"TID\":\"1001\",\"C\":\"I am 2001 ,you are 1001.\"}";
    client.print(s);
    delay(100);
    Serial.println(s);
  }
}

