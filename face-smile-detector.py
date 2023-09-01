import cv2

# Load some pre-trained data on face frontals and smiles from opencv (haar cascade algorithm)
trained_face_data = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
trained_smile_data = cv2.CascadeClassifier('haarcascade_smile.xml')

# Capture video from webcam
webcam = cv2.VideoCapture(0)

while True:
    #Read the current frame
    succesful_frame_read, frame = webcam.read()

    # Convert the image to greyscale
    img_greyscale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces
    face_coordinates = trained_face_data.detectMultiScale(img_greyscale, minNeighbors = 12)

    # Create rectangles around the detected faces and create a different color box around each one
    for (x,y,w,h) in face_coordinates:

        #Draw a rectangle around the face
        cv2.rectangle(frame,(x, y),(x+w, y+h),(0,255,0), 3)

        # Create image the size of each face box
        the_face = frame[y:y+h, x:x+w]

        #Change facebox subset to greuscale
        face_greyscale = cv2.cvtColor(the_face, cv2.COLOR_BGR2GRAY)

        # Search for smiles within each face box
        smiles = trained_smile_data.detectMultiScale(face_greyscale, scaleFactor = 1.7, minNeighbors = 25)
        
        # Run smile detection within each of the faces
        for (a,b,c,d) in smiles:
            
            #Draw a rectangle around each detected smile within the face
            cv2.rectangle(the_face, (a, b), (a+c, b+d),(0,0,255),3)

        #Label this face as smiling
        if len(smiles) > 0:
            cv2.putText(frame, 'SMILING', (x ,y+h+40), fontScale = 2, fontFace = cv2.FONT_HERSHEY_PLAIN, color=(255, 255, 255))

    # Display the image with boxes around the detected faces
    cv2.imshow('Clever Programmer Face and Smile Detector', frame)
    key = cv2.waitKey(1)

    #Exit the program if Q key is pressed
    if key == 81 or key == 113:
        break

#Realease the webcam
webcam.release()

print("Code Completed")