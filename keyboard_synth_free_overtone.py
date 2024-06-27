import pygame as pg
import numpy as np
import rtmidi
import midiconstants
from midiconstants import NOTE_ON, NOTE_OFF

pg.init()
pg.mixer.init(frequency=44100,buffer=16000, size=-16, channels=1)
font = pg.font.SysFont("Impact", 24)

# Screen dimensions
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

# Margins for axes
MARGIN_X = 50
MARGIN_Y = 50

# Frequency range
FREQ_MIN, FREQ_MAX = 1, 10

screen = pg.display.set_mode((WIDTH, HEIGHT))


# Function to map x position to frequency
def x_to_freq(x):
    return round(float(FREQ_MIN + (FREQ_MAX - FREQ_MIN) * ((x - MARGIN_X) / (WIDTH - 2 * MARGIN_X))), 2)


# List to store points
points = []

# Current point being edited
current_point = {'x': MARGIN_X, 'y': HEIGHT - MARGIN_Y}
selecting_x = True

# Index der aktuell ausgewählten Säule
selected_index = 0

# funktion um die x-koordinaten, also die frequenzen zu bekommen
def get_freqs(points):
    freqs = [x_to_freq(point['x']) for point in points if point['x'] >= 20]
    return freqs

# funktion um die y-koordinaten zu bekommen
def get_amps(points):
    amps = [point['y'] for point in points if point['y'] > 0]
    return amps

amps = get_amps(points=points)

freqs = get_freqs(points=points)

def print_freqs(freqs):
    for i,x in enumerate(freqs):
        print(f"Frequenzy: {x} at index. {i}")

# funktion um y-koordinaten zu printen
def print_amps(amps):
    for i,y in enumerate(amps):
        print(f"amplitude: {y} at index: {i}")
    print("End of Array")

# Function to draw everything
def draw():
    screen.fill(GRAY)
    
    # Draw axes
    pg.draw.line(screen, BLACK, (MARGIN_X, HEIGHT - MARGIN_Y), (WIDTH - MARGIN_X, HEIGHT - MARGIN_Y), 2)
    pg.draw.line(screen, BLACK, (MARGIN_X, MARGIN_Y), (MARGIN_X, HEIGHT - MARGIN_Y), 2)
    
    # Draw all lines
    for point in points:
        if point['y'] > 0:
            pg.draw.line(screen, RED, (point['x'], HEIGHT - MARGIN_Y), (point['x'], HEIGHT - point['y'] - MARGIN_Y), 2)

    # Draw current point
    if selecting_x:
        pg.draw.circle(screen, RED, (current_point['x'], HEIGHT - MARGIN_Y), 5)
        # Display frequency at current x position
        freq_text = font.render(f"Multiplikator: {x_to_freq(current_point['x'])} ", True, BLACK)
        screen.blit(freq_text, (current_point['x'] + 10, HEIGHT - MARGIN_Y - 30))
    else:
        pg.draw.line(screen, RED, (current_point['x'], HEIGHT - MARGIN_Y), (current_point['x'], HEIGHT - current_point['y'] - MARGIN_Y), 2)
        pg.draw.circle(screen, RED, (current_point['x'], HEIGHT - current_point['y'] - MARGIN_Y), 5)
        # Display frequency at current x position
        freq_text = font.render(f"Multiplikator: {x_to_freq(current_point['x'])} ", True, BLACK)
        screen.blit(freq_text, (current_point['x'] + 10, HEIGHT - current_point['y'] - MARGIN_Y - 30))

    pg.display.flip()

# Function to find the nearest point to the mouse click
def find_nearest_point(mouse_pos):
    for point in points:
        if abs(point['x'] - mouse_pos[0]) < 10 and abs(HEIGHT - point['y'] - MARGIN_Y - mouse_pos[1]) < 10:
            return point
    return None

# Funktion, welche die Sinuswelle erzeugt
def synth(frequencies, amplitudes, duration, sampling_rate=44100):
    
    frames = int(duration * sampling_rate)
    t = np.linspace(0, duration, frames, endpoint=False)
    #wave = 0.5 * np.sin(2 * np.pi * frequency * t)
    
    wave = np.zeros_like(t)
    
    # Generiere die Wellenform mit Obertönen
    for i, amplitude in enumerate(amplitudes):
        frequency = frequencies * freqs[i]
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
#notes_file = open(f"/home/synthi/synthi/noteslist.txt")
notes_file = open(r"/home/tim/Desktop/Seminarprojekt/synthi/noteslist.txt")
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

# amp parameter richtig anpassen
#map_sound_to_keys(freq,[d / HEIGHT for d in amps])
map_sound_to_keys(freq=freq, amp=amps)

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

running = True
mod = 1
pg.display.set_caption("Synth - Change range: 0 - = // Play with keys or Midi: " )

keypresses = []
dragging = False

while running:
    draw()
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

        # Obertöne einstellen
        elif event.type == pg.MOUSEBUTTONDOWN:
            if selecting_x:
                selected_point = find_nearest_point(event.pos)
                if selected_point:
                    current_point = selected_point
                    points.remove(selected_point)
                    amps = get_amps(points=points)
                    freqs = get_freqs(points=points)
                selecting_x = False
            else:
                current_point['y'] = HEIGHT - pg.mouse.get_pos()[1] - MARGIN_Y
                points.append(current_point.copy())
                amps = get_amps(points=points)
                freqs = get_freqs(points=points)
                print_amps(amps=amps)
                print_freqs(freqs=freqs)
                current_point = {'x': MARGIN_X, 'y': HEIGHT - MARGIN_Y}
                selecting_x = True
                map_sound_to_keys(freq,[d / HEIGHT for d in amps])
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False

                
    # Handle mouse movement for current point
    if selecting_x:
        mouse_x = pg.mouse.get_pos()[0]
        current_point['x'] = max(MARGIN_X, min(WIDTH - MARGIN_X, mouse_x))
        #print(mouse_x)
    else:
        mouse_y = pg.mouse.get_pos()[1]
        current_point['y'] = max(0, min(HEIGHT - MARGIN_Y, HEIGHT - mouse_y - MARGIN_Y))
    
    #pg.display.update()


pg.mixer.quit()
pg.quit()
