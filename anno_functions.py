

def get_coordinates(self, modelview_matrix, projection_matrix, viewport):
    world_coordinates = []
    projection_coordinates = []
    center_coordinates = [] # consists of 2 elements: world and projection coordinates
    # loop through rectangle vertices
    for vertex in self.rectangle.vertices:
            
        vertex_new = vertex + (0,)  # tuple had only 3 elements
        transformed_vertex_world = [0,0,0,0]
        transformed_vertex_projection = [0,0,0,0]
            
        # apply model-view matrix
        for i in range(4):
            for j in range(4):
                transformed_vertex_world[i] += float(modelview_matrix[i][j] * vertex_new[j])
                    
        # apply projection matrix -> those are normalized
        for i in range(4):
            for j in range(4):
                transformed_vertex_projection[i] += float(projection_matrix[i][j] * vertex_new[j])
                screen_x, screen_y = convert_projected_to_screen(transformed_vertex_projection[0], transformed_vertex_projection[1], viewport)
            
         
        world_coordinates.append(tuple(transformed_vertex_world[:3]))
        projection_coordinates.append((screen_x, screen_y))
            
    # center calculation 
    tmp = world_coordinates[0]
    x, y, z = tmp[0], tmp[1], tmp[2]
    x = x-self.rectangle.width
    y = y-self.rectangle.height
    z = z-self.rectangle.depth
    center_coordinates.append((x,y,z))
    convert_projected_to_screen(x, y, viewport)
    center_coordinates.append((screen_x, screen_y)) 

def convert_projected_to_screen(proj_x, proj_y, viewport):
    screen_x = int((1 + proj_x) * viewport[2] / 2 )
    screen_y = int((1 - proj_y) * viewport[3] / 2 )
    print(screen_x, screen_y)
    return screen_x, screen_y