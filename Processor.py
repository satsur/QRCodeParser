import ConfigManager

# Strip comma from end if necessary
def strip_commas(full_str:str) -> str:
    while full_str[-1] == ",":
        full_str = full_str[:-1]
    return full_str

# Get file paths from config
def get_data_file_path():
    return ConfigManager.get_config('paths')['qr_strings']

def write_full_str(path:str, full_str:str):
    with open(path, 'a') as file:
        file.write(strip_commas(full_str) + "\n")

def replace_last_entry(new_str:str):
    paths = get_data_file_path()
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

def get_team_number(full_str:str) -> str:
    return full_str.split(",")[1]

def get_match_number(full_str:str) -> str:
    return full_str.split(",")[2]

# Make sure qr string is a csv value and contains "Auton" and "Teleop" (should be in all strings regardless of that year's game)
def is_correct_format(full_str:str) -> bool:
    values = full_str.split(',')
    return len(values) > 0 and "Auton" in values and "Teleop" in values