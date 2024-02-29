QR_STRING = "ScouterName,TeamNumber,MatchNumber,AlliancePartner1,AlliancePartner2,AllianceColor,PreloadNote,NoShow,FellOver," + \
        "Leave,Park,Stage,Auton,NumberPickedUp,ScoredSpeaker,MissedSpeaker,ScoredAmp,MissedAmp,Teleop,NumberPickedUp,ScoredSpeaker," + \
        "MissedSpeaker,ScoredAmp,MissedAmp,ScoredTrap,MissedTrap"

# Writes setup portion of qr string to setupList.csv
def write_to_setup_list(path, full_str):
    str_arr = full_str.split(",")
    str_arr = str_arr[:str_arr.index("Auton")]
    setup_str = "".join([data + "," for data in str_arr])[:-1]
    with open(path, 'w') as file:
        file.write(setup_str)

def write_to_event_list(path, full_str):
    with open(path, 'w') as file:
        file.write(full_str)

write_to_setup_list("setupList.csv", QR_STRING)