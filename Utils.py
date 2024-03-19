import os

DIGITS = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

def find_files(filename, search_path):
   result = []

# Walking top-down from the root
   for root, directory, files in os.walk(search_path):
      if filename in files:
         result.append(os.path.join(root, filename))
   if len(result) > 0:
      return result[0]
   else:
      return None
   

def char_is_digit(str_num):
   return str_num in DIGITS