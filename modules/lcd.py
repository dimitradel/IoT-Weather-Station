# lcd.py — I2C LCD 1602 driver (PCF8574 backpack, 4-bit mode)
from machine import I2C, Pin
import time
 
_LCD_ADDR = 0x27
 
def _i2c():
    return I2C(0, sda=Pin(0), scl=Pin(1), freq=50_000)
 
_bus = None
 
def init():
    global _bus
    _bus = _i2c()
    time.sleep_ms(200)
    for c in (0x33, 0x32, 0x28, 0x0C, 0x06, 0x01):
        _cmd(c); time.sleep_ms(5)
 
def _toggle(b):
    time.sleep_us(500)
    _bus.writeto(_LCD_ADDR, bytes([b | 0x04]))
    time.sleep_us(500)
    _bus.writeto(_LCD_ADDR, bytes([b & ~0x04]))
    time.sleep_us(500)
 
def _send(val, mode):
    bl = 0x08
    for nibble in (val & 0xF0, (val << 4) & 0xF0):
        b = mode | nibble | bl
        _bus.writeto(_LCD_ADDR, bytes([b]))
        _toggle(b)
 
def _cmd(c): _send(c, 0)
 
def puts(text, row):
    _cmd(0x80 if row == 0 else 0xC0)
    for ch in "{:<16}".format(text[:16]):
        _send(ord(ch), 1)
