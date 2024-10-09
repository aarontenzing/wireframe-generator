import pygame as pg
from pygame import *
from OpenGL.GL import *
from OpenGL.GLU import *
import random
from rectangle import RectangleMesh
from handle_json import write_json, clear_json
import os

class App:

    def __init__(self, manual):

        # initialize pygame for GUI
        pg.init() 
        self.display = (512,512)
        self.screen = pg.display.set_mode(self.display, pg.OPENGL|pg.DOUBLEBUF) # tell pygame we run OPENGL & DOUBLEBUFFERING, one frame vis & one drawing
        pg.display.set_caption("Wireframe generator")
        
        # activation variables 
        self.axes = 0
        self.screenshot = 1
        clear_json()
        
        # get the base directory
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        self.wireframes_dir = os.path.join(BASE_DIR, 'wireframes')
        icon = os.path.join(BASE_DIR, 'images_sd')
        icon = os.path.join(icon, 'rect.png')
        
        # Check if the directory exists, if not create it
        if not os.path.exists(self.wireframes_dir):
            os.makedirs(self.wireframes_dir)
            
        pg.display.set_icon(pg.image.load(icon))    
            
        # clearing directory
        for file_name in os.listdir(self.wireframes_dir):
            file_path = os.path.join(self.wireframes_dir, file_name)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(f"Failed to delete {file_path}. Reason: {e}")
        
        # initialize OpenGL
        glClearColor(0,0,0,1)
        
        glMatrixMode(GL_PROJECTION) # activate projection matrix
        
        gluPerspective(45, self.display[0]/self.display[1], 0.1, 100)
        self.projectionmatrix = glGetDoublev(GL_PROJECTION_MATRIX)
        print("Projection matrix: \n", self.projectionmatrix)
        
        glMatrixMode(GL_MODELVIEW) # activate modelview matrix
        
        gluLookAt(0, 0, -15, 0, 0, 0, 0, 1, 0) # set camera position (eye, center, up)
        print("ModelView matrix: \n", glGetDoublev(GL_MODELVIEW_MATRIX))
        
        # draw wired rectangle
        self.rectangle = RectangleMesh(3, 3, 3, [0,0,0], [0,0,0]) # create rectangle 1-3
        self.rectangle.draw_wired_rect()
        
        if (manual):
            self.mainLoop()

    def mainLoop(self):
        rect_id = 0
        step = 1
        running = True
        while(running):
            # Check for events
            for event in pg.event.get():
                
                if (event.type == pg.QUIT):
                    running = False
                
                if (event.type == pg.KEYDOWN):
                   
                    if (event.key == K_s):
                        # enable screenshots
                        self.screenshot = not self.screenshot 
                    
                    if (event.key == K_r):
                        # reset position of rectangle
                        self.rectangle.translate('reset', step)
                    
                    if (event.key == K_PAGEUP):
                        self.rectangle.translate('forward', step) 
                               
                    if (event.key == K_PAGEDOWN):
                        self.rectangle.translate('backward', step)     
                             
                    if (event.key == K_UP):
                        self.rectangle.translate('up', step)  

                    if (event.key == K_DOWN):
                        self.rectangle.translate('down', step)  
                        
                    if (event.key == K_RIGHT):
                        self.rectangle.translate('right', step)
                    
                    if (event.key == K_LEFT):
                        self.rectangle.translate('left', step)    
                    
                    if (event.key == K_ESCAPE):
                        print("Coordinates vertices: \n", self.rectangle.get_world_coordinates())
                        print("modelview matrix: \n", self.rectangle.modelview)
                        print("projection matrix: \n", glGetDoublev(GL_PROJECTION_MATRIX))

                    if (event.key == K_u):
                        if (step < 0.1):
                            step *= 2
                        else:
                            step += 0.1
                            print('Step increment: ', float(step))
                            
                    if (event.key == K_d):
                        step /= 2
                        print('Step decrement: ', float(step))
                    
                    if (event.key == K_a):
                        # draw axes
                        self.axes = not self.axes
                    
                    if (event.key == K_SPACE):
                        # random position of rectangle
                        self.rectangle.set_rotation(random.uniform(0,360), random.uniform(0,360), random.uniform(0,360))
                        self.rectangle.set_translation(random.uniform(-3,3), random.uniform(0,4), 0)
                        self.rectangle.draw_wired_rect()
                        pg.time.wait(10) # wait 10ms till complete the drawing
                        
                        print(f"Random rotation: {self.rectangle.eulers}")
                        print(f"Random translation: {self.rectangle.position}")
                        
                        # take screenshot && write rectangle data to CSV file
                        if (self.screenshot):
                            self.save_image(rect_id)
                            self.write_annotations(rect_id)
                            rect_id += 1 

                    if (event.key == K_RETURN):
                        print("Delete rectangle...")
                        del self.rectangle
                        self.rectangle = RectangleMesh(random.uniform(1,4), random.uniform(1,4), random.uniform(1,4), [0,0,0], [0,0,0])   
                        print("Created rectangle: ", self.rectangle.width, self.rectangle.height, self.rectangle.depth)
                        
                # --- Drawing the scene --- #
                glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
                
                self.rectangle.draw_wired_rect()
                
                if (self.axes):
                
                    glBegin(GL_LINES)

                    # X Axis in Red
                    glColor3f(1, 0, 0)
                    glVertex3f(0, 0, 0)
                    glVertex3f(5, 0, 0)

                    # Y Axis in Green
                    glColor3f(0, 1, 0)
                    glVertex3f(0, 0, 0)
                    glVertex3f(0, 5, 0)

                    # Z Axis in Blue
                    glColor3f(0, 0, 1)
                    glVertex3f(0, 0, 0)
                    glVertex3f(0, 0, 5)

                    glEnd()
                    
                pg.display.flip()
                pg.time.wait(60)

        self.quit()
          
    def quit(self):
        pg.quit()
    
    def write_annotations(self, rect_id):
        pc, wc = self.get_annotations(self.rectangle.modelview, self.projectionmatrix, glGetIntegerv(GL_VIEWPORT)) # calculate annotation
        valid = self.object_on_screen(pc)  # check if rectangle valid
        dimensions = self.rectangle.get_dimensions()
        write_json(rect_id, dimensions, pc, wc, valid)
    
    def save_image(self, rect_id):
        print("Taking screenshot...")
        pixels = glReadPixels(0, 0, self.display[0], self.display[1], GL_RGB, GL_UNSIGNED_BYTE) 
        image = pg.image.frombuffer(pixels, (self.display[0], self.display[1]), 'RGB') # read pixels from the OpenGL buffer
        # image = pg.transform.flip(image, True, False) # flip
        # name = "wireframes\\img" + str(rect_id) + "_" + str(img_shot) + ".png"
        name = os.path.join(self.wireframes_dir, f"{rect_id}.jpg")
        pg.image.save(image, name) # It then converts those pixels into a Pygame surface and saves it using pygame.image.save()         
    
    def get_annotations(self, model_view, projection, viewport):
        # Calculate world and pixel cords of vertices rectangle
        world_coordinates = []
        pixel_coordinates = []
    
        for vertex in self.rectangle.vertices:
            x_screen, y_screen, z =  gluProject(vertex[0], vertex[1], vertex[2], model_view, projection, viewport)
            pixel_coordinates.append((int(x_screen),int(y_screen)))
        
        # print("pixel coordinates: ",pixel_coordinates)
        # print("world coordinates: ",self.rectangle.get_world_coordinates())
        world_coordinates = self.rectangle.get_world_coordinates()
        
        # Calculate center
        x_screen, y_screen, _ = gluProject(0, 0, 0, model_view, projection, viewport)
        pixel_coordinates.append((int(x_screen), int(y_screen)))
        
        return pixel_coordinates, world_coordinates

    def object_on_screen(self, projection_coordinates):
        outside = 0
        for i in projection_coordinates:
            if (i[0] not in range(0,self.display[0]) or i[1] not in range(0,self.display[1])):
                outside += 1
                if (outside == 3):
                    return "false"
            else:
                continue

        return "true"        
    
    def generate_random_rectangle(self, amount, shots):
        rect_id = 0  
        for i in range(amount):
            del self.rectangle
            self.rectangle = RectangleMesh(random.uniform(2,4), random.uniform(2,4), random.uniform(2,4), [0,0,0], [0,0,0])       
            print("created rectangle")
            for j in range(shots):
                # random position of rectangle
                self.rectangle.set_rotation(random.uniform(0,360), random.uniform(0,360), random.uniform(0,360))
                self.rectangle.set_translation(random.uniform(-3,3), random.uniform(0,4), 0)
                self.rectangle.draw_wired_rect()
                pg.time.wait(10)
                        
                # take screenshot && write rectangle data to CSV file           
                self.save_image(rect_id)
                self.write_annotations(rect_id)  
                print("Rectangle ", rect_id, " generated successfully!")
                rect_id += 1
      
if __name__ == "__main__":
    
    manual = input("Do you want to manually generate wireframes? (y/n) ")
   
    if (manual == "y"):
        myApp = App(True)
    elif (manual == "n"):
        myApp = App(False)
        amount = input("How many wireframes do you want to generate? ")
        shots = input("How many shots per wireframe? ")
        myApp.generate_random_rectangle(int(amount), int(shots))
        print("Wireframes generated successfully!")