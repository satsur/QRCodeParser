# Writes setup portion of qr string to setupList.csv
def write_to_setup_list(path:str, full_str:str):
    str_arr = full_str.split(",")
    str_arr = str_arr[:str_arr.index("Auton")]
    setup_str = ",".join([data for data in str_arr])
    with open(path, 'a') as file:
        file.write(setup_str + "\n")

# Writes first three fields (name, match, team) and scoring data to eventList.csv
def write_to_event_list(path:str, full_str:str):
    str_arr = full_str.split(",")
    match_data_start = str_arr.index("Auton")
    # print("Array from QR String: " + str(str_arr))
    full_str = ",".join(str_arr[:3] + str_arr[match_data_start:])
    with open(path, 'a') as file:
        file.write(full_str + "\n")

def write_full_str(path:str, full_str:str):
    with open(path, 'a') as file:
        file.write(full_str + "\n")

def replace_last_entry(paths:list, new_str:str):
    for path in paths:
        with open(path, 'r') as file:
            lines = file.readlines()
        lines = lines[:-1].append(new_str)
        with open(path, 'w') as write_file:
            write_file.write(line + '\n' for line in lines)

def get_team_number(full_str:str) -> str:
    return full_str.split(",")[1]