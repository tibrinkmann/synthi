from gpiozero import MCP3008, Button

# Channels evtl wechseln
pot1 = MCP3008(0)
pot2 = MCP3008(1)

button1 = Button(29)
button2 = Button(31)
button3 = Button(37)

try:
    while True:
        
        print(f"Poti 1 value = " + pot1.value)
        print(f"Poti 2 value = " + pot2.value)
        print("Button 1 Value = " + 

except KeyboardInterrupt:
    print("End")
