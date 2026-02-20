#version7.5
#uses midi port 1 (my USB interface)
#diplays the bmp from the midi port
#By Ian Dixon


#!/usr/bin/env python3
import time
import mido
import unicornhathd as uh

# -----------------------------
# Unicorn HAT HD setup
# -----------------------------
uh.rotation(0)
uh.brightness(0.4)
WIDTH, HEIGHT = uh.get_shape()

beat_blip = 0.0

# -----------------------------
# Serpentine mapping helper
# -----------------------------
def set_pixel_mapped(x, y, r, g, b):
    #if y % 2 == 1:
        #x = (WIDTH - 1) - x
    x= (WIDTH -1) -x
    uh.set_pixel(x, y, r, g, b)

# -----------------------------
# MIDI setup
# -----------------------------
ports = mido.get_input_names()

print("Available MIDI inputs:")
for i, p in enumerate(ports):
    print(f"{i}: {p}")

if len(ports) < 2:
    raise RuntimeError("MIDI interface 1 not found.")

midi_in = mido.open_input(ports[1])
print(f"Using MIDI input: {ports[1]}")

# -----------------------------
# BPM calculation
# -----------------------------
CLOCK_TICKS_PER_BEAT = 24
clock_count = 0
last_tick_time = None
bpm_history = []
bpm = 0.0

# -----------------------------
# 5×7 pixel font (clean + readable)
# -----------------------------
FONT_5x7 = {
    "0": [
        "01110",
        "10001",
        "10011",
        "10101",
        "11001",
        "10001",
        "01110"
    ],
    "1": [
        "00100",
        "01100",
        "00100",
        "00100",
        "00100",
        "00100",
        "01110"
    ],
    "2": [
        "01110",
        "10001",
        "00001",
        "00010",
        "00100",
        "01000",
        "11111"
    ],
    "3": [
        "11110",
        "00001",
        "00001",
        "01110",
        "00001",
        "00001",
        "11110"
    ],
    "4": [
        "00010",
        "00110",
        "01010",
        "10010",
        "11111",
        "00010",
        "00010"
    ],
    "5": [
        "11111",
        "10000",
        "11110",
        "00001",
        "00001",
        "10001",
        "01110"
    ],
    "6": [
        "00110",
        "01000",
        "10000",
        "11110",
        "10001",
        "10001",
        "01110"
    ],
    "7": [
        "11111",
        "00001",
        "00010",
        "00100",
        "01000",
        "01000",
        "01000"
    ],
    "8": [
        "01110",
        "10001",
        "10001",
        "01110",
        "10001",
        "10001",
        "01110"
    ],
    "9": [
        "01110",
        "10001",
        "10001",
        "01111",
        "00001",
        "00010",
        "01100"
    ]
}

DIGIT_W = 5
DIGIT_H = 7
DIGIT_SPACING = 1

# -----------------------------
# Digit drawing
# -----------------------------


def draw_digit(digit, x_offset, y_offset, color):
    pattern = FONT_5x7[digit]
    for y, row in enumerate(pattern):
        for x, pixel in enumerate(row):
            if pixel == "1":
                px = x + x_offset
                py = y + y_offset
                if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                    set_pixel_mapped(px, py, *color)

def draw_bpm(value,blip):
    uh.clear()
    
    if blip >0.01:
        intensity=int(255 * blip)
        set_pixel_mapped(0,0,intensity,intensity,0)

    try:
        bpm_int = int(round(value))
    except:
        bpm_int = 0

    bpm_int = max(0, min(999, bpm_int))
    text = str(bpm_int)

    total_width = len(text) * (DIGIT_W + DIGIT_SPACING) - DIGIT_SPACING
    start_x = (WIDTH - total_width) // 2
    start_y = (HEIGHT - DIGIT_H) // 2

    color = (255, 200, 80)

    for i, digit in enumerate(text):
        x_offset = start_x + i * (DIGIT_W + DIGIT_SPACING)
        draw_digit(digit, x_offset, start_y, color)

    uh.show()

# -----------------------------
# Main loop
# -----------------------------
print("Listening for MIDI clock...")

try:
    while True:
        for msg in midi_in.iter_pending():
            if msg.type == 'clock':
                now = time.time()

                if last_tick_time is not None:
                    dt = now - last_tick_time
                    if dt > 0:
                        instant_bpm = 60.0 / (dt * CLOCK_TICKS_PER_BEAT)
                        bpm_history.append(instant_bpm)
                        if len(bpm_history) > 20:
                            bpm_history.pop(0)
                        bpm = sum(bpm_history) / len(bpm_history)

                last_tick_time = now
                clock_count += 1
                beat_blip *=0.85
                draw_bpm(bpm,beat_blip)

                if clock_count >= CLOCK_TICKS_PER_BEAT:
                    beat_blip = 1.0
                    draw_bpm(bpm,beat_blip)
                    #draw_bpm(bpm)
                    clock_count = 0
                    
       
                    

        time.sleep(0.001)

except KeyboardInterrupt:
    uh.clear()
    uh.show()
    print("\nExiting cleanly.")
