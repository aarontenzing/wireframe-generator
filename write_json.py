import json
import numpy 

def write(rectangle, shot, whd, world_coordinates, projection_coordinates, center):
    
    # data written to csv
    data = {
                "image" : rectangle,
                "shot"  : shot,
                "whd"   : whd,
                "world" : world_coordinates,
                "projection" : projection_coordinates,
                "center" : center
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
    # Open a JSON file in write mode (creates the file if it doesn't exist)
    with open("annotations.json", "w") as file:
        # Use the `truncate()` method to clear the file's content
        file.truncate()
