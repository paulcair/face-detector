import cv2
#from random import randrange

# Load some pre-trained data on face frontals from opencv (haar cascade algorithm)
trained_face_data = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

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

    # Display the image with boxes around the detected faces
    cv2.imshow('Clever Programmer Face Detector Grey', frame)
    key = cv2.waitKey(1)

    #Exit the program if Q key is pressed
    if key == 81 or key == 113:
        break

#Realease the webcam
webcam.release()

print("Code Completed")