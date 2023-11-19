import cv2
import os
import time
import serial
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button

#Get the path of the current script
script_path=os.path.abspath(__file__)

# Get the directory containing the script
script_directory = os.path.dirname(script_path)

# Concatenate the script directory with the face XML file name
cascade_face_path = os.path.join(script_directory, 'haarcascade_frontalface_default.xml')

# Concatenate the script directory with the Smile XML file name
cascade_smile_path = os.path.join(script_directory, 'haarcascade_smile.xml')

# Open a connection to the serial port (adjust the port and baud rate as needed)
ser = serial.Serial('/dev/ttyACM0', 9600)

# Create an App class called FaceDetect
class FaceDetect(App):

    #Build a window named self and set the columns
    def build(self):
        self.window = GridLayout()
        self.window.cols = 1
        self.window.size_hint = (0.6, 0.7)
        self.window.pos_hint = {"center_x":0.5, "center_y":0.5 }
    
        # Add widgets to the window

        # Create a lable widget with a greeting
        self.greeting = Label(
                        text = "Welcome to Paul's Facial Recognition App",
                        font_size = 32,
                        color = '#00FFCE'
                        )
        self.window.add_widget(self.greeting)

        # Create a label widget with a prompt
        self.prompt = Label(
                      text = "Please select the functionality",
                      font_size = 16
                      )
        self.window.add_widget(self.prompt)

        # Create a button widget with face detector only
        self.face = Button(
                      text = "Track face only",
                      size_hint = (1,0.5),
                      bold = True,
                      background_color = '#00FFCE'
                      )
        self.face.bind(on_press = self.track_face)
        self.window.add_widget(self.face)

        # Create a button widget with face and smile detector
        self.face_smile = Button(
                      text = "Track face and smile",
                      size_hint = (1,0.5),
                      bold = True,
                      background_color = '#00FFCE'
                      )
        self.face_smile.bind(on_press = self.track_face_smile)
        self.window.add_widget(self.face_smile)
     
        return self.window
        
    #Function that launches face tracker on button press
    def track_face(self, instance):

        # Load some pre-trained data on face frontals from opencv (haar cascade algorithm)
        trained_face_data = cv2.CascadeClassifier(cascade_face_path)

        # Choose an image to detect faces in
        #img = cv2.imread('paulface.jpg')

        # Capture video from webcam
        webcam = cv2.VideoCapture(0)

        while True:
            #Read the current frame
            succesful_frame_read, frame = webcam.read()

            # Convert the image to greyscale
            img_greyscale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Detect faces
            face_coordinates = trained_face_data.detectMultiScale(img_greyscale)

            # Create rectangles around the detected faces and create a different color box around each one
            for (x,y,w,h) in face_coordinates:
                cv2.rectangle(frame,(x, y),(x+w, y+h),(0,255,0), 3)
                
                 # Send face coordinates to Arduino via serial port
                coordinates_string = f"{x},{y},{w},{h}\n"
                ser.write(coordinates_string.encode('utf-8'))


            #Add Label with prompt to press ESC to exit
            cv2.putText(frame, 'PRESS ESC TO EXIT PROGRAM', (40 ,40), fontScale = 2, fontFace = cv2.FONT_HERSHEY_PLAIN, color=(255, 255, 255))
            
            # Display the image with boxes around the detected faces
            cv2.imshow('Clever Programmer Face Detector Grey', frame)
            key = cv2.waitKey(1)

            #Exit the program if Q key is pressed
            if key == 27:
                break
            
        
        #Realease the webcam
        webcam.release()
        cv2.destroyAllWindows()
 
    # Function that launches face and smile tracker on button press
    def track_face_smile(self, instance):

        # Load some pre-trained data on face frontals and smiles from opencv (haar cascade algorithm)
        trained_face_data = cv2.CascadeClassifier(cascade_face_path)
        trained_smile_data = cv2.CascadeClassifier(cascade_smile_path)

        # Capture video from webcam
        webcam = cv2.VideoCapture(0)

        while True:
            #Read the current frame
            succesful_frame_read, frame = webcam.read()

            # Convert the image to greyscale
            img_greyscale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Detect faces
            face_coordinates = trained_face_data.detectMultiScale(img_greyscale, minNeighbors = 10)

            # Create rectangles around the detected faces and create a different color box around each one
            for (x,y,w,h) in face_coordinates:

                #Draw a rectangle around the face
                cv2.rectangle(frame,(x, y),(x+w, y+h),(0,255,0), 3)

                # Send face coordinates to Arduino via serial port
                coordinates_string = f"{x},{y},{w},{h}\n"
                ser.write(coordinates_string.encode('utf-8'))

                # Create image the size of each face box
                the_face = frame[y:y+h, x:x+w]

                #Change facebox subset to greuscale
                face_greyscale = cv2.cvtColor(the_face, cv2.COLOR_BGR2GRAY)

                # Search for smiles within each face box
                smiles = trained_smile_data.detectMultiScale(face_greyscale, scaleFactor = 1.3, minNeighbors = 12)
                
                # Run smile detection within each of the faces
                for (a,b,c,d) in smiles:
                    
                    #Draw a rectangle around each detected smile within the face
                    cv2.rectangle(the_face, (a, b), (a+c, b+d),(0,0,255),3)

                #Label this face as smiling
                if len(smiles) > 0:
                    cv2.putText(frame, 'SMILING', (x ,y+h+40), fontScale = 2, fontFace = cv2.FONT_HERSHEY_PLAIN, color=(255, 255, 255))

            #Add Label with prompt to press ESC to exit
            cv2.putText(frame, 'PRESS ESC TO EXIT PROGRAM', (40 ,40), fontScale = 2, fontFace = cv2.FONT_HERSHEY_PLAIN, color=(255, 255, 255))

            # Display the image with boxes around the detected faces
            cv2.imshow('Clever Programmer Face and Smile Detector', frame)
            key = cv2.waitKey(1)

            
            #Exit the program if Q key is pressed
            if key == 27:
                break
            

        #Release the webcam
        webcam.release()
        cv2.destroyAllWindows()
         
# Run the App called FaceDetect   
if __name__ == "__main__":
    FaceDetect().run()
