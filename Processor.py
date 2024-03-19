import ConfigManager

# Strip comma from end if necessary
def strip_commas(full_str:str) -> str:
    while full_str[-1] == ",":
        full_str = full_str[:-1]
    return full_str

# Get file paths from config
def get_file_paths():
    return [val for key,val in ConfigManager.get_config("paths")]

# Writes setup portion of qr string to setupList.csv
def write_to_setup_list(path:str, full_str:str):
    str_arr = strip_commas(full_str).split(",")
    str_arr = str_arr[:str_arr.index("Auton")]
    setup_str = ",".join([data for data in str_arr])
    with open(path, 'a') as file:
        file.write(setup_str + "\n")

# Writes first three fields (name, match, team) and scoring data to eventList.csv
def write_to_event_list(path:str, full_str:str):
    str_arr = strip_commas(full_str).split(",")
    match_data_start = str_arr.index("Auton")
    # print("Array from QR String: " + str(str_arr))
    full_str = ",".join(str_arr[:3] + str_arr[match_data_start:])
    with open(path, 'a') as file:
        file.write(full_str + "\n")

def write_full_str(path:str, full_str:str):
    with open(path, 'a') as file:
        file.write(strip_commas(full_str) + "\n")

def replace_last_entry(new_str:str):
    paths = get_file_paths()
    for path in paths:
        with open(path, 'r+') as file:
            print(path)
            lines = file.readlines()
            print("oldlines: " + str(lines))
            # Make sure not to delete the headers
            if len(lines) > 1:
                lines = lines[:-1]
            file.seek(0)
            file.truncate()
            print("newlines: " + str(lines))
            for line in lines:
                file.write(line)
    # 0: qrStrings, 1: eventList, 2: setupList
    write_full_str(paths[0], new_str)
    write_to_event_list(paths[1], new_str)
    write_to_setup_list(paths[2], new_str)

def get_team_number(full_str:str) -> str:
    return full_str.split(",")[1]

def get_match_number(full_str:str) -> str:
    return full_str.split(",")[2]