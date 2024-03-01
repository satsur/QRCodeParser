import cv2
from pyzbar.pyzbar import decode
import pygame
from tkinter import Tk
from tkinter import filedialog
import numpy as np
import pyautogui
import Processor
from components.InputBox import InputBox
import Utils

QR_STRING = "ScouterName,TeamNumber,MatchNumber,AlliancePartner1,AlliancePartner2,AllianceColor,PreloadNote,NoShow,FellOver," + \
        "Leave,Park,Stage,Auton,NumberPickedUp,ScoredSpeaker,MissedSpeaker,ScoredAmp,MissedAmp,Teleop,NumberPickedUp,ScoredSpeaker," + \
        "MissedSpeaker,ScoredAmp,MissedAmp,ScoredTrap,MissedTrap"
Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
dir = filedialog.askdirectory(initialdir="C:", title="Please select a directory") # show an "Open" dialog box and return the path to the selected file
EVENT_LIST_PATH = Utils.find_files("eventList.csv", dir)
SETUP_LIST_PATH = Utils.find_files("setupList.csv", dir)
QR_STRINGS_PATH = Utils.find_files("qrStrings.txt", dir)

TITLE_FONT = pygame.font.Font("fonts/Diavlo_BOLD_II_37.otf", 32) # Title-size font
NORMAL_FONT = pygame.font.Font("fonts/Diavlo_BOLD_II_37.otf", 22) # normal text size font
SMALL_FONT = pygame.font.Font("fonts/Diavlo_BOLD_II_37.otf", 12) # small text size font
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

pygame.init()
pygame.display.set_caption("QR Code Parser - Mercury 1089")
surface = pygame.display.set_mode([SCREEN_WIDTH,SCREEN_HEIGHT])
title_surface = TITLE_FONT.render("Mercury 1089 QR Code Parser", True, pygame.Color("white"))
box_instructions_surf = NORMAL_FONT.render("Enter team numbers here:", True, pygame.Color("white"))
file_paths_surf = SMALL_FONT.render(f"Event List: {EVENT_LIST_PATH} \n" +
                                    f"Setup List: {SETUP_LIST_PATH} \n" +
                                    f"QR Strings: {QR_STRINGS_PATH}", True, pygame.color((169, 255, 115))) # Light green

# 10 pixel margins between each box (vertically and horizontally)
BOX_WIDTH = 200
BOX_HEIGHT = 50
MARGIN = 10
team_num_r1 = InputBox(0.75 * SCREEN_WIDTH - BOX_WIDTH - MARGIN, SCREEN_HEIGHT / 2 - 1.5 * BOX_HEIGHT - MARGIN, BOX_WIDTH, BOX_HEIGHT)
team_num_r2 = InputBox(0.75 * SCREEN_WIDTH - BOX_WIDTH - MARGIN, SCREEN_HEIGHT / 2 - 0.5*BOX_HEIGHT, BOX_WIDTH, BOX_HEIGHT)
team_num_r3 = InputBox(0.75 * SCREEN_WIDTH - BOX_WIDTH - MARGIN, SCREEN_HEIGHT / 2 + 0.5*BOX_HEIGHT + MARGIN, BOX_WIDTH, BOX_HEIGHT)
team_num_b1 = InputBox(0.75 * SCREEN_WIDTH, SCREEN_HEIGHT / 2 - 1.5*BOX_HEIGHT - MARGIN, BOX_WIDTH, BOX_HEIGHT)
team_num_b2 = InputBox(0.75 * SCREEN_WIDTH, SCREEN_HEIGHT / 2 - 0.5*BOX_HEIGHT, BOX_WIDTH, BOX_HEIGHT)
team_num_b3 = InputBox(0.75 * SCREEN_WIDTH, SCREEN_HEIGHT / 2 + 0.5*BOX_HEIGHT + MARGIN, BOX_WIDTH, BOX_HEIGHT)

team_number_boxes = [team_num_r1, team_num_r2, team_num_r3, team_num_b1, team_num_b2, team_num_b3]

#0 Is the built in camera
cap = cv2.VideoCapture(0)
#Gets fps of your camera    
fps = cap.get(cv2.CAP_PROP_FPS)
print("fps:", fps)
# If your camera can achieve 60 fps
# Else just have this be 1-30 fps
cap.set(cv2.CAP_PROP_FPS, 60)

while True:
    surface.fill([51,51,51])

    # Get frame from video
    success, frame = cap.read()
    if not success:
        break

    ''' 
    Process Frame - Detect and decode QR Code from frame
    '''
    decoded_info = decode(frame)
    print(decoded_info)

    if (len(decoded_info) > 1): # Don't want to scan two QR codes at once
        pyautogui.alert("Make sure there isn't more than ONE QR Code on screen at once!")

    # If QR code has been scanned, process and write to file, update boxes as needed
    if (len(decoded_info) > 0):
        print("Decoded info: " + str(decoded_info))
        # data is type "bytes" by default, use decode("utf-8") to convert to string
        qr_string = decoded_info[0].data.decode("utf-8")
        print("QR String: " + qr_string)
        # Write strings to respective lists
        Processor.write_to_event_list(EVENT_LIST_PATH, qr_string)
        Processor.write_to_setup_list(SETUP_LIST_PATH, qr_string)
        Processor.write_full_str(QR_STRINGS_PATH, qr_string)

        team_number = Processor.get_team_number(qr_string)
        num_in_boxes = False
        for box in team_number_boxes:
            if team_number == box.text.strip():
                num_in_boxes = True
                if box.completed:
                    pyautogui.alert("A QR code has already been submitted with this team number.")
                    break
                box.completed = True
                break
        if not num_in_boxes:
             pyautogui.alert("Team number does not match up to list. Make sure the boxes and QR code have the right information.")
            
    

    # Flip image because the frames appeared inverted by default
    frame = np.fliplr(frame)
    frame = np.rot90(frame)

    # The capture uses BGR colors and PyGame needs RGB
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    surf = pygame.surfarray.make_surface(frame)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        for box in team_number_boxes:
                box.handle_event(event)

    count_completed = 0
    # Show each box, count if completed
    for box in team_number_boxes:
        if box.completed:
            count_completed += 1
        box.update()
        box.draw(surface)

    if count_completed == len(team_number_boxes):
        for box in team_number_boxes:
            box.text = ''
            box.completed = False

    # Show the webcam capture surface!
    surface.blit(surf, (20 , SCREEN_HEIGHT / 2 - surf.get_height() / 2))
    # Show title and instructions
    surface.blit(title_surface, (SCREEN_WIDTH / 2 - title_surface.get_width() / 2, 20))
    surface.blit(box_instructions_surf, (team_num_r1.rect.x, team_num_r1.rect.y - box_instructions_surf.get_height()-10))
    surface.blit(file_paths_surf, (20, SCREEN_HEIGHT - 3 * file_paths_surf.get_height()))
    pygame.display.flip()