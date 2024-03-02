import os

def find_files(filename, search_path):
   result = []

# Walking top-down from the root
   for root, directory, files in os.walk(search_path):
      if filename in files:
         result.append(os.path.join(root, filename))
   return result[0]