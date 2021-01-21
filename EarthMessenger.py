# Resolution: 1366x768
# Special thanks to Kenney for the game assets
from tkinter import Tk, PhotoImage, Button, Label, LabelFrame, Message, Canvas, messagebox, Entry, Toplevel, Checkbutton, IntVar, StringVar, OptionMenu
import time
import random
import json


# DEFINING FUNCTION SECTION


def change_settings():
    """Takes the settings values and store it to data.json"""
    with open("data/data.json", "r+") as file:
        data = json.load(file)
        print("hi")
        if(initial_hint.get() == 0):
            data['initial_hint'] = False
        if(initial_hint.get() == 1):
            data['initial_hint'] = True

        if(fall_speed.get() == "Fast"):
            data['fall_speed'] = "fast"
        if(fall_speed.get() == "Medium"):
            data['fall_speed'] = "medium"
        if(fall_speed.get() == "Slow"):
            data['fall_speed'] = "slow"

        if(enemy.get() == 0):
            data['enemy'] = False
        if(enemy.get() == 1):
            data['enemy'] = True

        if(numbers_shown.get() == 0):
            data['numbers_shown'] = False
        if(numbers_shown.get() == 1):
            data['numbers_shown'] = True

        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2)


def boss_key(event):
    """Will open a top level to pretend working"""
    main.attributes("-fullscreen", False)
    boss_key_window = Toplevel(main)
    boss_key_window.title("What is boss key about?")
    boss_key_window.geometry("1366x768")
    boss_key_window.iconbitmap("images/EarthMessenger_Icon.ico")

    boss_key_label = Label(boss_key_window, image=boss_key_image)
    boss_key_label.pack()


def pause():
    """Pause the game"""

    repeat_continue_or_home = messagebox.askyesnocancel(
        "E. M. Pause", "Do you want to repeat mission (Yes), continue mission (No), or cancel mission (Cancel)?")
    if (repeat_continue_or_home):
        game_set_up(level-1)
    elif not(repeat_continue_or_home):
        return
    elif(repeat_continue_or_home is None):
        choose_level()


def input_leader_board():
    """Reassuring input and make record on leader board"""
    name = leader_board_input_name.get()
    yes_or_no = messagebox.askquestion(
        "E. M. Leader Board", "You are going to be recorded as "+name+", are you sure?")
    if (yes_or_no == "no"):
        return
    elif(yes_or_no == "yes"):
        with open("data/data.json", "r+") as file:
            data = json.load(file)
            for i in range(10):
                # If found a worse record than this one
                if (level > data['leader_board'][i]['lv'] or (level == data['leader_board'][i]['lv'] and time_used < data['leader_board'][i]['time'])):
                    # Insert into the list
                    data['leader_board'].insert(
                        i, {'name': name, 'lv': level, 'time': time_used})
                    break
            # Delete the 11th candidate
            del data['leader_board'][10]
            file.seek(0)
            file.truncate()
            json.dump(data, file, indent=2)
        confirming_record = messagebox.showinfo(
            "E. M. Leader Board", "Your score has been recorded!")
        # Delete unwilling frames and button
        leader_board_input_frame.place_forget()
        add_to_leader_board_button.place_forget()


def delete_leader_board_input_frame():
    """Just for deleting leader board input frame"""
    leader_board_input_frame.place_forget()


def add_to_leader_board():
    """Allow players enter their names to leader board"""

    global leader_board_input_frame, leader_board_input_name

    # Create leader board input frame
    leader_board_input_frame = LabelFrame(
        game_canvas, borderwidth=2, bg="#aacfd0", relief="groove")
    leader_board_input_frame.place(x=341, y=192, relwidth=0.5, relheight=0.5)

    leader_board_input_title = Label(leader_board_input_frame, text="LEADER BOARD REGISTER", font=(
        "Courier", 30, "bold"), justify="center", anchor="center", bg="#aacfd0", padx=70, pady=20)
    leader_board_input_title.grid(
        row=0, column=0, columnspan=2, sticky="w"+"e")

    # Ask player name and shows information about this record
    leader_board_input_information_name = Label(leader_board_input_frame, text="Player Name: ", font=(
        "Courier", 15), justify="right", anchor="center", bg="#aacfd0")
    leader_board_input_information_name.grid(row=1, column=0)

    leader_board_input_information_lv = Label(leader_board_input_frame, text="LV: ", font=(
        "Courier", 15), justify="right", anchor="center", bg="#aacfd0")
    leader_board_input_information_lv.grid(row=2, column=0)

    leader_board_input_information_time = Label(leader_board_input_frame, text="Time Used: ", font=(
        "Courier", 15), justify="right", anchor="center", bg="#aacfd0")
    leader_board_input_information_time.grid(row=3, column=0)

    leader_board_input_name = Entry(leader_board_input_frame, font=(
        "Courier", 15), justify="left", bg="#ffffff")
    leader_board_input_name.insert(0, "Player Name")
    leader_board_input_name.grid(row=1, column=1, sticky="w"+"e")

    leader_board_input_lv = Entry(leader_board_input_frame, font=(
        "Courier", 15), justify="left", bg="#ffffff")
    leader_board_input_lv.insert(0, str(level))
    leader_board_input_lv.configure(state="disabled")
    leader_board_input_lv.grid(row=2, column=1, sticky="w"+"e")

    leader_board_input_time = Entry(leader_board_input_frame, font=(
        "Courier", 15), justify="left", bg="#ffffff")
    leader_board_input_time.insert(0, str(time_used))
    leader_board_input_time.configure(state="disabled")
    leader_board_input_time.grid(row=3, column=1, sticky="w"+"e")

    OK_button = Button(leader_board_input_frame, text="OK", font=(
        "Courier", 25), justify="center", bg="#aacfd0", command=input_leader_board, padx=50, pady=20)
    OK_button.grid(row=4, column=0, sticky="e", padx=20, pady=20)

    cancel_button = Button(leader_board_input_frame, text="CANCEL", font=(
        "Courier", 25), justify="center", bg="#aacfd0", command=delete_leader_board_input_frame, padx=50, pady=20)
    cancel_button.grid(row=4, column=1, sticky="w", padx=20, pady=20)


def correct_code():
    """If player introduced correct code"""

    global level, victory_frame, progress, add_to_leader_board_button

    # Save game progress to progress.txt file
    if (level == progress):
        progress += 1
    with open("data/data.json", "r+") as file:
        data = json.load(file)
        data['level'] = progress
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2)

    # Rocket launched when correct
    game_canvas.delete(rocket)
    launch_rocket = game_canvas.create_image(
        1050, 550, image=launch_rocket_image)
    launch_rocket_position = game_canvas.bbox(launch_rocket)
    while (launch_rocket_position[3] > 0):
        game_canvas.move(launch_rocket, 0, -10)
        main.after(1, main.update())
        launch_rocket_position = game_canvas.bbox(launch_rocket)

    # Create victory frame
    victory_frame = LabelFrame(game_canvas, borderwidth=0, bg="#aacfd0")
    victory_frame.place(x=341, y=192, relwidth=0.5, relheight=0.5)

    victory_title = Label(victory_frame, text="VICTORY", font=(
        "Courier", 50, "bold"), justify="center", anchor="center", bg="#aacfd0")
    victory_title.pack()

    victory_information = Label(victory_frame, text="In: LV " + str(level) + " - " + str(
        time_used)+"s", font=("Courier", 30), justify="center", anchor="center", bg="#aacfd0")
    victory_information.pack()

    victory_text = Message(victory_frame, text="We have just won a battle thanks to your message! \n You can challenge the next level now!", font=(
        "Courier", 15), justify="center", anchor="center", bg="#aacfd0")
    victory_text.pack()

    level_button = Button(victory_frame, borderwidth=1, image=level_button_image,
                          bg="#aacfd0", relief="raised", command=choose_level)
    level_button.place(x=221, y=292)

    home_button = Button(victory_frame, borderwidth=1, image=home_button_image,
                         bg="#aacfd0", relief="raised", command=main_buttons)
    home_button.place(x=321, y=292)
    # level-1 because in the method it will add 1 again
    repeat_button = Button(victory_frame, borderwidth=1, image=repeat_button_image,
                           bg="#aacfd0", relief="raised", command=lambda: game_set_up(level-1))
    repeat_button.place(x=421, y=292)

    with open("data/data.json", "r+") as file:
        data = json.load(file)
        better = False
        for i in range(10):
            if (level > data['leader_board'][i]['lv'] or (level == data['leader_board'][i]['lv'] and time_used < data['leader_board'][i]['time'])):
                better = True
                break
        if (better):
            add_to_leader_board_button = Button(
                victory_frame, borderwidth=1, image=leader_board_icon_image, bg="#aacfd0", relief="raised", command=add_to_leader_board)
            add_to_leader_board_button.place(x=600, y=75)


def incorrect_code():
    """If player introduced incorrect code"""

    global defeat_frame

    # Explosion when wrong
    explosions = []
    for j in range(4):
        explosions.append(game_canvas.create_image(
            685, 550, image=random.choice(explosion_images)))
        main.after(5, main.update())
    for j in range(4):
        main.after(5, game_canvas.delete(explosions[j]))

    # Create defeat frame
    defeat_frame = LabelFrame(game_canvas, borderwidth=0, bg="#aacfd0")
    defeat_frame.place(x=341, y=192, relwidth=0.5, relheight=0.5)

    defeat_title = Label(defeat_frame, text="DEFEAT", font=(
        "Courier", 50, "bold"), justify="center", anchor="center", bg="#aacfd0")
    defeat_title.pack()

    defeat_information = Label(defeat_frame, text="In: LV " + str(level) + " - " + str(
        time_used)+"s", font=("Courier", 30), justify="center", anchor="center", bg="#aacfd0")
    defeat_information.pack()

    defeat_text = Message(defeat_frame, text="The battle was hard without your message... \n Nevermind, fighting for the next time!", font=(
        "Courier", 15), justify="center", anchor="center", bg="#aacfd0")
    defeat_text.pack()

    level_button = Button(defeat_frame, borderwidth=1, image=level_button_image,
                          bg="#aacfd0", relief="raised", command=choose_level)
    level_button.place(x=221, y=292)

    home_button = Button(defeat_frame, borderwidth=1, image=home_button_image,
                         bg="#aacfd0", relief="raised", command=main_buttons)
    home_button.place(x=321, y=292)
    # level-1 because in the method it will add 1 again
    repeat_button = Button(defeat_frame, borderwidth=1, image=repeat_button_image,
                           bg="#aacfd0", relief="raised", command=lambda: game_set_up(level-1))
    repeat_button.place(x=421, y=292)


def code_box_movement(event):
    """Will let the box move around the canvas when pressed"""
    global code_box, vortex_position, time_used

    mouse_x = event.x
    mouse_y = event.y

    game_canvas.coords(code_box, mouse_x, mouse_y)

    # Check for collision between vortex and box
    code_box_position = game_canvas.coords(code_box)

    # Error when moving twice due to mouse speed
    try:
        if(vortex_position[0] < code_box_position[0] < vortex_position[2] and vortex_position[1] < code_box_position[1] < vortex_position[3]):

            # Start checking the code

            # Store as string
            code_entered = enter_code.get()

            # In case that enter_code is empty
            if (enter_code.get() == ""):
                code_entered = "l"

            # Check if any letter doesn't match
            for i in range(level):
                if (not(code_entered[i] == str(airdrops[i]))):
                    correct = False
                    break
                correct = True
            finish = time.time()
            time_used = round((finish - start), 3)

            if (level == 1):
                correct_or_incorrect = messagebox.showinfo(
                    "E. M. Guideline", "It's the moment of truth, if code is CORRECT, the ROCKET WILL LAUNCH, otherwise, the vortex will BLOW UP.")
                main.after(50)

            # Cheat code "life"
            game_canvas.delete(code_box)
            main.after(2000)
            if (correct or code_entered == "life"):
                correct_code()
            elif not(correct):
                incorrect_code()

    except IndexError:
        pass


def create_code_box():
    """To build a image that the player can move"""

    global code_box

    # Store as string
    code_entered = enter_code.get()

    # Create an object to move
    if (level == 1):
        move_code_box = messagebox.showinfo(
            "E. M. Guideline", "Now your code is contained in this box. Move it to the vortex below to check whether the code is correct!")
    code_box = game_canvas.create_image(683, 200, image=code_box_image)
    # Clear entry box and button
    enter_code.place_forget()
    enter_button.place_forget()
    game_canvas.bind("<B1-Motion>", code_box_movement)


def airdrop_starts():
    """Start dropping aidrops with numbers"""

    global airdrops
    airdrops = []
    # Add airdrops
    for i in range(level):
        airdrops.append(random.randint(0, 9))

    # Guide
    if (level == 1):
        remember_the_code = messagebox.showinfo(
            "E. M. Guideline", "Remember the numbers appearing soon in the correct order. This will be the code you should introduce later!")

    # Read the speed and if want enemy in data.json
    update_gap_time = 10
    want_enemy = True
    with open("data/data.json", "r") as file:
        data = json.load(file)
        if(data['fall_speed'] == "fast"):
            update_gap_time = 1
        if(data['fall_speed'] == "medium"):
            update_gap_time = 10
        if(data['fall_speed'] == "slow"):
            update_gap_time = 20

        want_enemy = data['enemy']

    # Airdrop starts to fall, enemy and missil Collision
    for i in airdrops:
        # Move distance of the airdrops
        movement_distance = 1
        airdrop = game_canvas.create_image(683, 0, image=airdrop_images[i])
        collision = False

        while not(collision):

            game_canvas.move(airdrop, 0, movement_distance)
            airdrop_position = game_canvas.bbox(airdrop)

            # Make the enemy aircraft appear and launch missil. The numbers in the condition is due to can't be sure when adding value is around 2.
            if(want_enemy):
                if (airdrop_position[3]//1 in (320, 319, 318)):
                    missil = game_canvas.create_image(
                        350, 300, image=missil_image)
                    enemy = game_canvas.create_image(250, 300, image=random.choice(
                        [aircraft_1_image, aircraft_2_image, aircraft_3_image, aircraft_4_image]))
                    main.after(10)

                    while not (collision):

                        game_canvas.move(missil, 25, 0,)
                        missil_position = game_canvas.bbox(missil)
                        # Collision detection, if missil going from left side goes further than the left border of the airdrop, then collides.
                        if (missil_position[0] > airdrop_position[0]):
                            collision = True
                            main.after(10)
                            # Delete missil and sirdrop
                            game_canvas.delete(missil)
                            game_canvas.delete(airdrop)
                            # Create some explosion
                            explosions = []
                            for j in range(7):
                                explosions.append(game_canvas.create_image(
                                    683, 300, image=random.choice(explosion_images)))
                                main.after(5, main.update())
                            for j in range(7):
                                main.after(
                                    5, game_canvas.delete(explosions[j]))

                            game_canvas.delete(enemy)

                            break
                        # Just in case that the missil haven't touched the airdrop
                        if (missil_position[0] > 1366):
                            game_canvas.delete(missil)
                            break
                        main.after(5, main.update())

            main.after(update_gap_time, main.update())

            # Change speed over time, being terminal speed at some point
            if (movement_distance < 4):
                movement_distance += 0.01
            # Were for test purpose but it is fine to leave it for settings
            if (airdrop_position[1] > 400):
                main.after(50, game_canvas.delete(airdrop))
                break
    # Guide
    if (level == 1):
        enter_the_code = messagebox.showinfo(
            "E. M. Guideline", "Now, enter the code that you have just seen to send the key message! Once entered, press the send button.")

    # Entry box
    global enter_code, start, enter_button
    start = time.time()

    # Read settings in data.json if want number or *
    number = False
    with open("data/data.json", "r") as file:
        data = json.load(file)
        number = data['numbers_shown']

    if not(number):
        enter_code = Entry(game_canvas, width=level, bg="#000000", fg="#42A8DB", font=(
            "Courier", 25), show="*", justify="center", insertbackground="#42A8DB")
    elif (number):
        enter_code = Entry(game_canvas, width=level, bg="#000000", fg="#42A8DB", font=(
            "Courier", 25), justify="center", insertbackground="#42A8DB")
    enter_code.place(x=600, y=200)

    # Send button
    enter_button = Button(game_canvas, image=enter_button_image,
                          command=create_code_box, bg="#000000", borderwidth=5)
    enter_button.place(x=550, y=200)


def game_set_up(lv):
    """Game's background setting"""

    global game_canvas, level, rocket

    # Clean any possible previous frames
    try:
        victory_frame.place_forget()
        defeat_frame.place_forget()
    except NameError:
        pass

    main.after(1000)

    # Set global level
    level = lv + 1

    # Creating game canvas
    game_canvas = Canvas(main_frame, borderwidth=0, highlightthickness=0)
    game_canvas.place(x=0, y=0, relwidth=1, relheight=1)

    # Background for the game
    game_canvas_bg = game_canvas.create_image(
        0, 0, anchor="nw", image=main_bg_image)

    # Creating starry upper background (Stewart's video helped a lot, although I already had this idea in the first place)

    background_star = []
    star_colors = ["#f0f5f9", "#c9d6de", "#52616a", "#005f6b", "#D1B6E1"]

    for i in range(500):
        y = random.randint(0, 300)
        if (y > 100):
            y = random.randint(0, 300)
        if (y > 200):
            y = random.randint(0, 300)

        x = random.randint(0, 1366)
        if (x > 800 and i % 3 == 0):
            x = random.randint(0, 1366)

        size = random.randint(0, 3)
        if (size > 2):
            size = random.randint(0, 4)
        color = random.choice(star_colors)

        xy = (x, y, x+size, y+size)
        background_star.append(
            game_canvas.create_oval(xy, fill=color, width=0))

    # Setting the grass ground
    initial_x = 0
    initial_y = 400
    # Used to decide if it's in a normal row/column, or need a bit of indentation
    modify_x = True
    grass = []
    while (initial_y <= 768):
        while(initial_x <= 1466):
            grass.append(game_canvas.create_image(
                initial_x, initial_y, image=grass_and_soil_image))
            initial_x += 100
        if (modify_x):
            initial_x = 50
            modify_x = False
        else:
            initial_x = 0
            modify_x = True

        initial_y += 25

    # Placing some decoration
    small_base = game_canvas.create_image(200, 450, image=small_base_image)
    large_base = game_canvas.create_image(150, 600, image=large_base_image)
    satellite_1 = game_canvas.create_image(340, 470, image=satellite_2_image)
    satellite_2 = game_canvas.create_image(280, 510, image=satellite_2_image)
    satellite_3 = game_canvas.create_image(400, 500, image=satellite_1_image)
    satellite_4 = game_canvas.create_image(340, 540, image=satellite_1_image)
    aircraft_cargo = game_canvas.create_image(
        1250, 400, image=aircraft_cargo_image)
    aircraft_miner = game_canvas.create_image(
        1250, 550, image=aircraft_miner_image)
    rocket = game_canvas.create_image(1050, 550, image=rocket_image)
    transmitting_gate_NE = game_canvas.create_image(
        740, 500, image=transmitting_gate_NE_image)
    transmitting_gate_NW = game_canvas.create_image(
        630, 500, image=transmitting_gate_NW_image)
    vortex = game_canvas.create_image(685, 550, image=vortex_image)
    transmitting_gate_SE = game_canvas.create_image(
        740, 560, image=transmitting_gate_SE_image)
    transmitting_gate_SW = game_canvas.create_image(
        630, 560, image=transmitting_gate_SW_image)
    for i in range(4):
        main.after(500, game_canvas.delete(vortex))
        if (i % 2 == 0):
            vortex = game_canvas.create_image(
                685, 550, image=vortex_change_image)
        else:
            vortex = game_canvas.create_image(685, 550, image=vortex_image)
        main.update()

    global vortex_position
    vortex_position = game_canvas.bbox(vortex)

    # Quit button
    quit_button = Button(main_frame, text="QUIT", padx=2, pady=1, borderwidth=3, image=quit_button_image,
                         relief="groove", font=("Monotype Corsiva", 15), fg="#f0f5f9", bg="#1e2022", command=main.quit)
    quit_button.grid(row=0, column=0, sticky="W")

    # Changing full screen mode
    change_full_screen_button = Button(main_frame, text="Change\nScreen\nMode", padx=2, pady=1, borderwidth=3, relief="groove", font=(
        "Monotype Corsiva", 15), fg="#f0f5f9", bg="#1e2022", command=lambda: changeFullScreenMain(0))
    change_full_screen_button.grid(row=0, column=0, sticky="W")
    change_full_screen_button.place(x=1295)

    # Pause button
    pause_button = Button(game_canvas, image=pause_icon_image,
                          borderwidth=0, bg="#1e2022", command=pause)
    pause_button.place(x=0, y=718)

    airdrop_starts()


def choose_level():
    """Will let player choose the wanted level"""

    global progress

    main.after(200)

    # Creating choose label frame
    choose_level_frame = LabelFrame(main_frame, borderwidth=0)
    choose_level_frame.place(x=0, y=0, relwidth=1, relheight=1)

    # Blurred background for main frames
    choose_level_frame_bg = Label(
        choose_level_frame, image=main_bg_image_blurred)
    choose_level_frame_bg.place(x=0, y=0, relwidth=1, relheight=1)

    # Title of choose_level frame
    choose_level_title = Label(choose_level_frame, text="CHOOSE LEVEL", font=(
        "Monotype Corsiva", 40), borderwidth=0, fg="#f0f5f9", bg="#1e2022", padx=500)
    choose_level_title.grid(
        row=0, column=0, columnspan=7, sticky="w"+"e", pady=100)

    # Quit button
    quit_button = Button(main_frame, text="QUIT", padx=2, pady=1, borderwidth=3, image=quit_button_image,
                         relief="groove", font=("Monotype Corsiva", 15), fg="#f0f5f9", bg="#1e2022", command=main.quit)
    quit_button.grid(row=0, column=0, sticky="W")

    # Changing full screen mode
    change_full_screen_button = Button(main_frame, text="Change\nScreen\nMode", padx=2, pady=1, borderwidth=3, relief="groove", font=(
        "Monotype Corsiva", 15), fg="#f0f5f9", bg="#1e2022", command=lambda: changeFullScreenMain(0))
    change_full_screen_button.grid(row=0, column=0, sticky="W")
    change_full_screen_button.place(x=1295)

    # Back button
    choose_level_back_button = Button(
        choose_level_frame, image=back_button_image, borderwidth=0, command=main_buttons)
    choose_level_back_button.place(x=0, y=693)

    # Update progress
    with open("data/data.json") as file:
        data = json.load(file)
        progress = data['level']

    # Level buttons
    initial_row = 1
    initial_column = 1
    level_buttons = [None]*15
    for i in range(15):
        level_buttons[i] = Button(choose_level_frame, text="LV"+str(i+1), font=("Forte", 25), fg="#011638", bg="#7E7F94",
                                  padx=10, pady=10, state="disabled", anchor="center", justify="center", command=lambda i=i: game_set_up(i))
        level_buttons[i].grid(row=(initial_row+(i//5)),
                              column=(initial_column+(i % 5)), padx=50, pady=20)

        if (i < progress):
            level_buttons[i].configure(state="active")


def new_game():
    """Will clear content in progress.txt file, and reset it to 1, then set progress to 1"""

    global progress

    start_game_frame.place_forget()

    with open("data/data.json", "r+") as file:
        data = json.load(file)
        data['level'] = 1
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2)

    progress = 1

    choose_level()


def load_game():
    """Will read the progress in progress.txt file and load it to progress variable"""

    global progress

    start_game_frame.place_forget()

    with open("data/data.json") as file:
        data = json.load(file)
        progress = data['level']

    choose_level()


def introduction_page():
    """Function that shows all the features of introduction page"""

    # Creating introduction frame
    introduction_frame = LabelFrame(main_frame, borderwidth=0)
    introduction_frame.place(x=0, y=0, relwidth=1, relheight=1)

    # Blurred background for main frames
    introduction_frame_bg = Label(
        introduction_frame, image=main_bg_image_blurred)
    introduction_frame_bg.place(x=0, y=0, relwidth=1, relheight=1)

    # Title of introduction frame
    empty_filler_text = Message(
        introduction_frame, text="     ", bg="#000000", borderwidth=0)
    empty_filler_text.grid(row=0, column=0)
    introduction_title = Label(
        introduction_frame, image=introduction_title_image, anchor="center", borderwidth=0)
    introduction_title.grid(row=0, column=1, columnspan=3)

    # Quit button
    quit_button = Button(main_frame, text="QUIT", padx=2, pady=1, borderwidth=3, image=quit_button_image,
                         relief="groove", font=("Monotype Corsiva", 15), fg="#f0f5f9", bg="#1e2022", command=main.quit)
    quit_button.grid(row=0, column=0, sticky="W")

    # Changing full screen mode
    change_full_screen_button = Button(main_frame, text="Change\nScreen\nMode", padx=2, pady=1, borderwidth=3, relief="groove", font=(
        "Monotype Corsiva", 15), fg="#f0f5f9", bg="#1e2022", command=lambda: changeFullScreenMain(0))
    change_full_screen_button.place(x=1295)

    # Adding information icon
    introduction_information_icon = Label(
        introduction_frame, image=introduction_information_icon_image, bg="#011638", anchor="w", borderwidth=0)
    introduction_information_icon.grid(row=1, column=0)

    # Background story
    background_story_title = Label(introduction_frame, text="BACKGROUND STORY ", anchor="e", font=(
        "Forte", 25), bg="#1D2C42", fg="#ffffff", pady=58)
    background_story_title.grid(row=2, column=0, columnspan=2, sticky="W"+"E")
    background_story = Label(introduction_frame, text="  Curtains open, cosmos panorama. Years since crashes between galactic civilizations started; millions of rays shooting, uncountable spacecraft, spies on enemies spaceships, the war began!\n\n  Your role in the war is a MESSENGER ON EARTH. In this immense battlefield, any piece of information can be the decisive, and you are responsible for receiving CODES PACKAGED AS NUMBERS in airdrop form, and introducing the code to SEND the rocket with the vital MESSAGE! BUT, the enemy is always watching to DESTROY the code, you should REMEMBER the code!", font=("Lucida Calligraphy", 15), bg="#1D2C42", fg="#ffffff", justify="left", wraplength=800)
    background_story.grid(row=2, column=2, rowspan=3,
                          columnspan=2, ipady=20, sticky="w"+"e", pady=40)

    # Author notes
    author_notes_title = Label(introduction_frame, text="AUTHOR NOTES ", anchor="e", font=(
        "Forte", 25), bg="#1D2C42", fg="#ffffff", pady=16)
    author_notes_title.grid(row=5, column=0, columnspan=2, sticky="W"+"E")
    author_notes = Label(introduction_frame, text="  This game is actually testing one's Short Term Memory (STM), with a Digit Span Task. This consists in showing a list of numbers, which the participants are asked to recall after in the same order. Theorically, one's digit span is around 7 (±2), with scarce exceptions.", font=(
        "Lucida Calligraphy", 15), bg="#1D2C42", fg="#ffffff", anchor="w", padx=10, justify="left", wraplength=800)
    author_notes.grid(row=5, column=2, rowspan=2, columnspan=2,
                      ipady=20, sticky="w"+"e", pady=40)

    # Back button
    introduction_back_button = Button(
        introduction_frame, image=back_button_image, borderwidth=0, command=introduction_frame.place_forget)
    introduction_back_button.place(x=0, y=693)


def start_game_page():
    """Function that shows new game or load game page"""

    global start_game_frame

    # Creating leader board frame
    start_game_frame = LabelFrame(main_frame, borderwidth=0)
    start_game_frame.place(x=0, y=0, relwidth=1, relheight=1)

    # Blurred background for main frames
    start_game_frame_bg = Label(start_game_frame, image=main_bg_image_blurred)
    start_game_frame_bg.place(x=0, y=0, relwidth=1, relheight=1)

    # Quit button
    quit_button = Button(main_frame, text="QUIT", padx=2, pady=1, borderwidth=3, image=quit_button_image,
                         relief="groove", font=("Monotype Corsiva", 15), fg="#f0f5f9", bg="#1e2022", command=main.quit)
    quit_button.grid(row=0, column=0, sticky="W")

    # Changing full screen mode
    change_full_screen_button = Button(main_frame, text="Change\nScreen\nMode", padx=2, pady=1, borderwidth=3, relief="groove", font=(
        "Monotype Corsiva", 15), fg="#f0f5f9", bg="#1e2022", command=lambda: changeFullScreenMain(0))
    change_full_screen_button.place(x=1295)

    # New game and lead game button
    new_game_button = Button(
        start_game_frame, image=new_game_image, borderwidth=5, command=new_game)
    new_game_button.place(x=43, y=50)

    load_game_button = Button(
        start_game_frame, image=load_game_image, borderwidth=5, command=load_game)
    load_game_button.place(x=43, y=400)

    # Back button
    start_game_back_button = Button(
        start_game_frame, image=back_button_image, borderwidth=0, command=start_game_frame.place_forget)
    start_game_back_button.place(x=0, y=693)


def leader_board_page():
    """Function that shows all the features of leader board page"""

    # Creating leader board frame
    leader_board_frame = LabelFrame(main_frame, borderwidth=0)
    leader_board_frame.place(x=0, y=0, relwidth=1, relheight=1)

    # Blurred background for main frames
    leader_board_frame_bg = Label(
        leader_board_frame, image=main_bg_image_blurred)
    leader_board_frame_bg.place(x=0, y=0, relwidth=1, relheight=1)

    # Title of leader_board frame
    leader_board_title = Label(
        leader_board_frame, image=leader_board_title_image, borderwidth=0)
    leader_board_title.grid(row=0, column=1, columnspan=4)

    # Adding leader board icon
    leader_board_information_icon = Label(
        leader_board_frame, image=leader_board_icon_image, bg="#011638", anchor="w", borderwidth=0)
    leader_board_information_icon.grid(row=1, column=0)

    # Quit button
    quit_button = Button(main_frame, text="QUIT", padx=2, pady=1, borderwidth=3, image=quit_button_image,
                         relief="groove", font=("Monotype Corsiva", 15), fg="#f0f5f9", bg="#1e2022", command=main.quit)
    quit_button.grid(row=0, column=0, sticky="W")

    # Changing full screen mode
    change_full_screen_button = Button(main_frame, text="Change\nScreen\nMode", padx=2, pady=1, borderwidth=3, relief="groove", font=(
        "Monotype Corsiva", 15), fg="#f0f5f9", bg="#1e2022", command=lambda: changeFullScreenMain(0))
    change_full_screen_button.place(x=1295)

    # Back button
    leader_board_home_button = Button(leader_board_frame, image=home_button_image,
                                      borderwidth=0, bg="#000000", command=leader_board_frame.place_forget)
    leader_board_home_button.place(x=0, y=718)

    # Take data from data/data.json
    with open("data/data.json") as file:
        data = json.load(file)

    # Creating leader board numbers
    leader_board_numbers = []
    for i in range(1, 11):
        leader_board_numbers.append(Label(leader_board_frame, text=str(
            i)+".", font=("Forte", 20), bg="#7E7F94", justify="right", padx=5, pady=5))
        leader_board_numbers[i-1].grid(row=1+i, column=1, padx=20, pady=5)

    # Leader board names
    leader_board_name = Label(leader_board_frame, text="Player Name", font=(
        "Lucida Calligraphy", 40), bg="#7E7F94", justify="center")
    leader_board_name.grid(row=1, column=2, pady=20, sticky="w"+"e")
    # Leader board level
    leader_board_name = Label(leader_board_frame, text="Level", font=(
        "Lucida Calligraphy", 40), bg="#7E7F94", justify="center")
    leader_board_name.grid(row=1, column=3, pady=20, sticky="w"+"e")
    # Leader board time
    leader_board_name = Label(leader_board_frame, text="Time", font=(
        "Lucida Calligraphy", 40), bg="#7E7F94", justify="center")
    leader_board_name.grid(row=1, column=4, pady=20, sticky="w"+"e")

    # To make sure it's not lost
    all_data_from_records = [[], [], []]

    i = 0
    for j in range(len(data['leader_board'])):
        all_data_from_records[0].append(Label(leader_board_frame, text=data['leader_board'][j]['name'], font=(
            "Courier", 20), justify="left", bg="#7E7F94", padx=5, pady=5))
        all_data_from_records[0][j].grid(row=2+i, column=2, sticky="w"+"e")
        all_data_from_records[1].append(Label(leader_board_frame, text=str(
            data['leader_board'][j]['lv']), font=("Courier", 20), justify="left", bg="#7E7F94", padx=5, pady=5))
        all_data_from_records[1][j].grid(row=2+i, column=3, sticky="w"+"e")
        all_data_from_records[2].append(Label(leader_board_frame, text=str(
            data['leader_board'][j]['time']), font=("Courier", 20), justify="left", bg="#7E7F94", padx=5, pady=5))
        all_data_from_records[2][j].grid(row=2+i, column=4, sticky="w"+"e")
        i += 1


def settings_page():
    """Function that shows all the features of settings page"""

    global initial_hint, fall_speed, enemy, numbers_shown

    # Creating settings frame
    settings_frame = LabelFrame(main_frame, borderwidth=0)
    settings_frame.place(x=0, y=0, relwidth=1, relheight=1)

    # Blurred background for main frames
    settings_frame_bg = Label(settings_frame, image=main_bg_image_blurred)
    settings_frame_bg.place(x=0, y=0, relwidth=1, relheight=1)

    # Title of settings frame
    settings_title = Label(
        settings_frame, image=settings_title_image, borderwidth=0)
    settings_title.grid(row=0, column=1, columnspan=3)

    # Adding settings icon
    settings_information_icon = Label(
        settings_frame, image=settings_icon_image, bg="#011638", anchor="w", borderwidth=0)
    settings_information_icon.grid(row=1, column=0)

    # Quit button
    quit_button = Button(main_frame, text="QUIT", padx=2, pady=1, borderwidth=3, image=quit_button_image,
                         relief="groove", font=("Monotype Corsiva", 15), fg="#f0f5f9", bg="#1e2022", command=main.quit)
    quit_button.grid(row=0, column=0, sticky="W")

    # Changing full screen mode
    change_full_screen_button = Button(main_frame, text="Change\nScreen\nMode", padx=2, pady=1, borderwidth=3, relief="groove", font=(
        "Monotype Corsiva", 15), fg="#f0f5f9", bg="#1e2022", command=lambda: changeFullScreenMain(0))
    change_full_screen_button.place(x=1295)

    # Back button
    settings_back_button = Button(
        settings_frame, image=back_button_image, borderwidth=0, command=settings_frame.place_forget)
    settings_back_button.place(x=0, y=693)

    # initial hint
    settings_initial_hint_text = Label(settings_frame, text="Initial fullscreen hint:", font=(
        "Courier", 30), anchor="e", padx=5, pady=5, bg="#1D2C42", fg="#ffffff")
    settings_initial_hint_text.grid(
        row=2, column=1, padx=20, pady=20, sticky="w"+"e")

    settings_initial_hint_option = Checkbutton(settings_frame, image=settings_unchecked_image,
                                               selectimage=settings_checked_image, bg="#1D2C42", variable=initial_hint, onvalue=1, offvalue=0)
    settings_initial_hint_option.select()
    settings_initial_hint_option.grid(row=2, column=2)

    # Fall speed
    settings_fall_speed_text = Label(settings_frame, text="Fall speed:", font=(
        "Courier", 30), anchor="e", padx=5, pady=5, bg="#1D2C42", fg="#ffffff")
    settings_fall_speed_text.grid(
        row=3, column=1, padx=20, pady=20, sticky="w"+"e")
    settings_fall_speed_option = OptionMenu(
        settings_frame, fall_speed, "Fast", "Medium", "Slow")
    settings_fall_speed_option.grid(row=3, column=2)

    # Enemy
    settings_enemy_text = Label(settings_frame, text="Enemy:", font=(
        "Courier", 30), anchor="e", padx=5, pady=5, bg="#1D2C42", fg="#ffffff")
    settings_enemy_text.grid(row=4, column=1, padx=20, pady=20, sticky="w"+"e")

    settings_enemy_option = Checkbutton(settings_frame, image=settings_unchecked_image,
                                        selectimage=settings_checked_image, bg="#1D2C42", variable=enemy, onvalue=1, offvalue=0)
    settings_enemy_option.select()
    settings_enemy_option.grid(row=4, column=2)

    # Numbers shown
    settings_numbers_shown_text = Label(settings_frame, text="Numbers shown:", font=(
        "Courier", 30), anchor="e", padx=5, pady=5, bg="#1D2C42", fg="#ffffff")
    settings_numbers_shown_text.grid(
        row=5, column=1, padx=20, pady=20, sticky="w"+"e")

    settings_numbers_shown_option = Checkbutton(settings_frame, image=settings_unchecked_image,
                                                selectimage=settings_checked_image, bg="#1D2C42", variable=numbers_shown, onvalue=1, offvalue=0)
    settings_numbers_shown_option.grid(row=5, column=2)

    change_button = Button(settings_frame, text="Change", padx=30, pady=15, font=(
        "Forte", 40), bg="#000000", fg="#ffffff", command=change_settings, borderwidth=5)
    change_button.grid(row=6, column=1, columnspan=2,
                       sticky="e", padx=50, pady=30)


def changeFullScreenMain(self):
    """Changes full screen state of the window"""
    if not(main.attributes("-fullscreen")):
        main.attributes("-fullscreen", True)
        return
    elif main.attributes("-fullscreen"):
        main.attributes("-fullscreen", False)
        return


def show_full_screen_instruction():
    """Shows the instruction regarding to how to quit and enter in full screen mode, including a button that hides the frame once clicked."""
    global full_screen_instruction_frame, full_screen_instruction

    # Creating frame that contains the hint
    full_screen_instruction_frame = LabelFrame(
        main, text="Hint", padx=5, pady=2, bg="#1e2022", borderwidth=0)
    full_screen_instruction_frame.place(x=0, y=300,)

    # Hint text
    full_screen_instruction = Label(full_screen_instruction_frame, text="TIP: Use ESC key to quit from/enter in full screen mode (button option available too). Game designed for full screen.",
                                    pady="10", font=("Monotype Corsiva", 25), fg="#f0f5f9", bg="#1e2022")
    full_screen_instruction.grid(row=0, column=0, sticky="W"+"E")

    # Button to continue
    finalize_full_screen_instruction_button = Button(full_screen_instruction_frame, text="CONTINUE...", font=(
        "Magneto", 30), fg="#f0f5f9", bg="#1e2022", anchor="e", command=main_buttons)
    finalize_full_screen_instruction_button.grid(row=1, column=0, stick="E")

    return


def main_buttons():
    global main_frame

    # Make hint frame disappear, although consider settings that there may be not an instruction
    main.after(500)
    try:
        full_screen_instruction_frame.place_forget()
    except NameError:
        pass

    # Creating main frame
    main_frame = LabelFrame(main, borderwidth=0)
    main_frame.place(x=0, y=0, relwidth=1, relheight=1)

    # Blurred background for main frames
    main_frame_bg = Label(main_frame, image=main_bg_image_blurred)
    main_frame_bg.place(x=0, y=0, relwidth=1, relheight=1)

    # Quit button
    quit_button = Button(main_frame, text="QUIT", padx=2, pady=1, borderwidth=3, image=quit_button_image,
                         relief="groove", font=("Monotype Corsiva", 15), fg="#f0f5f9", bg="#1e2022", command=main.quit)
    quit_button.grid(row=0, column=0, sticky="W")

    # Changing full screen mode
    change_full_screen_button = Button(main_frame, text="Change\nScreen\nMode", padx=2, pady=1, borderwidth=3, relief="groove", font=(
        "Monotype Corsiva", 15), fg="#f0f5f9", bg="#1e2022", command=lambda: changeFullScreenMain(0))
    change_full_screen_button.grid(row=0, column=0, sticky="W")
    change_full_screen_button.place(x=1295)

    # Creating main buttons frame, to place buttons
    main_buttons_frame = LabelFrame(main_frame, borderwidth=0)
    main_buttons_frame.place(x=433)

    # Background for main buttons frame
    main_buttons_frame_bg = Label(
        main_buttons_frame, image=main_buttons_frame_bg_image, borderwidth=0)
    main_buttons_frame_bg.place(x=0, y=0, relwidth=1, relheight=1)

    # Title
    main_title = Label(main_buttons_frame,
                       image=main_title_image, borderwidth=0)
    main_title.grid(row=0, column=0)

    # Introduction button
    main_introduction_button = Button(
        main_buttons_frame, image=main_introduction_image, borderwidth=0, command=introduction_page)
    main_introduction_button.grid(row=1, column=0)
    # Start Game button
    main_start_game_button = Button(
        main_buttons_frame, image=main_start_game_image, borderwidth=0, command=start_game_page)
    main_start_game_button.grid(row=2, column=0)
    # Leader board button
    main_leader_board_button = Button(
        main_buttons_frame, image=main_leader_board_image, borderwidth=0, command=leader_board_page)
    main_leader_board_button.grid(row=3, column=0)
    # Settings button
    main_settings_button = Button(
        main_buttons_frame, image=main_settings_image, borderwidth=0, command=settings_page)
    main_settings_button.grid(row=4, column=0)


# MAIN PROGRAM
main = Tk()

# Global variables
progress = 0
level = 0
start = 0
time_used = 0
continue_pause = True
initial_hint = IntVar()
fall_speed = StringVar()
enemy = IntVar()
numbers_shown = IntVar()


# Images section

# Main frame images
main_bg_image_blurred = PhotoImage(
    file="images/main_frame_images/main_bg_blurred.png")
main_buttons_frame_bg_image = PhotoImage(
    file="images/main_frame_images/main_buttons_frame_bg.png")
main_title_image = PhotoImage(
    file="images/main_frame_images/main_buttons_title.png")
main_introduction_image = PhotoImage(
    file="images/main_frame_images/main_buttons_introduction.png")
main_start_game_image = PhotoImage(
    file="images/main_frame_images/main_buttons_start_game.png")
main_leader_board_image = PhotoImage(
    file="images/main_frame_images/main_buttons_leader_board.png")
main_settings_image = PhotoImage(
    file="images/main_frame_images/main_buttons_settings.png")
quit_button_image = PhotoImage(file="images/power.png")
back_button_image = PhotoImage(file="images/back_button.png")
level_button_image = PhotoImage(file="images/game_frame_images/menuGrid.png")
home_button_image = PhotoImage(file="images/game_frame_images/home.png")
repeat_button_image = PhotoImage(file="images/game_frame_images/return.png")
unpause_button_image = PhotoImage(file="images/game_frame_images/forward.png")
boss_key_image = PhotoImage(file="images/boss_key_image.png")

# Introduction frame images
introduction_title_image = PhotoImage(
    file="images/introduction_frame_images/introduction_title.png")
introduction_information_icon_image = PhotoImage(
    file="images/introduction_frame_images/information.png")

# Game frame images
new_game_image = PhotoImage(
    file="images/game_frame_images/game_new_game_button.png")
load_game_image = PhotoImage(
    file="images/game_frame_images/game_load_game_button.png")
pause_icon_image = PhotoImage(file="images/game_frame_images/pause.png")
grass_and_soil_image = PhotoImage(
    file="images/game_frame_images/road/grass.png")
grass_image = PhotoImage(file="images/game_frame_images/road/grassWhole.png")
large_base_image = PhotoImage(
    file="images/game_frame_images/base/hangar_largeB_SE.png")
small_base_image = PhotoImage(
    file="images/game_frame_images/base/hangar_roundB_SE.png")
satellite_1_image = PhotoImage(
    file="images/game_frame_images/base/satelliteDish_detailed_SE.png")
satellite_2_image = PhotoImage(
    file="images/game_frame_images/base/satelliteDish_large_SE.png")
aircraft_cargo_image = PhotoImage(
    file="images/game_frame_images/aircraft/craft_cargoB_SE.png")
aircraft_miner_image = PhotoImage(
    file="images/game_frame_images/aircraft/craft_miner_SW.png")
rocket_image = PhotoImage(file="images/game_frame_images/base/rocket.png")
launch_rocket_image = PhotoImage(
    file="images/game_frame_images/base/rocket_launch.png")
aircraft_1_image = PhotoImage(
    file="images/game_frame_images/aircraft/craft_speederA_SE.png")
aircraft_2_image = PhotoImage(
    file="images/game_frame_images/aircraft/craft_speederB_SE.png")
aircraft_3_image = PhotoImage(
    file="images/game_frame_images/aircraft/craft_speederC_SE.png")
aircraft_4_image = PhotoImage(
    file="images/game_frame_images/aircraft/craft_speederD_SE.png")
transmitting_gate_NE_image = PhotoImage(
    file="images/game_frame_images/base/gate_complex_NE.png")
transmitting_gate_NW_image = PhotoImage(
    file="images/game_frame_images/base/gate_complex_NW.png")
transmitting_gate_SE_image = PhotoImage(
    file="images/game_frame_images/base/gate_complex_SE.png")
transmitting_gate_SW_image = PhotoImage(
    file="images/game_frame_images/base/gate_complex_SW.png")
vortex_image = PhotoImage(file="images/game_frame_images/base/vortex.png")
vortex_change_image = PhotoImage(
    file="images/game_frame_images/base/vortex_change.png")
airdrop_images = []
for i in range(10):
    airdrop_images.append(PhotoImage(
        file="images/game_frame_images/airdrop/game_airdrop_"+str(i)+".png"))

missil_image = PhotoImage(file="images/game_frame_images/aircraft/missile.png")
explosion_images = []
for i in range(9):
    explosion_images.append(PhotoImage(
        file="images/game_frame_images/explosion/explosion0"+str(i)+".png"))
enter_button_image = PhotoImage(file="images/game_frame_images/export.png")
code_box_image = PhotoImage(
    file="images/game_frame_images/base/answer_code.png")

# Leader board frame images
leader_board_title_image = PhotoImage(
    file="images/leader_board_frame_images/leader_board_title.png")
leader_board_icon_image = PhotoImage(
    file="images/leader_board_frame_images/leaderboardsComplex.png")

# Settings frame images
settings_title_image = PhotoImage(
    file="images/settings_frame_images/settings_title.png")
settings_icon_image = PhotoImage(file="images/settings_frame_images/gear.png")
settings_checked_image = PhotoImage(
    file="images/settings_frame_images/blue_boxCheckmark.png")
settings_unchecked_image = PhotoImage(
    file="images/settings_frame_images/blue_boxCross.png")
settings_bar_image = PhotoImage(
    file="images/settings_frame_images/grey_button14.png")


# Initial state of the main window
main.title("Earth Messenger")
main.geometry("1366x768")
main.attributes("-fullscreen", True)
main.iconbitmap("images/EarthMessenger_Icon.ico")

# Background
main_bg_image = PhotoImage(file="images/main_bg.png")
main_bg = Label(main, image=main_bg_image)
main_bg.place(x=0, y=0, relwidth=1, relheight=1)

# Guide on full screen, if not exist yet, go to function. Also reads the settings in data.json.
try:
    full_screen_instruction
except NameError:
    with open("data/data.json", "r") as file:
        data = json.load(file)
        if (data['initial_hint']):
            show_full_screen_instruction()
        else:
            main_buttons()

# Changing full screen mode
main.bind("<Escape>", changeFullScreenMain)
change_full_screen_button = Button(main, text="Change\nScreen\nMode", padx=2, pady=1, borderwidth=3, relief="groove", font=(
    "Monotype Corsiva", 15), fg="#f0f5f9", bg="#1e2022", command=lambda: changeFullScreenMain(0))
change_full_screen_button.grid(row=0, column=0, sticky="E")
change_full_screen_button.place(x=1295)

main.bind("<Tab>", boss_key)

# Quit from program
quit_button = Button(main, text="QUIT", padx=2, pady=1, borderwidth=3, image=quit_button_image,
                     relief="groove", font=("Monotype Corsiva", 15), fg="#f0f5f9", bg="#1e2022", command=main.quit)
quit_button.grid(row=0, column=0, sticky="W")


main.mainloop()
