# face-detector
An AI face-dector written in python

## To run install the following packages on your machine

### install python3

```
sudo apt install python3
```


### install opencv

```
sudo apt install python3-opencv
```


### install kivy

```
sudo apt install python3-kivy
```

### install pyserial (for facefollower.py)

for Ubuntu
```
sudo apt install python3-serial
```

for Windows/mac
```
sudo apt install python3-pyserial
```

### set the serial port name and baud rate in line 23 (for facefollower.py)

for Ubuntu (replace ttyUSB0 with arduino address)
```
ser = serial.Serial('/dev/ttyUSB0', 9600)
```
for Windows/mac (replace # with the COM number of arduino address)
```
ser = serial.Serial('COM#', 9600)
```

### Run the program

1. navigate to the folder that this repository is in

2. Select and execute the version of the app you would like to use:
      
      a. facedetector
      b. face-smile-detector
      c. face-smile-detector_app
      d. face-follower_app

```
python3 version-of-app-to-execute.py
```


