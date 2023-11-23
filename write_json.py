import json
import numpy 

def write(rectanlge, world_coordinates, projection_coordinates, center, rotation):
    

    # data written to csv
    data = {"image" : rectanlge,
            "world" : world_coordinates,
            "projection" : projection_coordinates,
            "center" : center, 
            "rotation" : rotation}
    
    with open("annotations.json", "r") as file:
        try:
            file_data = json.load(file) # file content to python list
        except json.decoder.JSONDecodeError:
                file_data = []
                print("file empty")
    
    file_data.append(data) 
    
    with open("annotations.json", 'w') as file:
        json.dump(file_data, file) # dict to array (json)   