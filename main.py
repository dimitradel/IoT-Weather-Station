from machine import Pin, PWM
from time import sleep
import dht, lcd, servo, rgb

#Παραμετροποίηση προγράμματος
RED_PIN = 14
GREEN_PIN = 13
BLUE_PIN = 12
DHT_PIN = 15
SERVO_PIN=10

#Timings
MEASURE_S = 20 # 20s - 35s 

comfort_index = ""

rgb.r = Pin(RED_PIN, Pin.OUT)
rgb.g = Pin(GREEN_PIN, Pin.OUT)
rgb.b = Pin(BLUE_PIN, Pin.OUT)
sensor = dht.DHT11(Pin(DHT_PIN))
servo.s = PWM(Pin(SERVO_PIN))
servo.s.freq(50)

lcd.init()

while True:
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
    
    
    #servo.set_angle(0)
    sleep(MEASURE_S)  
