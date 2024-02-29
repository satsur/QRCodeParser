import cv2
import pygame
import numpy as np
import pyautogui
from components.InputBox import InputBox

QR_STRING = "ScouterName,TeamNumber,MatchNumber,AlliancePartner1,AlliancePartner2,AllianceColor,PreloadNote,NoShow,FellOver," + \
        "Leave,Park,Stage,Auton,NumberPickedUp,ScoredSpeaker,MissedSpeaker,ScoredAmp,MissedAmp,Teleop,NumberPickedUp,ScoredSpeaker," + \
        "MissedSpeaker,ScoredAmp,MissedAmp,ScoredTrap,MissedTrap"
EVENT_LIST_PATH = "eventList.csv"
SETUP_LIST_PATH = "setupList.csv"
QR_STRINGS_PATH = "qrStrings.txt"

pygame.init()
pygame.display.set_caption("QR Code Parser - Mercury 1089")
surface = pygame.display.set_mode([1280,720])

scouter_name_1 = InputBox(800, 200, 200, 50)
scouter_name_2 = InputBox(800, 250, 200, 50)
scouter_name_3 = InputBox(800, 300, 200, 50)
scouter_name_4 = InputBox(800, 350, 200, 50)
scouter_name_5 = InputBox(800, 400, 200, 50)
scouter_name_6 = InputBox(800, 450, 200, 50)
scouter_name_boxes = [scouter_name_1, scouter_name_2, scouter_name_3, scouter_name_4, scouter_name_5,scouter_name_6]

#0 Is the built in camera
cap = cv2.VideoCapture(0)
#Gets fps of your camera    
fps = cap.get(cv2.CAP_PROP_FPS)
print("fps:", fps)
#If your camera can achieve 60 fps
#Else just have this be 1-30 fps
cap.set(cv2.CAP_PROP_FPS, 60)

while True:
    surface.fill([255,255,255])

    # Get frame from video
    success, frame = cap.read()
    if not success:
        break

    ''' 
    Process Frame - Detect and decode QR Code from frame
        retval:          True if QR Code is detected
        decoded_info:    tuple containing QR Code content in each QR code detected
        points:          numpy.ndarray of coordinates on screen of four corners of QR code
        straight_qrcode: tuple of binary values of 0 and 255 representing the black and white of each cell of the QR code.
    '''
    qcd = cv2.QRCodeDetector()
    retval, decoded_info, points, straight_qrcode = qcd.detectAndDecodeMulti(frame)
    print(f"Info: {decoded_info}") 

    if (len(decoded_info) > 1): # Don't want to scan two QR codes at once
        pyautogui.alert("Make sure there isn't more than ONE QR Code on screen at once!")

    # QR code has been scanned, now process and write to file: 
        

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
        for box in scouter_name_boxes:
                box.handle_event(event)

    for box in scouter_name_boxes:
        box.update()
        box.draw(surface)

    # Show the PyGame surface!
    surface.blit(surf, (0,0))
    pygame.display.flip()