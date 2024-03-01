# Writes setup portion of qr string to setupList.csv
def write_to_setup_list(path:str, full_str:str):
    str_arr = full_str.split(",")
    str_arr = str_arr[:str_arr.index("Auton")]
    # [:-1] removes ending comma
    setup_str = ",".join([data for data in str_arr])[:-1]
    with open(path, 'w') as file:
        file.write(setup_str + "\n")

# Writes first three fields (name, match, team) and scoring data to eventList.csv
def write_to_event_list(path:str, full_str:str):
    str_arr = full_str.split(",")
    match_data_start = str_arr.index("Auton")
    # [:-1] removes ending comma
    print("Array from QR String: " + str(str_arr))
    full_str = ",".join(str_arr[:3] + str_arr[match_data_start:])[:-1]
    with open(path, 'a') as file:
        file.write(full_str + "\n")

def write_full_str(path:str, full_str:str):
    with open(path, 'a') as file:
        file.write(full_str + "\n")

def get_team_number(full_str:str) -> str:
    return full_str.split(",")[1]

