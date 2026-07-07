from machine import Pin, PWM
from time import sleep
import dht, lcd, servo, rgb
from secrets import secrets
import network, json
from mqtt import MQTTClient

#Παραμετροποίηση προγράμματος
RED_PIN = 14
GREEN_PIN = 13
BLUE_PIN = 12
DHT_PIN = 15
SERVO_PIN=10

# ΔΙΚΤΥΩΣΗ - NETWORKING
WIFI_SSID = secrets["WIFI_SSID"]
WIFI_PW = secrets["WIFI_PW"]

MQTT_HOST = "test.mosquitto.org"
MQTT_PORT = 1883
MQTT_CLIENT_ID = "dimitra"
TOPIC_DATA = b"robotonio/dimitra/weather"

#Timings
MEASURE_S = 10  

comfort_index = ""

rgb.r = Pin(RED_PIN, Pin.OUT)
rgb.g = Pin(GREEN_PIN, Pin.OUT)
rgb.b = Pin(BLUE_PIN, Pin.OUT)
sensor = dht.DHT11(Pin(DHT_PIN))
servo.s = PWM(Pin(SERVO_PIN))
servo.s.freq(50)

lcd.init()
lcd.puts("DIMITRA", 0)
lcd.puts("Starting...",1)
sleep(1)

#=====================================
# WIFI Connection
#=====================================
lcd.puts("Connecting WiFi...", 0)
lcd.puts("",1)
print("Connecting to WiFi...")

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(WIFI_SSID, WIFI_PW)

while not wlan.isconnected():
    lcd.puts("Waiting WiFi...", 0)
    lcd.puts("",1)
    print("Waiting for WiFi...")
    sleep(1)

print("WiFi connected! IP:", wlan.ifconfig()[0])
lcd.puts("WiFi Connected! IP:", 0)
lcd.puts(wlan.ifconfig()[0],1)
sleep(1)

#=====================================
# MQTT Connection (Adafruit IO)
#=====================================
lcd.puts("Connecting MQTT...", 0)
lcd.puts("Please Wait...",1)
print("Connecting to Adafruit IO...")

client = MQTTClient(
    client_id = MQTT_CLIENT_ID,
    server = MQTT_HOST,
    port = MQTT_PORT,
    keepalive = 60
    )

client.connect()

print("Connected to Adafruit IO")
print("-------------------------")
lcd.puts("Adafruit IO OK!", 0)
lcd.puts("",1)
sleep(1)

counter = 0

while True:
    counter = counter + 1 #counter += 1
    
    sensor.measure() #Παίρνω τη μέτρηση
    T = sensor.temperature() # Σπάω τη μέτρηση σε θερμοκρασία και
    H = sensor.humidity() # υγρασία
    
    comfort_index = rgb.comfort_color(T,H)
    
    servo.from_temp(T)
    
    lcd.puts("T: {:.0f}C H: {:.0f}%".format(T, H), 0)
    lcd.puts("C.Index: {}".format(comfort_index),1)
        
    print ("Temperature :", T, "C")
    print("Humidity   :", H, "%")
    print("-----------------------")
 
    # Send Data MQTT
    print("Sending data to MQTT...")
    
    json_data = json.dumps({
        "id"     : counter,
        "temp"   : T,
        "hum"    : H,
        "comfort": comfort_index
        })
    
    client.publish(TOPIC_DATA, json_data)
    print("Data sent!")
    print(json_data)
    print("-------------------------")
 
    sleep(MEASURE_S)  
