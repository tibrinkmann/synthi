# Projektidee
Synthesizer mit einstellbarer Obertonreihe und Rotationseingabegerät

# Synthesizer
## Bibliotheken
numpy

GUI bzw. Menü:
https://realpython.com/python-gui-tkinter/

oder mit PySimpleGUI:
https://www.pysimplegui.com/

matplot in GUI:
https://pythonprogramming.net/how-to-embed-matplotlib-graph-tkinter-gui/

standard build-in python library: 
https://wiki.python.org/moin/Audio/

Pyo: 
http://ajaxsoundstudio.com/pyodoc/
https://github.com/belangeo/pyo

aiotone:
https://github.com/ambv/aiotone/

pedalboard:
https://github.com/spotify/pedalboard

## Materialien
> [!CAUTION]
> Materialliste beinhaltet keine Pull-Up Widerstände (siehe [Schaltplan](https://github.com/tibrinkmann/synthi/blob/main/Synthi.pdf)), da wir vermuten, dass diese aktuell einen Fehler verursachen!
- 1x Raspy 4B (1GB)
- 1x 3.5" LCD Display mit Touch
- 1x MicroSD Karte (mind. 16GB)
- 1x 2 Kanal 16bit ADC

- 1x Wechselschalter, 3 Positionen
- 3x Knopf
- 1x 100Ω Potentiometer, linear
- 1x 100Ω Potentiometer, logarithmisch

- 2x MIDI DIN Buchse 5-polig
- 1x 6N138 Optokoppler
- 1x 7414N Hex Schmitt-Trigger Inverter
- 1x 1N4148 Diode
- 3x 220Ω Widerstand
- 1x 1kΩ Widerstand
- 1x 470Ω Widerstand
- 1x Platine zum Löten

Und entsprechendes Material zum Löten
## Schaltplan

Hier den entsprechenden [Schaltplan für den Synthi](https://github.com/tibrinkmann/synthi/blob/main/Synthi.pdf) beachten.

## Beispielvideo

(Link folgt)

## Weitere Webseiten
https://medium.com/analytics-vidhya/understanding-oscillators-python-2813ec38781d

https://plainenglish.io/blog/making-a-synth-with-python-oscillators-2cb8e68e9c3b

https://www.physics.rutgers.edu/grad/509/03_Scipy.html

## Beispiele
https://www.youtube.com/watch?v=InGrKBRRCUc&t=364s 

https://www.youtube.com/watch?v=gGRs7a9GpHk
https://github.com/denczo/pyblaster

# Rotationseingabegerät
> [!NOTE]
> Die Entwicklung des REG hat den Prototypenstatus nicht verlassen. Weiter können aktuell keine weiteren Arbeiten durchgeführt werden, da der MPU 9250 defekt ist.
> Somit sind alle Angaben voraussichtlich unfertig und ohne Gewähr!
## Bibliotheken

MPU9250:
MPU9250_WE
https://github.com/wollewald/MPU9250_WE

(vorübergehend) Bluetooth:
BluetoothSerial
https://www.arduino.cc/reference/en/libraries/bluetoothserial/

## Materialien

- 1x LOLIN32 Lite
- 1x MPU 9250
- 1x LED, rot
- 1x LED, blau
- 13x LED, grün
- 2x Knopf
- 1x 3,7V Li-Ion Akku (max. 500mA Ladestrom!)

Und entsprechende Materialien zum Löten.
## Schaltplan

Siehe [REG Schaltplan](https://github.com/tibrinkmann/synthi/blob/main/REG.pdf).

## Beispielvideo

(Link folgt)


