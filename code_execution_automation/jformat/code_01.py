# This code is referent to the sequence of notebooks of the click library in python. The specific notebook is click_library_python.ipynb.

# import libratys
import json
import os
import sys
import argparse    # library to set args to the program in the code lines

def formatter(string, sort_keys=True, indent=4):
  # print the string before the treatment
  print(string)
  # load the json
  json_obj = json.loads(string)
  # print the string after the treatment, in the dump (persist) process
  print(json.dumps(json_obj, sort_keys=sort_keys, indent=2))

# Lendo um arquivo
def main(path):
    with open(path) as _f:
        string = _f.read()
        formatter(string)


if __name__ == "__main__":
    # do 2 processes, i) create a json on the path, ii) run the main function to process the json

    # Persist a json on the path
    # print the current path
    curr_path = os.getcwd()
    print(curr_path)
    json_obj = {"name": "history", "content": "Once upon a time that was a grorious Empire"}
    # the json file where the output must be stored 
    file_name = "/myfile.json" 
    with open(curr_path + file_name, 'w') as f:
        json.dump(json_obj, f)

    # check to see if the json is on the path
    print(os.listdir())

    # Call the funtion
    # The arg to pass in the command line is the path where the json is saved. Equal to current path + filename
    main(sys.argv[-1])
    # This line of code print the correct path. Remove the comment to check before pass in the command line
    # print(curr_path + file_name)

