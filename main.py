# Imports
import numpy as np
import cv2

# Helper function
def nothing(x):
    pass

# Get the webcame
cap = cv2.VideoCapture(0)

# Create window
cv2.namedWindow('Range Picker')

# Create trackbar for colour threshlding
# Hue is from 0-19 in OpenCV
cv2.createTrackbar('Hmin', 'Range Picker', 0, 179, nothing) 
cv2.createTrackbar('Hmax', 'Range Picker', 0, 179, nothing) 

# Set default value for min and max
cv2.setTrackbarPos('Hmin', 'Range Picker', 30)
cv2.setTrackbarPos('Hmax', 'Range Picker', 40)

while(True):
    # Get current position of all trackbars
    h_min = cv2.getTrackbarPos('Hmin', 'Range Picker')
    h_max = cv2.getTrackbarPos('Hmax', 'Range Picker')
    
    # Capture frame-by-frame
    ret, frame = cap.read()
    
    # Covert to hsv colour space
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv_frame)
    blur = cv2.GaussianBlur(h, (5,5), 1)
    thresh = cv2.inRange(blur, h_min, h_max)
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, (5,5))
    closing =  cv2.morphologyEx(opening, cv2.MORPH_CLOSE, (5,5))
    countours, hierarchy = cv2.findContours(closing, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for c in countours:
        rect = cv2.boundingRect(c)
        if rect[2] < 50 or rect[3] < 50: continue
        x,y,w,h = rect
        cv2.rectangle(frame, (x,y), (x+w, y+h), (0,0,255), 2)
        
    
        cx = x + (w * 0.5)
        cy = y + (y* 0.5)


    # Display the resulting frame
    cv2.imshow('Frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()