from machine import PWM, Pin

s = None

def _duty(deg):
    return int(1638 + (deg / 180) * (8192 - 1638))
 
def set_angle(deg):
    s.duty_u16(_duty(max(0, min(180, deg))))

def from_temp(T):
    angle = (T - 10) / (45 - 10) * 180 # mapping
    set_angle(angle)
