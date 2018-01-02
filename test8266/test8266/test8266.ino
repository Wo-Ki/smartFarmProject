#include <ESP8266WiFi.h>
#include <SimpleDHT.h>

#define relay1 2
const char *ssid     = "360WiFi-48681F";//这里是我的wifi，你使用时修改为你要连接的wifi ssid
const char *password = "dianxin151";//你要连接的wifi密码
const char *host = "192.168.100.3";//修改为手机的的tcpServer服务端的IP地址，即手机在路由器上的ip
WiFiClient client;
const int tcpPort = 8989;//修改为你建立的Server服务端的端口号

#define ID 1001

#define pinDHT22 2
SimpleDHT22 dht22;
float dhtHum = 0.0; //温度
float dhtTem = 0.0;//湿度

void setup()
{ //pinMode(relay1,OUTPUT);
  Serial.begin(115200);
  delay(10);
  Serial.println();
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED)//WiFi.status() ，这个函数是wifi连接状态，返回wifi链接状态
    //这里就不一一赘述它返回的数据了，有兴趣的到ESP8266WiFi.cpp中查看
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
      Serial.print("chickin");
      //      client.print("{\"M\":\"checkin\",\"ID\":\"3114\",\"K\":\"1161b7956\"}\r\n");
      delay(500);
    }

  }
  while (client.available())//，无线读取到的数据转发到到串口
  {
    String s = client.readString();
    Serial.print(s);
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

}

unsigned long lastSend = 0;
void dht11Func() {
  if (lastSend == 0 || millis() - lastSend >= 3000) {
    lastSend = millis();
    //    int chk = DHT11.read(DHTPIN);
    //    Serial.print("Read sensor: ");
    //    switch (chk)
    //    {
    //      case DHTLIB_OK:
    //        Serial.println("OK");
    //        break;
    //      case DHTLIB_ERROR_CHECKSUM:
    //        Serial.println("Checksum error");
    //        break;
    //      case DHTLIB_ERROR_TIMEOUT:
    //        Serial.println("Time out error");
    //        break;
    //      default:
    //        Serial.println("Unknown error");
    //        break;
    //    }
    //    dhtHum = (float)DHT11.humidity;
    //    Serial.print("Humidity(%):");
    //    Serial.println(dhtHum);
    //
    //    dhtTem = (float)DHT11.temperature;
    //    Serial.print("Temperature(℃):");
    //    Serial.println(dhtTem);

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
    String sendData = "{\"ID\":" + String(ID) + ",\"Hum\":" + String(dhtHum) + ",\"Tem\":" + String(dhtTem) + "}\r\n";
    client.print(sendData);

  }
}

