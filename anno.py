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
        self.display = (1280,720)
        self.screen = pg.display.set_mode(self.display, pg.OPENGL|pg.DOUBLEBUF) # tell pygame we run OPENGL & DOUBLEBUFFERING, one frame vis & one drawing
        pg.display.set_caption("Wireframe generator")
        
        # Initialize OpenGL
        glClearColor(0,0,0,1)
        gluPerspective(45, self.display[0]/self.display[1], 0.1, 50)
        
        # Activate variables 
        self.axes = 0
        self.wireframe = 1
        
        # Draw wired rectangle
        self.rectangle = RectangleMesh(1, 1, 1, [1,1,1], [0,1,0], [0,0,-10])   
        self.rectangle.draw_wired_rect()
        glTranslatef(self.rectangle.position[0], self.rectangle.position[1], self.rectangle.position[2])   
        self.draw_axes()
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
                
                elif (event.type == KEYDOWN) and (event.key == K_w):
                    self.wireframe = not self.wireframe
                
                elif (event.type == KEYDOWN) and (event.key == K_a):
                    # draw axes
                    self.axes = not self.axes
                   
                elif (event.type == KEYDOWN) and (event.key == K_RIGHT):
                    # random position of rectangle
                    self.rectangle.random_rotation()
                    
                    if (rect_name == img_number):
                        self.save_image(rect_name, img_shot)
                        img_shot += 1
                    else:
                        img_number += 1  
                        rect_name = img_number   
                        img_shot = 0
                        self.save_image(rect_name, img_shot)
                        img_shot += 1    

                elif (event.type == KEYDOWN) and (event.key == K_RETURN):
                    # New size of rectangle (scale)
                    rect_name += 1
                    self.rectangle.set_scale(random.uniform(0.1,3), random.uniform(0.1,3), random.uniform(0.1,3))
                    print(self.rectangle.width, self.rectangle.depth, self.rectangle.height)
                
                glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
                if (self.wireframe):
                    glDisable(GL_DEPTH_TEST)
                    glDisable(GL_LIGHTING)
                    glDisable(GL_LIGHT0)
                    self.rectangle.draw_wired_rect()
                else:
                    self.lighting_setup()
                    self.rectangle.draw_rect()
                if (self.axes):
                    self.draw_axes()
                    
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

        glLightfv(GL_LIGHT0, GL_POSITION, (-2, -2, 2, 1))  # Set light position

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

        
class RectangleMesh:

    def __init__(self, width, height, depth, scale, eulers, position):
            
        self.width = width/2
        self.height = height/2
        self.depth = depth/2
        self.scale = np.array(scale, dtype=np.float32) # scale
        self.eulers= np.array(eulers, dtype=np.float32) # angle
        self.position= np.array(position, dtype=np.float32) # position
    
    def draw_rect(self):
        
        # Set material properties
        glColor3f(1.0, 1.0, 1.0)  # Set the color to white
        glMaterialfv(GL_FRONT, GL_AMBIENT, [0.1, 0.1, 0.1, 1.0])  # Ambient material property
        glMaterialfv(GL_FRONT, GL_DIFFUSE, [1.0, 1.0, 1.0, 1.0])  # Diffuse material property
        glMaterialfv(GL_FRONT, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])  # Specular material property
        glMaterialf(GL_FRONT, GL_SHININESS, 50.0)  # Shininess of the material
    
        glBegin(GL_QUADS)
        # front plane
        glVertex3f(self.width, self.height, self.depth) # front top right
        glVertex3f(-self.width, self.height, self.depth) # front top left
        glVertex3f(-self.width, -self.height, self.depth) # front bottom left
        glVertex3f(self.width, -self.height, self.depth) # front bottom right
        
        # Back plane
        glVertex3f(self.width, self.height, -self.depth) # back top right
        glVertex3f(-self.width, self.height, -self.depth) # back top left
        glVertex3f(-self.width, -self.height, -self.depth) # back bottom left
        glVertex3f(self.width, -self.height, -self.depth) # back bottom right
         
        # left    
        glVertex3f(-self.width, self.height, self.depth) # front top left
        glVertex3f(-self.width, -self.height, self.depth) # front bottom left
        glVertex3f(-self.width, -self.height, -self.depth) # back bottom left
        glVertex3f(-self.width, self.height, -self.depth) # back top left
        
        # right
        glVertex3f(self.width, self.height, self.depth) # front top right
        glVertex3f(self.width, -self.height, self.depth) # front bottom right
        glVertex3f(self.width, -self.height, -self.depth) # back bottom right
        glVertex3f(self.width, self.height, -self.depth) # back top right
        
        # top
        glVertex3f(-self.width, self.height, self.depth) # front top left
        glVertex3f(self.width, self.height, self.depth) # front top right
        glVertex3f(self.width, self.height, -self.depth) # back top right
        glVertex3f(-self.width, self.height, -self.depth) # back top left
        
        # bottom
        glVertex3f(-self.width, -self.height, self.depth) # front bottom left
        glVertex3f(self.width, -self.height, self.depth) # front bottom right
        glVertex3f(self.width, -self.height, -self.depth) # back bottom right
        glVertex3f(-self.width, -self.height, -self.depth) # back bottom left
        
        glEnd()

    def draw_wired_rect(self):
        
        glEnable(GL_LINE_SMOOTH)  # Enable line smoothing
        glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)  # Use the highest quality for line smoothing
        glLineWidth(3)
        
        glBegin(GL_LINES)
        glColor3f(1.0, 1.0, 1.0)  
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
        
    def random_rotation(self):

        # Generate random angles for rotation
        angle_x = random.uniform(0, 360)
        angle_y = random.uniform(0, 360)
        angle_z = random.uniform(0, 360)
                
        # Apply radnom rotation
        
        glRotatef(angle_x, 1, 0, 0)
        glRotatef(angle_y, 0, 1, 0)
        glRotatef(angle_z, 0, 0, 1)  
           
    def set_scale(self, x, y, z):
        
        # new scale rectangle 
        self.width = x 
        self.height = y 
        self.depth = z
        self.draw_rect() 
        
        
if __name__ == "__main__":
    myApp = App()

