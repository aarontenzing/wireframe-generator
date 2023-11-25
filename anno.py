import pygame as pg
from pygame import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import random
from rectangle import RectangleMesh
from write_json import write, clear_json

class App:

    def __init__(self):

        # initialize pygame for GUI
        pg.init() 
        self.display = (512,512)
        self.screen = pg.display.set_mode(self.display, pg.OPENGL|pg.DOUBLEBUF) # tell pygame we run OPENGL & DOUBLEBUFFERING, one frame vis & one drawing
        pg.display.set_caption("Wireframe generator")
        
        # activation variables 
        self.axes = 0
        self.screenshot = 1
        clear_json()
        
        # initialize OpenGL
        glClearColor(0,0,0,1)
        
        glMatrixMode(GL_PROJECTION) # activate projection matrix
        gluPerspective(45, self.display[0]/self.display[1], 0.1, 50)
        
        # draw wired rectangle
        self.rectangle = RectangleMesh(1, 1, 1, [0,0,0], [0,0,-20]) 
        self.rectangle.draw_wired_rect()
        
        self.mainLoop()

    def mainLoop(self):
        rect_name = 1  
        img_number = 1 # counts the rectangle that is been shown
        img_shot = 1 # counts how many screenshots were taken
        
        running = True
        while(running):
            # Check for events
            for event in pg.event.get():
                
                if (event.type == pg.QUIT):
                    running = False
                    
                if (event.type == KEYDOWN) and (event.key == K_s):
                    # enable screenshots
                    self.screenshot = not self.screenshot 
                
                if (event.type == KEYDOWN) and (event.key == K_a):
                    # draw axes
                    self.axes = not self.axes
                    
                if (event.type == KEYDOWN) and (event.key == K_p):
                    # draw axes
                    print(self.rectangle.eulers)
                  
                   
                if (event.type == KEYDOWN) and (event.key == K_RIGHT):
                    
                    # random position of rectangle
                    self.rectangle.set_rotation(random.uniform(0,360), random.uniform(0,360), random.uniform(0,360))
                    self.rectangle.set_translation(random.uniform(-5,5), random.uniform(-5,5), random.uniform(-10,-20))
                    self.rectangle.draw_wired_rect()
                    pg.time.wait(60)
                    
                    print(f"random rotation: {self.rectangle.eulers}")
                    print(f"random translation: {self.rectangle.position}")
                    
                    # take screenshot && write rectangle data to CSV file
                    if (self.screenshot):
                        
                        # calculate annotation
                        wc, pc, center = self.get_coordinates(self.rectangle.modelview, glGetDoublev(GL_PROJECTION_MATRIX), glGetDoublev(GL_VIEWPORT))
                        # write to json
                        write(rect_name, img_shot,  wc, pc, center)
                        
                        if (rect_name == img_number):
                            self.save_image(rect_name, img_shot)
                            img_shot += 1
                        else:
                            img_number += 1  
                            rect_name = img_number   
                            img_shot = 1
                            self.save_image(rect_name, img_shot)
                            img_shot += 1    
                        

                if (event.type == KEYDOWN) and (event.key == K_RETURN):
                    print("delete rectangle...")
                    del self.rectangle
                    # new size of rectangle
                    self.rectangle = RectangleMesh(random.uniform(0.1,5), random.uniform(0.1,5), random.uniform(0.1,5), [0,0,0], [0,0,-15])   
                    print("created rectangle: ", self.rectangle.width, self.rectangle.height, self.rectangle.depth)
                    # rectangle name count
                    rect_name += 1
                    
                # --- Drawing the scene --- #
                glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
                
                self.rectangle.draw_wired_rect()
                    
                pg.display.flip()
                pg.time.wait(60)

        self.quit()
          
    def quit(self):
        pg.quit()

    def save_image(self, rect_name, img_shot):
        print("taking screenshot...")
        pixels = glReadPixels(0, 0, self.display[0], self.display[1], GL_RGB, GL_UNSIGNED_BYTE) 
        image = pg.image.frombuffer(pixels, (self.display[0], self.display[1]), 'RGB') # read pixels from the OpenGL buffer
        name = "wireframes\\img" + str(rect_name) + "_" + str(img_shot) + ".png"
        pg.image.save(image, name) # It then converts those pixels into a Pygame surface and saves it using pygame.image.save()
        
    def draw_axes(self):
        
        # X axis (red)
        glBegin(GL_LINES)
        glColor3f(1, 0, 0)
        glVertex3f(0, 0, 0)
        glVertex3f(5, 0, 0)
        glEnd()

        # Y axis (green)
        glBegin(GL_LINES)
        glColor3f(0, 1, 0)
        glVertex3f(0, 0, 0)
        glVertex3f(0, 5, 0)
        glEnd()

        # Z axis (blue)
        glBegin(GL_LINES)
        glColor3f(0, 0, 1)
        glVertex3f(0, 0, 0)
        glVertex3f(0, 0, 5)
        glEnd()      

    def get_coordinates(self, modelview_matrix, projection_matrix, viewport):
        
        print(modelview_matrix)
        world_coordinates = []
        projection_coordinates = []
        center_coordinates = [] # consists of 2 elements: world and projection coordinates
        # loop through rectangle vertices
        for vertex in self.rectangle.vertices:
            
            vertex_homogeen = vertex + (1,) # homogene cord
            
            transformed_vertex_world = [0,0,0,0]
            
            # apply model-view matrix
            for i in range(4):
                for j in range(4):
                    transformed_vertex_world[i] += float(modelview_matrix[i][j] * vertex_homogeen[j])
             
            # normaliseren      
            for i in range(4):
                transformed_vertex_world[i] = transformed_vertex_world[i] /  transformed_vertex_world[3]
                
            transformed_vertex_projection = [0,0,0,0]
            
            # apply projection matrix -> those are normalized
            for i in range(4):
                for j in range(4):
                    transformed_vertex_projection[i] += float(projection_matrix[i][j] * transformed_vertex_world[j])
            
            print("vertex projection cords: ",transformed_vertex_projection)
            
            # calculate screen cords     
            screen_x, screen_y = self.convert_projected_to_screen(transformed_vertex_projection[0], transformed_vertex_projection[1], viewport)

            # append to list
            world_coordinates.append(transformed_vertex_world[:3])
            projection_coordinates.append((screen_x, screen_y))
            
        # center calculation 
        # values = world_coordinates[0]
        # x, y, z = values[0], values[1], values[2]
        # x = x-self.rectangle.width
        # y = y-self.rectangle.height
        # z = z-self.rectangle.depth
        # center_coordinates.append((x,y,z))
        # self.convert_projected_to_screen(x, y, viewport)
        # center_coordinates.append((screen_x, screen_y))  
        #print("those are the projections cords: \n",projection_coordinates)
        #print("those are the world cords: \n",world_coordinates)
        
        return world_coordinates, projection_coordinates, center_coordinates

    def convert_projected_to_screen(self, proj_x, proj_y, viewport):
        screen_x = (1 + proj_x) * (viewport[2] * 0.5)
        screen_y = (1 - proj_y) * (viewport[2] * 0.5)
        return int(screen_x), int(screen_y)
      
if __name__ == "__main__":
    myApp = App()

