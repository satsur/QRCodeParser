import os

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