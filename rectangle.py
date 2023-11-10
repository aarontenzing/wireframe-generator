from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import random

class RectangleMesh:

    def __init__(self, width, height, depth, eulers, position):
            
        self.width = width/2
        self.height = height/2
        self.depth = depth/2
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

    def set_translation(self, pos_x, pos_y, pos_z, wireframe):
        
        # set postions
        self.position[0] = pos_x
        self.position[1] = pos_y
        self.position[2] = pos_z
        glTranslatef(self.position[0], self.position[1], self.position[2])
        # draw with rotation
        if (wireframe):
            self.draw_wired_rect()
        else:
            self.draw_rect()        
        
    def set_rotation(self, angle_x, angle_y, angle_z, wireframe):
        
        # set eulers
        self.eulers[0] = angle_x
        self.eulers[1] = angle_y
        self.eulers[2] = angle_z
        # apply radnom rotation
        glRotatef(self.eulers[0], 1, 0, 0)
        glRotatef(self.eulers[1], 0, 1, 0)
        glRotatef(self.eulers[2], 0, 0, 1)  
        
        # draw with rotation
        if (wireframe):
           self.draw_wired_rect()
        else:
            self.draw_rect()      
           
    def set_scale(self, x, y, z, wireframe):
        
        # new scale rectangle 
        self.width = x 
        self.height = y 
        self.depth = z
        
        if (wireframe):
            self.draw_wired_rect()
        else:
            self.draw_rect()

    def write_dim_csv(self):
        # normalize dimensions
        w = self.width / self.height
        h = 1
        d = self.depth / self.height