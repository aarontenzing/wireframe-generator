import pygame as pg
from pygame import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import random
from rectangle import RectangleMesh
from handle_json import write, clear_json

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
        self.projectionmatrix = glGetDoublev(GL_PROJECTION_MATRIX)
        # draw wired rectangle
        self.rectangle = RectangleMesh(random.uniform(0.1,5), random.uniform(0.1,5), random.uniform(0.1,5), [0,0,0], [0,0,-15]) 
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
                        wc, pc, center = self.get_annotations(self.rectangle.modelview, self.projectionmatrix, glGetIntegerv(GL_VIEWPORT))
                        # write to json
                        write(rect_name, img_shot, self.rectangle.get_norm_dim(),  wc, pc, center)
                        
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
        #image = pg.transform.flip(image, False, True) # flip
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
    
    def get_annotations(self, model_view, projection, viewport):
        # Calculate world and pixel cords of vertices rectangle
        world_coordinates = []
        pixel_coordinates = []
        center = []
        for vertex in self.rectangle.vertices:
            x_screen, y_screen, z =  gluProject(vertex[0], vertex[1], vertex[2], model_view, projection, viewport)
            pixel_coordinates.append((int(x_screen),int(y_screen)))
            x_world, y_world, z_world = gluUnProject( x_screen, y_screen, 0, model_view, projection, viewport)
            world_coordinates.append((x_world, y_world, z_world))
        
        print("pixel coordinates: ",pixel_coordinates)
        print("world coordinates: ",world_coordinates)
        
        # Calculate center
        x_screen, y_screen, z = gluProject(0, 0, 0, model_view, projection, viewport)
        x_world, y_world, z_world = gluUnProject( x_screen, y_screen, 0, model_view, projection, viewport)
        center.append((x_world, y_world, z_world))
        center.append((int(x_screen), int(y_screen)))
        
        return world_coordinates, pixel_coordinates, center
      
if __name__ == "__main__":
    myApp = App()

