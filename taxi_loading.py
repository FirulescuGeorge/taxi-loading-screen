import tkinter as tk
from tkinter import ttk
import math
import random


# ============================================================
# TAXI LOADING SCREEN - V5 FINAL
# ============================================================


# ------------------------------------------------------------
# SETARI GENERALE
# ------------------------------------------------------------

WINDOW_WIDTH = 900
WINDOW_HEIGHT = 600

CANVAS_WIDTH = 820
CANVAS_HEIGHT = 360

BG = "#0d1117"
SKY = "#141923"

ROAD = "#292d35"
SIDEWALK = "#5d6470"

YELLOW = "#f6c42f"
DARK_YELLOW = "#b38b00"

WHITE = "#ffffff"
WINDOW_BLUE = "#72b9e6"


# ------------------------------------------------------------
# FEREASTRA
# ------------------------------------------------------------

root = tk.Tk()

root.title("Taxi Loading Screen")

root.geometry(
    f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}"
)

root.resizable(
    False,
    False
)

root.configure(
    bg=BG
)


# ------------------------------------------------------------
# TITLU
# ------------------------------------------------------------

title_label = tk.Label(
    root,
    text="YOUR TAXI IS COMING",
    font=("Arial", 24, "bold"),
    fg=WHITE,
    bg=BG
)

title_label.pack(
    pady=(25, 10)
)


# ------------------------------------------------------------
# CANVAS
# ------------------------------------------------------------

canvas = tk.Canvas(
    root,
    width=CANVAS_WIDTH,
    height=CANVAS_HEIGHT,
    bg=SKY,
    highlightthickness=0
)

canvas.pack()


# ------------------------------------------------------------
# STATUS
# ------------------------------------------------------------

status_label = tk.Label(
    root,
    text="Calling your taxi...",
    font=("Arial", 13),
    fg="#dddddd",
    bg=BG
)

status_label.pack(
    pady=(15, 5)
)


# ------------------------------------------------------------
# PROGRESS BAR
# ------------------------------------------------------------

style = ttk.Style()

style.theme_use("clam")

style.configure(
    "Taxi.Horizontal.TProgressbar",
    troughcolor="#292d35",
    background=YELLOW,
    bordercolor="#292d35",
    lightcolor=YELLOW,
    darkcolor=YELLOW
)

progress = ttk.Progressbar(
    root,
    orient="horizontal",
    length=650,
    mode="determinate",
    maximum=100,
    style="Taxi.Horizontal.TProgressbar"
)

progress.pack()


percent_label = tk.Label(
    root,
    text="0%",
    font=("Arial", 13, "bold"),
    fg=YELLOW,
    bg=BG
)

percent_label.pack(
    pady=10
)


# ============================================================
# VARIABILE
# ============================================================

loading = 0

stage = "calling"

taxi_x = -190
taxi_y = 245

TAXI_STOP_X = 75

person_x = 270

person_walk_distance = 0

wave_direction = 1

suspension_angle = 0
last_suspension = 0

wheel_angle = 0

smoke_particles = []

city_groups = []

road_lines = []

person_parts = []

taxi_parts = []

wheel_spokes = []

door = None

taxi_body = None

person_arm_wave = None

enter_step = 0


# ============================================================
# FUNCTII GENERALE
# ============================================================

def update_loading():

    progress["value"] = loading

    percent_label.config(
        text=f"{loading}%"
    )


def move_items(items, dx, dy=0):

    for item in items:

        canvas.move(
            item,
            dx,
            dy
        )


def hide_items(items):

    for item in items:

        canvas.itemconfigure(
            item,
            state="hidden"
        )


# ============================================================
# CER
# ============================================================

def draw_sky():

    canvas.create_rectangle(
        0,
        0,
        CANVAS_WIDTH,
        240,
        fill=SKY,
        outline=""
    )

    # Luna

    canvas.create_oval(
        680,
        30,
        750,
        100,
        fill="#fff4c2",
        outline=""
    )

    canvas.create_oval(
        706,
        20,
        760,
        90,
        fill=SKY,
        outline=""
    )

    # Stele

    stars = [
        (65, 40),
        (120, 78),
        (180, 35),
        (245, 60),
        (320, 30),
        (390, 75),
        (455, 42),
        (520, 82),
        (590, 35),
        (640, 70),
        (780, 55)
    ]

    for x, y in stars:

        canvas.create_oval(
            x,
            y,
            x + 3,
            y + 3,
            fill=WHITE,
            outline=""
        )


# ============================================================
# ORAS
# ============================================================

def create_building(x, width, height):

    parts = []

    bottom = 240
    top = bottom - height

    building = canvas.create_rectangle(
        x,
        top,
        x + width,
        bottom,
        fill="#242a35",
        outline=""
    )

    parts.append(
        building
    )

    window_x = x + 15

    while window_x < x + width - 12:

        window_y = top + 20

        while window_y < bottom - 18:

            window = canvas.create_rectangle(
                window_x,
                window_y,
                window_x + 9,
                window_y + 12,
                fill="#f5d15f",
                outline=""
            )

            parts.append(
                window
            )

            window_y += 29

        window_x += 25

    city_groups.append(
        parts
    )


def draw_city():

    generator = random.Random(10)

    x = 0

    while x < 1100:

        width = generator.randint(
            70,
            100
        )

        height = generator.randint(
            90,
            180
        )

        create_building(
            x,
            width,
            height
        )

        x += width + 10


# ============================================================
# TROTUAR SI DRUM
# ============================================================

def draw_road():

    canvas.create_rectangle(
        0,
        240,
        CANVAS_WIDTH,
        280,
        fill=SIDEWALK,
        outline=""
    )

    canvas.create_rectangle(
        0,
        280,
        CANVAS_WIDTH,
        CANVAS_HEIGHT,
        fill=ROAD,
        outline=""
    )

    for x in range(
        0,
        1000,
        120
    ):

        line = canvas.create_rectangle(
            x,
            320,
            x + 60,
            325,
            fill=WHITE,
            outline=""
        )

        road_lines.append(
            line
        )


# ============================================================
# PERSONAJ
# ============================================================

def draw_person():

    global person_parts
    global person_arm_wave

    # CAP

    head = canvas.create_oval(
        person_x - 10,
        181,
        person_x + 10,
        201,
        fill="#d9a36c",
        outline=""
    )

    # PAR

    hair = canvas.create_arc(
        person_x - 10,
        179,
        person_x + 10,
        197,
        start=0,
        extent=180,
        fill="#252525",
        outline="#252525"
    )

    # TRICOU / JACHETA

    torso = canvas.create_polygon(
        person_x - 11,
        204,
        person_x + 11,
        204,
        person_x + 9,
        241,
        person_x - 9,
        241,
        fill="#e7e9ed",
        outline=""
    )

    # PANTALON STANG

    leg_left = canvas.create_line(
        person_x - 5,
        240,
        person_x - 10,
        269,
        fill="#334b72",
        width=6
    )

    # PANTALON DREPT

    leg_right = canvas.create_line(
        person_x + 5,
        240,
        person_x + 12,
        269,
        fill="#334b72",
        width=6
    )

    # PANTOF STANG

    shoe_left = canvas.create_line(
        person_x - 10,
        269,
        person_x - 17,
        269,
        fill="#111111",
        width=5
    )

    # PANTOF DREPT

    shoe_right = canvas.create_line(
        person_x + 12,
        269,
        person_x + 19,
        269,
        fill="#111111",
        width=5
    )

    # BRAT STANG

    arm_left = canvas.create_line(
        person_x - 8,
        212,
        person_x - 18,
        235,
        fill="#d9a36c",
        width=5
    )

    # BRATUL CARE CHEAMA TAXIUL

    person_arm_wave = canvas.create_line(
        person_x + 8,
        211,
        person_x + 30,
        192,
        fill="#d9a36c",
        width=5
    )

    person_parts = [
        head,
        hair,
        torso,
        leg_left,
        leg_right,
        shoe_left,
        shoe_right,
        arm_left,
        person_arm_wave
    ]

    # MODIFICARE:
    # coboram personajul cu 6 pixeli

    move_items(
        person_parts,
        0,
        6
    )


# ============================================================
# TAXI
# ============================================================

def draw_taxi():

    global taxi_parts
    global wheel_spokes
    global door
    global taxi_body

    # CAROSERIE

    taxi_body = canvas.create_polygon(
        taxi_x,
        taxi_y + 5,
        taxi_x + 25,
        taxi_y + 5,
        taxi_x + 48,
        taxi_y - 26,
        taxi_x + 112,
        taxi_y - 26,
        taxi_x + 140,
        taxi_y + 5,
        taxi_x + 165,
        taxi_y + 5,
        taxi_x + 165,
        taxi_y + 48,
        taxi_x,
        taxi_y + 48,
        fill=YELLOW,
        outline=""
    )

    # GEAM FATA

    front_window = canvas.create_polygon(
        taxi_x + 87,
        taxi_y - 21,
        taxi_x + 109,
        taxi_y - 21,
        taxi_x + 132,
        taxi_y + 2,
        taxi_x + 87,
        taxi_y + 2,
        fill=WINDOW_BLUE,
        outline=""
    )

    # GEAM SPATE

    rear_window = canvas.create_polygon(
        taxi_x + 53,
        taxi_y - 21,
        taxi_x + 82,
        taxi_y - 21,
        taxi_x + 82,
        taxi_y + 2,
        taxi_x + 35,
        taxi_y + 2,
        fill=WINDOW_BLUE,
        outline=""
    )

    # SEMN TAXI

    taxi_sign = canvas.create_rectangle(
        taxi_x + 67,
        taxi_y - 39,
        taxi_x + 101,
        taxi_y - 27,
        fill="#ffe875",
        outline=""
    )

    taxi_text = canvas.create_text(
        taxi_x + 84,
        taxi_y - 33,
        text="TAXI",
        font=("Arial", 7, "bold"),
        fill="#111111"
    )

    # FAR

    front_light = canvas.create_oval(
        taxi_x + 156,
        taxi_y + 13,
        taxi_x + 165,
        taxi_y + 23,
        fill="#fff6a9",
        outline=""
    )

    # STOP

    rear_light = canvas.create_oval(
        taxi_x,
        taxi_y + 14,
        taxi_x + 8,
        taxi_y + 24,
        fill="#d94747",
        outline=""
    )

    # ROTI

    rear_wheel = canvas.create_oval(
        taxi_x + 25,
        taxi_y + 35,
        taxi_x + 58,
        taxi_y + 68,
        fill="#080808",
        outline=""
    )

    front_wheel = canvas.create_oval(
        taxi_x + 110,
        taxi_y + 35,
        taxi_x + 143,
        taxi_y + 68,
        fill="#080808",
        outline=""
    )

    rear_center = canvas.create_oval(
        taxi_x + 35,
        taxi_y + 45,
        taxi_x + 48,
        taxi_y + 58,
        fill="#8b8b8b",
        outline=""
    )

    front_center = canvas.create_oval(
        taxi_x + 120,
        taxi_y + 45,
        taxi_x + 133,
        taxi_y + 58,
        fill="#8b8b8b",
        outline=""
    )

    # SPITE ROTI

    rear_spoke = canvas.create_line(
        taxi_x + 41,
        taxi_y + 39,
        taxi_x + 41,
        taxi_y + 64,
        fill=WHITE,
        width=2
    )

    front_spoke = canvas.create_line(
        taxi_x + 126,
        taxi_y + 39,
        taxi_x + 126,
        taxi_y + 64,
        fill=WHITE,
        width=2
    )

    # PORTIERA SPATE

    door = canvas.create_polygon(
        taxi_x + 90,
        taxi_y + 5,
        taxi_x + 132,
        taxi_y + 5,
        taxi_x + 132,
        taxi_y + 40,
        taxi_x + 90,
        taxi_y + 40,
        fill=YELLOW,
        outline=DARK_YELLOW,
        width=2
    )

    # MANER

    door_handle = canvas.create_line(
        taxi_x + 118,
        taxi_y + 13,
        taxi_x + 126,
        taxi_y + 13,
        fill="#806500",
        width=2
    )

    wheel_spokes = [
        rear_spoke,
        front_spoke
    ]

    taxi_parts = [
        taxi_body,
        front_window,
        rear_window,
        taxi_sign,
        taxi_text,
        front_light,
        rear_light,
        rear_wheel,
        front_wheel,
        rear_center,
        front_center,
        rear_spoke,
        front_spoke,
        door,
        door_handle
    ]


# ============================================================
# MANA CARE CHEAMA TAXIUL
# ============================================================

def wave_hand():

    global wave_direction

    if stage not in [
        "calling",
        "arriving"
    ]:

        return

    coords = canvas.coords(
        person_arm_wave
    )

    if len(coords) != 4:

        return

    x1 = coords[0]
    y1 = coords[1]

    x2 = coords[2]
    y2 = coords[3]

    y2 += wave_direction * 3

    if y2 >= 211:

        wave_direction = -1

    elif y2 <= 191:

        wave_direction = 1

    canvas.coords(
        person_arm_wave,
        x1,
        y1,
        x2,
        y2
    )

    root.after(
        90,
        wave_hand
    )


# ============================================================
# TAXIUL VINE
# ============================================================

def taxi_arriving():

    global taxi_x
    global loading
    global stage

    stage = "arriving"

    status_label.config(
        text="Taxi arriving..."
    )

    if taxi_x < TAXI_STOP_X:

        distance = 5

        if taxi_x + distance > TAXI_STOP_X:

            distance = TAXI_STOP_X - taxi_x

        move_items(
            taxi_parts,
            distance
        )

        taxi_x += distance

        progress_value = int(
            5
            +
            (
                (taxi_x + 190)
                /
                (TAXI_STOP_X + 190)
            )
            * 25
        )

        loading = min(
            30,
            progress_value
        )

        update_loading()

        root.after(
            35,
            taxi_arriving
        )

    else:

        loading = 32

        update_loading()

        stage = "arrived"

        status_label.config(
            text="Taxi arrived!"
        )

        root.after(
            650,
            open_door
        )


# ============================================================
# DESCHIDERE PORTIERA
# ============================================================

def open_door():

    global loading
    global stage

    stage = "door_open"

    status_label.config(
        text="Opening rear door..."
    )

    loading = 37

    update_loading()

    body_box = canvas.bbox(
        taxi_body
    )

    if body_box:

        x = body_box[0]
        y = taxi_y

        # MODIFICARE:
        # portiera se deschide mai mult

        canvas.coords(
            door,

            x + 90,
            y + 5,

            x + 132,
            y + 5,

            x + 165,
            y + 42,

            x + 102,
            y + 42
        )

    root.after(
        650,
        walk_to_taxi
    )


# ============================================================
# OMUL MERGE CATRE PORTIERA
# ============================================================

def walk_to_taxi():

    global person_walk_distance
    global loading
    global stage

    stage = "walking"

    status_label.config(
        text="Walking to the taxi..."
    )

    if person_walk_distance < 28:

        move_items(
            person_parts,
            -2
        )

        person_walk_distance += 2

        loading += 1

        if loading > 47:
            loading = 47

        update_loading()

        root.after(
            70,
            walk_to_taxi
        )

    else:

        root.after(
            300,
            enter_taxi
        )


# ============================================================
# OMUL INTRA IN TAXI
# ============================================================

def enter_taxi():

    global enter_step
    global loading
    global stage

    stage = "entering"

    status_label.config(
        text="Getting in..."
    )

    # MODIFICARE:
    # 15 pasi in loc de 10

    if enter_step < 15:

        # MODIFICARE:
        # merge mai mult spre stanga

        move_items(
            person_parts,
            -3,
            1
        )

        enter_step += 1

        loading += 1

        if loading > 55:
            loading = 55

        update_loading()

        root.after(
            70,
            enter_taxi
        )

    else:

        hide_items(
            person_parts
        )

        loading = 57

        update_loading()

        root.after(
            400,
            close_door
        )


# ============================================================
# INCHIDERE PORTIERA
# ============================================================

def close_door():

    global loading
    global stage

    stage = "door_closing"

    status_label.config(
        text="Closing door..."
    )

    body_box = canvas.bbox(
        taxi_body
    )

    if body_box:

        x = body_box[0]
        y = taxi_y

        canvas.coords(
            door,

            x + 90,
            y + 5,

            x + 132,
            y + 5,

            x + 132,
            y + 40,

            x + 90,
            y + 40
        )

    loading = 60

    update_loading()

    root.after(
        600,
        start_driving
    )


# ============================================================
# START DRIVING
# ============================================================

def start_driving():

    global stage

    stage = "driving"

    status_label.config(
        text="On the way..."
    )

    drive_animation()

    move_background()

    taxi_suspension()

    animate_wheels()

    create_smoke()

    animate_smoke()


# ============================================================
# FUNDAL IN MISCARE
# ============================================================

def move_background():

    if stage != "driving":

        return

    # CLADIRI

    for group in city_groups:

        move_items(
            group,
            -2
        )

        box = canvas.bbox(
            group[0]
        )

        if box and box[2] < -20:

            move_items(
                group,
                1100
            )

    # DRUM

    for line in road_lines:

        canvas.move(
            line,
            -9,
            0
        )

        coords = canvas.coords(
            line
        )

        if coords and coords[2] < 0:

            canvas.move(
                line,
                960,
                0
            )

    root.after(
        40,
        move_background
    )


# ============================================================
# SUSPENSIA TAXIULUI
# ============================================================

def taxi_suspension():

    global suspension_angle
    global last_suspension

    if stage != "driving":

        return

    suspension_angle += 0.35

    new_offset = math.sin(
        suspension_angle
    ) * 1.2

    difference = (
        new_offset
        -
        last_suspension
    )

    move_items(
        taxi_parts,
        0,
        difference
    )

    last_suspension = new_offset

    root.after(
        55,
        taxi_suspension
    )


# ============================================================
# ROTILE
# ============================================================

def animate_wheels():

    global wheel_angle

    if stage != "driving":

        return

    wheel_angle += 0.45

    wheels = [
        taxi_parts[7],
        taxi_parts[8]
    ]

    for index in range(2):

        box = canvas.bbox(
            wheels[index]
        )

        if not box:

            continue

        center_x = (
            box[0] + box[2]
        ) / 2

        center_y = (
            box[1] + box[3]
        ) / 2

        radius = 12

        x1 = (
            center_x
            +
            math.cos(wheel_angle)
            *
            radius
        )

        y1 = (
            center_y
            +
            math.sin(wheel_angle)
            *
            radius
        )

        x2 = (
            center_x
            -
            math.cos(wheel_angle)
            *
            radius
        )

        y2 = (
            center_y
            -
            math.sin(wheel_angle)
            *
            radius
        )

        canvas.coords(
            wheel_spokes[index],

            x1,
            y1,

            x2,
            y2
        )

    root.after(
        45,
        animate_wheels
    )


# ============================================================
# FUM
# ============================================================

def create_smoke():

    if stage != "driving":

        return

    box = canvas.bbox(
        taxi_body
    )

    if box:

        x = box[0] - 4
        y = box[3] - 18

        smoke = canvas.create_oval(
            x,
            y,
            x + 7,
            y + 7,
            fill="#777b82",
            outline=""
        )

        smoke_particles.append(
            smoke
        )

    root.after(
        260,
        create_smoke
    )


def animate_smoke():

    if stage != "driving":

        return

    for smoke in smoke_particles[:]:

        canvas.move(
            smoke,
            -3,
            -1
        )

        coordinates = canvas.coords(
            smoke
        )

        if coordinates:

            if coordinates[2] < 0:

                canvas.delete(
                    smoke
                )

                smoke_particles.remove(
                    smoke
                )

    root.after(
        50,
        animate_smoke
    )


# ============================================================
# ANIMATIA DE CONDUS
# ============================================================

def drive_animation():

    global loading
    global taxi_x

    if stage != "driving":

        return

    body_box = canvas.bbox(
        taxi_body
    )

    if body_box:

        taxi_center = (
            body_box[0]
            +
            body_box[2]
        ) / 2

        if taxi_center < 420:

            move_items(
                taxi_parts,
                3
            )

            taxi_x += 3

    loading += 1

    if loading > 100:

        loading = 100

    update_loading()

    if loading >= 100:

        finish_loading()

        return

    root.after(
        65,
        drive_animation
    )


# ============================================================
# FINAL
# ============================================================

def finish_loading():

    global stage

    stage = "finished"

    status_label.config(
        text="Ready!"
    )

    progress["value"] = 100

    percent_label.config(
        text="100%"
    )

    root.after(
        1200,
        fade_out
    )


# ============================================================
# FADE OUT
# ============================================================

def fade_out():

    alpha = root.attributes(
        "-alpha"
    )

    alpha -= 0.04

    if alpha > 0:

        root.attributes(
            "-alpha",
            alpha
        )

        root.after(
            40,
            fade_out
        )

    else:

        root.destroy()


# ============================================================
# DESENAM SCENA
# ============================================================

draw_sky()

draw_city()

draw_road()

draw_person()

draw_taxi()


# ============================================================
# PORNIREA ANIMATIEI
# ============================================================

root.after(
    500,
    taxi_arriving
)

root.after(
    500,
    wave_hand
)


# ============================================================
# START PROGRAM
# ============================================================

root.mainloop()