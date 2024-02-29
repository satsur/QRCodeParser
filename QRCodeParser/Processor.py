# Writes setup portion of qr string to setupList.csv
def write_to_setup_list(path, full_str):
    str_arr = full_str.split(",")
    str_arr = str_arr[:str_arr.index("Auton")]
    setup_str = "".join([data + "," for data in str_arr])[:-1]
    with open(path, 'w') as file:
        file.write(setup_str)

# Writes first three fields (name, match, team) and scoring data to eventList.csv
def write_to_event_list(path, full_str):
    str_arr = full_str.split(",")
    full_str = str_arr[:3] + str_arr[str_arr.index("Auton"):]
    with open(path, 'w') as file:
        file.write(full_str)

def get_name(full_str) -> str:
    return full_str.split(",")[0]

