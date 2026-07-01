from machine import Pin

r = None
g = None
b = None

def off():
    r.value(0)  #r.off()
    g.value(0)
    b.value(0)

def on():
    r.value(1)
    g.value(1)
    b.value(1)

def comfort_color(T,H):
    if T > 33 and H > 70:   # Apopniktika
        off()
        r.value(1)
        g.value(1)
        return("Apopn")
    if T < 17:  # Cold
        off()
        b.value(1)
        return "Cold  "
    if T > 35:  # Hot
        off()
        r.value(1)
        return "Hot   "
    if T >= 17 and T<= 35: # Normal
        off()
        g.value(1)
        b.value(1)
        return "Normal"
    
