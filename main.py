import cv2
from pyzbar.pyzbar import decode
import pygame
from tkinter import Tk
import tkinter
import tkinter.filedialog
import tkinter.messagebox
import tkinter.simpledialog
import numpy as np
import Processor
from components.InputBox import InputBox
from components.Button import Button
import Utils
import ConfigManager
import api.RequestHandler as RequestHandler
import time
import os

pygame.init()
ConfigManager.load_config()

# ----------------- CONSTANTS -----------------

APP_NAME = "QR Code Parser - Mercury 1089"
QR_STRING = "TeamNumber, MatchNumber, AlliancePartner1, AlliancePartner2, AllianceColor, Preload, NoShow, FellOver, Leave, Defense, Park, Hang, " \
    "AUTON, CORAL, L4ScoredCoral, L3ScoredCoral, L2ScoredCoral, L1ScoredCoral, L4MissedCoral, L3MissedCoral, L2MissedCoral, L1MissedCoral, PickedUpCoral, " \
        "ALGAE, L3RemovedAlgae, L2RemovedAlgae, L3FailedAlgae, L2FailedAlgae, ScoredProcessor, MissedProcessor, ScoredNet, MissedNet, PickedUpAlgae, "\
    "TELEOP, CORAL, L4ScoredCoral, L3ScoredCoral, L2ScoredCoral, L1ScoredCoral, L4MissedCoral, L3MissedCoral, L2MissedCoral, L1MissedCoral, PickedUpCoral, " \
        "ALGAE, L3RemovedAlgae, L2RemovedAlgae, L3FailedAlgae, L2FailedAlgae, ScoredProcessor, MissedProcessor, ScoredNet, MissedNet, PickedUpAlgae, ScouterName"
APP_BG_COLOR = pygame.Color((51,51,51))
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 30
FPS_CLOCK = pygame.time.Clock()

# ----------------- DISPLAY SURFACE -----------------
surface = pygame.display.set_mode([SCREEN_WIDTH,SCREEN_HEIGHT])

# ----------------- CHOOSING FILE DIRECTORY -----------------
last_path = ConfigManager.get_config()['last_path']
result = tkinter.messagebox.askquestion(title=APP_NAME, message=f'Would you like to use {last_path} again?')
if result == tkinter.messagebox.YES:
    dir = last_path
else:
    Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
    # show an "Open" dialog box and return the path to the selected file
    STRAT_FOLDER = "C:\\Users\\Mercury1089\\Desktop\\Strategy\\2025 Reefscape"
    dir = tkinter.filedialog.askdirectory(initialdir=STRAT_FOLDER, title="Please select the directory that contains eventList, setupList, and qr_strings")
QR_STRINGS_PATH = Utils.find_files("qrStrings.txt", dir)

# Add paths to config
if  QR_STRINGS_PATH != None:
    ConfigManager.set_config('last_path', dir)
    ConfigManager.set_config("paths", {"qr_strings": QR_STRINGS_PATH})
else:
    tkinter.messagebox.askokcancel(title=APP_NAME, message="Please select a directory that contains the necessary files (eventList.csv, setupList.csv, qrStrings.txt).")
    pygame.quit()
    exit()

# ----------------- FONT DETAILS -----------------
TITLE_FONT = pygame.font.Font("fonts/Diavlo_BOLD_II_37.otf", 32) # Title-size font
NORMAL_FONT = pygame.font.Font("fonts/ChakraPetch-Bold.ttf", 22) # normal text size font
SMALL_FONT = pygame.font.Font("fonts/Sintony-Bold.ttf", 13) # small text size font
FONT_COLOR = pygame.Color((255,150,0))

# ----------------- SCREEN ELEMENTS/SURFACES -----------------
pygame.display.set_caption(APP_NAME)
title_surface = TITLE_FONT.render("Mercury 1089 QR Code Parser", True, pygame.Color("white"))

qr_strings_surf = SMALL_FONT.render(f"QR STRINGS: {QR_STRINGS_PATH}", True, FONT_COLOR)

# 10 pixel margins between each box (vertically and horizontally)
BOX_WIDTH = 200
BOX_HEIGHT = 50
MARGIN = 10

match_num_text_surf = NORMAL_FONT.render("Match: ", True, pygame.Color("white"))
match_num_input_box = InputBox(0.75*SCREEN_WIDTH, SCREEN_HEIGHT/4, BOX_WIDTH/2, BOX_HEIGHT, completable=False)
box_instructions_surf = NORMAL_FONT.render("Enter team numbers here:", True, pygame.Color("white"))
team_num_r1 = InputBox(0.75 * SCREEN_WIDTH - BOX_WIDTH - MARGIN, SCREEN_HEIGHT / 2 - 1.5 * BOX_HEIGHT - MARGIN, BOX_WIDTH, BOX_HEIGHT)
team_num_r2 = InputBox(team_num_r1.rect.x, team_num_r1.rect.y+BOX_HEIGHT+MARGIN, BOX_WIDTH, BOX_HEIGHT)
team_num_r3 = InputBox(team_num_r1.rect.x, team_num_r2.rect.y+BOX_HEIGHT+MARGIN, BOX_WIDTH, BOX_HEIGHT)
team_num_b1 = InputBox(team_num_r1.rect.x + BOX_WIDTH+MARGIN, team_num_r1.rect.y, BOX_WIDTH, BOX_HEIGHT)
team_num_b2 = InputBox(team_num_b1.rect.x, team_num_r2.rect.y, BOX_WIDTH, BOX_HEIGHT)
team_num_b3 = InputBox(team_num_b1.rect.x, team_num_r3.rect.y, BOX_WIDTH, BOX_HEIGHT)

clear_button = Button("clear", team_num_r1.rect.x, team_num_r3.rect.y+BOX_HEIGHT+MARGIN, BOX_WIDTH, BOX_HEIGHT, "Clear")
# GET TEAMS fills in team data from the STORED match data
get_teams_button = Button("get_teams", team_num_b1.rect.x, team_num_b3.rect.y+BOX_HEIGHT+MARGIN, BOX_WIDTH, BOX_HEIGHT, "Get Teams")
# LOAD TEAMS fetches event match data from TheBlueAlliance API and stores in locally
load_teams_button = Button("load_teams", 10, 10, BOX_WIDTH, BOX_HEIGHT, "Load Teams")
reload_config_button = Button("reload_config", SCREEN_WIDTH-BOX_WIDTH-10, 10, BOX_WIDTH, BOX_HEIGHT, "Reload Config")

last_string_text = NORMAL_FONT.render("No QR code has been scanned", True, FONT_COLOR)
edit_button = Button("edit", 0.75 * SCREEN_WIDTH - BOX_WIDTH/2, 
                     clear_button.rect.y + BOX_HEIGHT + MARGIN,
                     BOX_WIDTH,
                     BOX_HEIGHT,
                     "Edit!", 
                     SMALL_FONT)

team_number_boxes = [team_num_r1, team_num_r2, team_num_r3, team_num_b1, team_num_b2, team_num_b3]
input_boxes = team_number_boxes + [match_num_input_box]
# Reminder to add edit_button and load_teams_button back, removed it for competition because of bugs
buttons = [clear_button, edit_button, load_teams_button, get_teams_button, reload_config_button]

focused = True

# ----------------- VIDEO CAPTURE -----------------
# 0 Is the built in camera, change to 1 if using webcam
cap = cv2.VideoCapture(0)
print(cap.read())
# Gets fps of your camera
fps = cap.get(cv2.CAP_PROP_FPS)
print("fps:", fps)
# If your camera can achieve 60 fps
# Else just have this be 1-30 fps
cap.set(cv2.CAP_PROP_FPS, 60)

# ----------------- "GAME" LOOP -----------------
match_number = 1
last_scan_time = 0
qr_string = None

while True:
    surface.fill(APP_BG_COLOR)

    frame = np.array([])
    # Get frame from video
    if focused:
        success, frame = cap.read()
        if not success:
            break
 
    # Process Frame - Detect and decode QR Code from frame
    decoded_info = decode(frame) if frame.size > 0 else []
    # print(decoded_info)

    if (len(decoded_info) > 1): # Don't want to scan two QR codes at once
        tkinter.messagebox.showwarning(title=APP_NAME, message="Make sure there isn't more than ONE QR Code on screen at once!")

    # If QR code has been scanned, process and write to file, update boxes as needed
    if (len(decoded_info) > 0):
        # 2 second cooldown between scans to hopefully prevent freezing/crashing
        now = time.time()
        if now - last_scan_time > 2:
            last_scan_time = now
        else:
            continue
        # print("Decoded info: " + str(decoded_info))
        # data is type "bytes" by default, use decode("utf-8") to convert to string
        qr_string = decoded_info[0].data.decode("utf-8")
        # print("QR String: " + qr_string)

        # If QR code is not in the right format (e.g. someone scans an external QR code), display an error & skip processing (so it doesn't crash)
        if not Processor.is_correct_format(qr_string):
            tkinter.messagebox.showwarning(title="AHHHHHHHHHHHHHHHHH", message=f"AHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH\n    "\
                                           "That's not the right QR code... \n" \
                                            "Please see your nearest strategy member for servicing :D")
            continue

        qr_string_team_number = Processor.get_team_number(qr_string)
        qr_string_match_num = Processor.get_match_number(qr_string)
        num_in_boxes = False
        duplicate_string = False
        for box in team_number_boxes:
            if qr_string_team_number == box.text.strip() and qr_string_match_num == str(match_number):
                # Do not let the same box be scanned twice
                if box.completed:
                    tkinter.messagebox.showerror(title=APP_NAME, message="A QR code has already been submitted with this team number.")
                    duplicate_string = True
                else:
                    Processor.write_full_str(QR_STRINGS_PATH, qr_string)
                    box.completed = True
                    # Show last scanned string 
                    last_string_text = NORMAL_FONT.render(qr_string, True, FONT_COLOR)
                num_in_boxes = True
        if num_in_boxes and not duplicate_string:
            tkinter.messagebox.showinfo(title=APP_NAME, message=f"Successfully scanned code for Team Number {qr_string_team_number}")
        elif not num_in_boxes:
             tkinter.messagebox.showerror(title=APP_NAME, 
                                          message="Team or match number do not match up to list. Make sure the boxes and QR code have the right information.")

    # ----------------- CREATING WEBCAM SURFACE -----------------
             
    # Flip image because the frames appeared inverted by default
    if focused:
        frame = np.fliplr(frame)
        frame = np.rot90(frame)

        # The capture uses BGR colors and PyGame needs RGB
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        webcam_surf = pygame.surfarray.make_surface(frame)

    # ----------------- EVENT LISTENERS -----------------

    for event in pygame.event.get():
        # Window close
        if event.type == pygame.QUIT:
            ConfigManager.write_config()
            pygame.quit()
            exit()
        if event.type == pygame.ACTIVEEVENT:
            if event.state == 2: # means focus changed
                focused = event.gain # 1 = focus gained, 0 = focus lost
        if event.type == pygame.KEYDOWN:
            # press TAB or ENTER
            if event.key == pygame.K_TAB or event.key == pygame.K_RETURN:
                for i in range(len(team_number_boxes)):
                    if team_number_boxes[i].active:
                        team_number_boxes[i].active = False
                        # If the current box is not the last box
                        if (i < len(team_number_boxes)-1):
                            team_number_boxes[i+1].active = True
                        # Current box is the last box, so it loops back to the first box
                        else:
                            team_number_boxes[0].active = True
                        break

        # All input box event handlers (typing)
        for box in input_boxes:
            box.handle_event(event)

        # All button event handlers (click, hover, etc.)
        for button in buttons:
            button.handle_event(event)
            
            # CLEAR BUTTON
            if button.name == "clear" and button.active:
                button.active = False
                for box in team_number_boxes:
                    box.text = ''
                    box.completed = False

            # EDIT BUTTON
            if button.name == "edit" and button.active:
                if qr_string == None:
                    tkinter.messagebox.showerror(title=APP_NAME, message="No QR code has been scanned!")
                else:
                    edit_prompt = tkinter.simpledialog.askstring(title=APP_NAME, prompt='Edit the string and click OK.', initialvalue=qr_string)
                    if edit_prompt != None:
                        Processor.replace_last_entry(edit_prompt)
                        button.active = False
            if button.name == "load_teams" and button.active:
                button.active = False
                event_key = ConfigManager.get_config()["event_key"]
                if event_key is None:
                    event_key = tkinter.simpledialog.askstring(title=APP_NAME, prompt="Please enter the event key (including the year)")
                else:
                    yesno = tkinter.messagebox.askyesno(title=APP_NAME, message=f"Would you like to use the event key {event_key} again?")
                    if yesno == False:
                        event_key = tkinter.simpledialog.askstring(title=APP_NAME, prompt="Please enter the event key (including the year)")
                        if event_key is None:
                            break
                try:
                    match_data = RequestHandler.load_match_data_from_api(event_key)
                except Exception as e:
                    print(e)
                    tkinter.messagebox.showerror(title=APP_NAME, message=f"Unable to connect. Make sure you have a stable internet connection.")
                    break
                if match_data is None:
                    tkinter.messagebox.showerror(title=APP_NAME, message=f"The event key '{event_key}' is invalid.")
                    break
                try:
                    RequestHandler.store_matches(match_data)
                    ConfigManager.set_config("event_key", event_key)
                except IndexError:
                    tkinter.messagebox.showerror(title=APP_NAME, message="Match data doesn't seem to exist for the given event. \n"\
                                                 "This may mean that the match schedule has not been released on TBA. Please try again later")
                else:
                    tkinter.messagebox.showinfo(title=APP_NAME, message=f"Data for event {event_key} has been fetched and stored.")

            # GET TEAMS BUTTON
            if button.name == "get_teams" and button.active:
                button.active = False
                event_key = ConfigManager.get_config()["event_key"]
                event_data = RequestHandler.get_stored_match_data(event_key)
                if event_data is None:
                    stored_event_key = RequestHandler.get_stored_event_key()
                    tkinter.messagebox.showerror(title=APP_NAME, message=f"Event key and event data don't match. \n" \
                                                    f"Config event key: {event_key}.\n" \
                                                    f"Stored event data: {stored_event_key} \n" \
                                                    f"If you have access to the Internet, press the 'Load Teams' button to get data for the desired competition. ")
                    break
                teams_in_match = RequestHandler.get_teams_in_match(event_data, match_number, RequestHandler.MatchTypes.QUALIFICATION)
                if teams_in_match is None:
                    tkinter.messagebox.showerror(title=APP_NAME, message="No teams exist for that match.")
                    break
                for i in range(len(team_number_boxes)):
                    team_number_boxes[i].completed = False
                    if i < 3:
                        team_number_boxes[i].text = teams_in_match["red"][i]
                    else:
                        team_number_boxes[i].text = teams_in_match["blue"][i-3]
                ConfigManager.set_config("event_key", event_key)
            
            # RELOAD CONFIG BUTTON - Will overwrite file directory in config stored in memory (file won't be updated with new dir upon close)
            # If you make changes to the file while the program is running, you must reload config for it to update in memory
            if button.name == "reload_config" and button.active:
                button.active = False
                # Yes = True, No = False
                warning = tkinter.messagebox.askyesno(title=APP_NAME, message=f"Reloading configuration will overwrite the file directory stored in memory. \n" \
                                               + "Press 'Yes' to continue.", icon=tkinter.messagebox.WARNING)
                if warning:
                    ConfigManager.load_config() # Loads config from config.yml into memory
        FPS_CLOCK.tick(FPS)
    # ----------------- DISPLAY (BLIT) ELEMENTS ON SCREEN -----------------
    
    count_completed = 0
    # Show each box, count if completed
    for box in team_number_boxes:
        if box.completed:
            count_completed += 1
        box.update()
        box.draw(surface)
    match_num_input_box.update()
    match_num_input_box.draw(surface)

    match_num_text = match_num_input_box.text.strip()
    num = int(match_num_text) if match_num_text != "" else 0
    if match_num_text != str(match_number):
        match_number = int(match_num_text) if match_num_text != "" else 0

    if count_completed == len(team_number_boxes):
        for box in team_number_boxes:
            box.text = ''
            box.completed = False
            match_num_input_box.text = str(num + 1)

    # Show the webcam capture surface!
    if focused:
        surface.blit(webcam_surf, (20 , SCREEN_HEIGHT / 2 - webcam_surf.get_height() / 2))
    # Show title and instructions
    surface.blit(title_surface, (SCREEN_WIDTH / 2 - title_surface.get_width() / 2, 20))
    surface.blit(match_num_text_surf, (match_num_input_box.rect.x - match_num_text_surf.get_width(), match_num_input_box.rect.y + match_num_input_box.rect.height/2))
    surface.blit(box_instructions_surf, (team_num_r1.rect.x, team_num_r1.rect.y - box_instructions_surf.get_height()-10))
    # Display file paths in bottom left
    surface.blit(qr_strings_surf, (20, SCREEN_HEIGHT - 1 * qr_strings_surf.get_height() - 10))
    # Display box for editing the last scanned qr string
    surface.blit(last_string_text, (0.5 * SCREEN_WIDTH - last_string_text.get_width()/2, 0.85 * SCREEN_HEIGHT + 10))
    # Show buttons
    for button in buttons:
        button.update()
        button.draw(surface)
    pygame.display.flip()