import pygame as pg
from pygame import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import random


class App:

    def __init__(self):

        # Initialize pygame for GUI
        pg.init() 
        self.display = (800,600)
        self.screen = pg.display.set_mode(self.display, pg.OPENGL|pg.DOUBLEBUF) # tell pygame we run OPENGL & DOUBLEBUFFERING, one frame vis & one drawing
        pg.display.set_caption("Wireframe generator")
        
        # Initialize OpenGL
        glClearColor(1,1,1,1)
        gluPerspective(45, self.display[0]/self.display[1], 0.1, 50)
        self.rectangle = RectangleMesh(1, 1, 1, [1,1,1], [0,1,0], [0,0,-15])   
        self.rectangle.draw_rect()
        glTranslatef(self.rectangle.position[0], self.rectangle.position[1], self.rectangle.position[2])   
        self.mainLoop()

    def mainLoop(self):
        rect_name = 0
        x = 0
        img_count = 0
        running = True
        while(running):
            # Check for events
            for event in pg.event.get():
                
                if (event.type == pg.QUIT):
                    running = False
                    
                elif (event.type == KEYDOWN) and (event.key == K_RIGHT):
                    # random position of rectangle
                    self.rectangle.random_pos()
                    if (rect_name == x):
                        self.save_image(rect_name, img_count)
                        img_count += 1
                    else:
                        x += 1  
                        rect_name = x   
                        img_count = 0
                        self.save_image(rect_name, img_count)
                        img_count += 1    

                elif (event.type == KEYDOWN) and (event.key == K_RETURN):
                    # New size of rectangle (scale)
                    rect_name += 1
                    self.rectangle.set_scale(random.uniform(0.1,3), random.uniform(0.1,3), random.uniform(0.1,3))
                    print(self.rectangle.width, self.rectangle.depth, self.rectangle.height)
                
                glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
                self.rectangle.draw_rect()
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
        
class RectangleMesh:

    def __init__(self, width, height, depth, scale, eulers, position):
            
        self.width = width/2
        self.height = height/2
        self.depth = depth/2
        self.scale = np.array(scale, dtype=np.float32) # scale
        self.eulers= np.array(eulers, dtype=np.float32) # angle
        self.position= np.array(position, dtype=np.float32) # position
    
    def draw_rect(self):
        glEnable(GL_LINE_SMOOTH)
        glLineWidth(3)
        glBegin(GL_LINES)
        glColor3f(0.0, 0.0, 0.0)  
        glVertex3f(self.width, self.height, self.depth) # front top right
        glVertex3f(self.width, -self.height, self.depth) # front bottom right

        glVertex3f(self.width, -self.height, self.depth) # front bottom right
        glVertex3f(-self.width, -self.height, self.depth) # front bottom left

        glVertex3f(-self.width, -self.height, self.depth) # front bottom left
        glVertex3f(-self.width, self.height, self.depth) # front top left
 
        glVertex3f(-self.width, self.height, self.depth) # front top left
        glVertex3f(self.width, self.height, self.depth) # front top right

        # Back plane
        glVertex3f(self.width, self.height, -self.depth) # back top right
        glVertex3f(self.width, -self.height, -self.depth) # back bottom right

        glVertex3f(self.width, -self.height, -self.depth) # back bottom right
        glVertex3f(-self.width, -self.height, -self.depth) # back bottom left

        glVertex3f(-self.width, -self.height, -self.depth) # back bottom left
        glVertex3f(-self.width, self.height, -self.depth) # back top left

        glVertex3f(-self.width, self.height, -self.depth) # back top left
        glVertex3f(self.width, self.height, -self.depth) # back top right
            
        # Connecting front and back   
        glVertex3f(self.width, self.height, self.depth) # front top right
        glVertex3f(self.width, self.height, -self.depth) # back top right

        glVertex3f(self.width, -self.height, self.depth) # front bottom right
        glVertex3f(self.width, -self.height, -self.depth) # back bottom right

        glVertex3f(-self.width, -self.height, self.depth) # front bottom left
        glVertex3f(-self.width, -self.height, -self.depth) # back bottom left

        glVertex3f(-self.width, self.height, self.depth) # front top left
        glVertex3f(-self.width, self.height, -self.depth) # back top left
        glEnd()
       
    def random_pos(self):

        # Generate random angles for rotation
        angle_x = random.uniform(0, 360)
        angle_y = random.uniform(0, 360)
        angle_z = random.uniform(0, 360)
                
        # Apply radnom rotation
        glRotatef(angle_x, 1, 0, 0)
        glRotatef(angle_y, 0, 1, 0)
        glRotatef(angle_z, 0, 0, 1)
        
        # Generate random distance for translation
        #distance_x = random.uniform(-1, 1)
        #distance_y = random.uniform(-1, 1)
        #distance_z = random.uniform(-2, -8)
        
        
        # Apply random translation
    
        #glTranslatef(0, 0, distance_z)       

    def set_scale(self, x, y, z):
        self.width = x 
        self.height = y 
        self.depth = z
        self.draw_rect() 
        
if __name__ == "__main__":
    myApp = App()

