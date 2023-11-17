import pygame as pg
from pygame import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import random
from rectangle import RectangleMesh
from write_csv import write

class App:

    def __init__(self):

        # initialize pygame for GUI
        pg.init() 
        self.display = (512,512)
        self.screen = pg.display.set_mode(self.display, pg.OPENGL|pg.DOUBLEBUF) # tell pygame we run OPENGL & DOUBLEBUFFERING, one frame vis & one drawing
        pg.display.set_caption("Wireframe generator")
        
        # activation variables 
        self.axes = 0
        self.wireframe = 1
        self.screenshot = 0
        
        # initialize OpenGL
        glClearColor(0,0,0,1)
        gluPerspective(45, self.display[0]/self.display[1], 0.1, 50)
       
        # draw wired rectangle
        self.rectangle = RectangleMesh(1, 1, 1, [0,0,0], [0,0,-20]) 
        self.rectangle.draw_wired_rect()
        
        self.mainLoop()

    def mainLoop(self):
        rect_name = 0  
        img_number = 0 # counts the rectangle that is been shown
        img_shot = 0 # counts how many screenshots were taken
        
        running = True
        while(running):
            # Check for events
            for event in pg.event.get():
                
                if (event.type == pg.QUIT):
                    running = False
                
                if (event.type == KEYDOWN) and (event.key == K_w):
                    # draw wired or not
                    self.wireframe = not self.wireframe
                    
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
                    
                    print("random rotation: ", self.rectangle.eulers)
                    print("random translation: ", self.rectangle.position)
                    
                    # write new rectangle coordinates and rotations to CSV file
                    if (self.screenshot):
                        if (rect_name == img_number):
                            self.save_image(rect_name, img_shot)
                            img_shot += 1
                        else:
                            img_number += 1  
                            rect_name = img_number   
                            img_shot = 0
                            self.save_image(rect_name, img_shot)
                            img_shot += 1    

                if (event.type == KEYDOWN) and (event.key == K_RETURN):
                    print("delete rectangle...")
                    del self.rectangle
                    # new size of rectangle
                    self.rectangle = RectangleMesh(random.uniform(0.1,5), random.uniform(0.1,5), random.uniform(0.1,5), [0,0,0], [0,0,-15])   
                    print("created rectangle: ",self.rectangle.width, self.rectangle.height, self.rectangle.depth)
                    # rectangle name count
                    rect_name += 1
                    # writable dimensions to csv file: normalize by the height
                    
                # --- Drawing the scene --- #
                glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
                
                if (self.wireframe):
                    glDisable(GL_DEPTH_TEST)
                    glDisable(GL_LIGHTING)
                    glDisable(GL_LIGHT0)
                    self.rectangle.draw_wired_rect()
                else:
                    self.lighting_setup()
                    self.rectangle.draw_rect()
                
                # Get the current model-view matrix
                modelview_matrix = glGetFloatv(GL_MODELVIEW_MATRIX)
                
                 # Get the current projection matrix
                projection_matrix = glGetFloatv(GL_PROJECTION_MATRIX)
                    
                pg.display.flip()
                pg.time.wait(60)

        self.quit()
          
    def quit(self):
        pg.quit()

    def save_image(self, rectangle_number, count):
        pixels = glReadPixels(0, 0, self.display[0], self.display[1], GL_RGB, GL_UNSIGNED_BYTE) 
        image = pg.image.frombuffer(pixels, (self.display[0], self.display[1]), 'RGB') # read pixels from the OpenGL buffer
        name = "wireframes\\img" + str(rectangle_number) + "_" + str(count) + ".png"
        pg.image.save(image, name) # It then converts those pixels into a Pygame surface and saves it using pygame.image.save()
    
    def lighting_setup(self):
        
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)

        glLightfv(GL_LIGHT0, GL_POSITION, (0, 5, 0, 1))  # Set light position
        
        ambient_light = (0.2, 0.2, 0.2, 1)
        diffuse_light = (0.8, 0.8, 0.8, 1)
        specular_light = (1.0, 1.0, 1.0, 1)

        glLightfv(GL_LIGHT0, GL_AMBIENT, ambient_light)
        glLightfv(GL_LIGHT0, GL_DIFFUSE, diffuse_light)
        glLightfv(GL_LIGHT0, GL_SPECULAR, specular_light)
        
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

    def get_coordinates(self, modelview_matrix, projection_matrix):
        world_coordinates = []
        projection_coordinates = []
        # loop through rectangle vertices
        for vertex in self.rectangle.vertices:
            transformed_vertex_world = [0,0,0,0]
            transformed_vertex_projection = [0,0,0,0]
            
            # apply model-view matrix
            for i in range(4):
                for j in range(4):
                    transformed_vertex_world[i] += modelview_matrix[i][j] * vertex[j]
                    
            # apply projection matrix
            for i in range(4):
                for j in range(4):
                    transformed_vertex_projection[i] += projection_matrix[i][j] * vertex[j]
            
            world_coordinates.append(transformed_vertex_world[:3])
            projection_coordinates.append(transformed_vertex_projection[:3])
        
        return world_coordinates, projection_coordinates
      
if __name__ == "__main__":
    myApp = App()

