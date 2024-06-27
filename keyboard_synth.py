import pygame as pg
import numpy as np
import sys
import subprocess
import rtmidi
import midiconstants
from midiconstants import NOTE_ON, NOTE_OFF

pg.init()
pg.mixer.pre_init(buffer=512)
pg.mixer.init(frequency=44100, size=-16, channels=1)
width, height = 400, 300
#screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
screen = pg.display.set_mode((width, height), pg.FULLSCREEN)
font = pg.font.SysFont("Impact", 24)

screen_adsr = pg.display.set_mode((width, height))


# Farben
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

def exec_adsr():
    subprocess.run([sys.executable, "/home/synthi/synthi/envelope.py"])

# Beispiel-Daten
data = [300, 0, 0, 0, 0, 0, 0, 0, 0, 0]

# Säulenparameter
num_columns = len(data)
column_width = width // num_columns
padding = 10

sliders = [ 0 for _ in range(num_columns)]

# Index der aktuell ausgewählten Säule
selected_index = 0

# Funktion, welche die Sinuswelle erzeugt
def synth(frequencies, amplitudes, duration, sampling_rate=44100):
    
    frames = int(duration * sampling_rate)
    t = np.linspace(0, duration, frames, endpoint=False)
    #wave = 0.5 * np.sin(2 * np.pi * frequency * t)
    
    wave = np.zeros_like(t)
    
    # Generiere die Wellenform mit Obertönen
    for i, amplitude in enumerate(amplitudes):
        frequency = frequencies * (i + 1)
        wave += amplitude * np.sin(2 * np.pi * frequency * t)
        
    # Normalisiere die Welle
    #wave = wave * (2**15 - 1) / np.max(np.abs(wave))

    # amplitude der fertigen wave berechnen und Lautstärke zum schluss anpassen
    amp = (np.max(wave) - np.min(wave)) / 2
    skalar = 1 / amp
    wave = wave * skalar

    sound_array = np.int16(wave * 32767)
    sound_array = np.column_stack((sound_array, sound_array))
    sound = pg.sndarray.make_sound(sound_array)

    return sound


keylist = '123456789qwertyuioasdfghjklzxcvbnm,.'
notes_file = open(f"/home/synthi/synthi/noteslist.txt")
#notes_file = open(r"/home/tim/Desktop/Seminarprojekt/synthi/noteslist.txt")
file_contents = notes_file.read()
notes_file.close()
noteslist = file_contents.splitlines()

keymod = '0-='
notes = {} # dict to store samples
freq = 16.3516 # start frequency
posx, posy = 25, 25 #start position

# funktion. die die Frequenz auf die Tasten linked
def map_sound_to_keys(freq,amp):
    # Map sound to keys
    for i in range(len(noteslist)):
        mod = int(i/36)
        key = keylist[i-mod*36]+str(mod)
        sample = synth(frequencies=freq, amplitudes=amp, duration=1/freq)
        notes[key] = [sample, noteslist[i], freq, (posx, posy)]
        notes[key][0].set_volume(0.33)
        freq = freq * 2 ** (1/12)

map_sound_to_keys(freq,[d / height for d in data])

#Midi-Setup
midi_in = rtmidi.MidiIn()
available_ports = midi_in.get_ports()
print(available_ports)
if len(available_ports) > 1:
    midi_in.open_port(1)
    print(f"Opened Midi port: {available_ports[1]}")
    print("open midi channel")
else:
    #midi_in.open_virtual_port("My Virtual Port")
    #print("Opened virtual port")
    print("No Midi device detected")

# Midi to key mapping
midi_note_to_key = {}
midi_start_note = 60
for i in range(len(keylist)):
    if midi_start_note + i <= 127:
        midi_note_to_key[midi_start_note + i] = keylist[i]

# Midi-callback funktion. Wird ausgeführt wenn Midi-Input erhalten wird
def midi_callback(message, data=None):
    global mod
    message, deltatime = message
    status, note, velocity = message[0], message[1], message[2]

    print(f"Received Midi - Status: {status}, Note: {note}, Velocity: {velocity}")

    if status == NOTE_ON and velocity > 0:
        key = midi_note_to_key.get(note)
        print(key)
        if key in keymod:
            mod = keymod.index(str(event.unicode))
        elif key in keylist:
            key = key+str(mod)
            notes[key][0].play(-1)
            keypresses.append([1, notes[key][1], pg.time.get_ticks()])
    elif status == NOTE_OFF or (status == NOTE_ON and velocity == 0):
        key = midi_note_to_key.get(note)
        print(key)
        if key in keymod:
            mod = keymod.index(str(event.unicode))
        elif key in keylist:
            key = key+str(mod)
            notes[key][0].fadeout(200)
            keypresses.append([0, notes[key][1], pg.time.get_ticks()])

midi_in.set_callback(midi_callback)

running = 1
mod = 1
pg.display.set_caption("Synth - Change range: 0 - = // Play with keys or Midi: " )

keypresses = []
dragging = False

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
            running = False

                
        if event.type == pg.KEYDOWN:
            key = str(event.unicode)
            if key in keymod:
                mod = keymod.index(str(event.unicode))
            elif key in keylist:
                key = key+str(mod)
                
                notes[key][0].play(-1)
                keypresses.append([1, notes[key][1], pg.time.get_ticks()])
                #screen.blit(font.render(notes[key][1], 0, (255,255,255)), notes[key][3])
        if event.type == pg.KEYUP and str(event.unicode) != '' and str(event.unicode) in keylist:
            key = str(event.unicode)+str(mod)
            notes[key][0].fadeout(200)
            keypresses.append([0, notes[key][1], pg.time.get_ticks()])
            #screen.blit(font.render(notes[key][1], 0, notes[key][4]), notes[key][3])

        # Säulenhöhe per Maus ändern       
        elif event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:  # Linke Maustaste
                mouse_x, mouse_y = event.pos
                for i in range(num_columns):
                    if i * column_width <= mouse_x < (i + 1) * column_width:
                        selected_index = i
                        dragging = True
                        break
        elif event.type == pg.MOUSEBUTTONUP:
            if event.button == 1:  # Linke Maustaste
                dragging = False
                map_sound_to_keys(freq,[d / height for d in data])
        elif event.type == pg.MOUSEMOTION:
            if dragging and selected_index is not None:
                mouse_x, mouse_y = event.pos
                data[selected_index] = max(0, height - mouse_y)

        elif event.type == pg.KEYDOWN and event.key == pg.K_PLUS:
            exec_adsr()

    # Bildschirm mit Weiß füllen
    screen.fill(WHITE)
    
    # Säulen zeichnen und beschriften
    for i, value in enumerate(data):
        column_height = value
        color = RED if i == selected_index else BLUE
        pg.draw.rect(screen, color, (i * column_width + padding, height - column_height - 30, column_width - 2 * padding, column_height))

        # Beschriftung unten zeichnen
        label = font.render(str(i + 1), True, BLACK)
        screen.blit(label, (i * column_width + padding + (column_width - 2 * padding) // 2 - label.get_width() // 2, height - 30))

    
    pg.display.update()


pg.mixer.quit()
pg.quit()
