import json
import numpy 

def write_json(rectangle, shot, whd, world_coordinates, projection_coordinates, center, valid):
    
    # data written to csv
    data = {
                "image" : rectangle,
                "shot"  : shot,
                "whd"   : whd,
                "world" : world_coordinates,
                "projection" : projection_coordinates,
                "center" : center,
                "valid" : valid
            }
    
    with open("annotations.json", "r") as file:
        try:
            file_data = json.load(file) # file content to python list
        except json.decoder.JSONDecodeError:
                file_data = []
                print("file empty")
    
    file_data.append(data) 
    
    with open("annotations.json", 'w') as file:
        json.dump(file_data, file, indent=2) # dict to array (json)   
        

def clear_json():
    # clear the json file 
    with open("annotations.json", "w") as file:
        file.truncate()
