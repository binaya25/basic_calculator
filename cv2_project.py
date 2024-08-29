import numpy as np
import cv2
import pyfirmata

# Initializing the ultrasonic sensor
board = pyfirmata.Arduino('/dev/cu.usbserial-14340')
trigger_pin = board.get_pin('d:24:o')
echo_pin = board.get_pin('d:18:i')

def measure_distance():
    trigger_pin.write(1)
    board.pass_time(0.00001)
    trigger_pin.write(0)

    while echo_pin.read() == 0:
        pass
    start_time = board.now()

    while echo_pin.read() == 1:
        pass
    end_time = board.now()

    duration = end_time - start_time
    distance = duration * 17150
    return distance

# Initializing the camera
cap = cv2.VideoCapture(0)

# Initializing the control flags
detect_green_ball = True
distance_threshold = 50
roi_x, roi_y, roi_width, roi_height = 0, 0, int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

while True:
    ret, frame = cap.read()   # Capture a frame from the camera
    key = cv2.waitKey(1) & 0xFF
    if key == ord('7'):
        detect_green_ball = not detect_green_ball
        print(f"Green ball detection is now {'enabled' if detect_green_ball else 'disabled'}")
    elif key == ord('8'):
        distance_threshold = int(input("Enter the new distance threshold (in cm): "))
        print(f"Distance threshold set to:{distance_threshold} cm")
    elif key == ord('9'):
        roi_x = int(input("Enter X-coordinate: "))
        roi_y = int(input("Enter Y-coordinate: "))
        roi_width = int(input("Enter width of ROI: "))
        roi_height = int(input("Enter height of ROI: "))
        print(f"ROI set to: ({roi_x}, {roi_y}, {roi_width}, {roi_height})")
    elif key == ord('q'):
        break

    # Cropping the frame to ROI
    roi_frame = frame[roi_y: roi_y + roi_height, roi_x: roi_x + roi_width]

    # Converting the frame to HSV color space
    hsv = cv2.cvtColor(roi_frame, cv2.COLOR_BGR2HSV)

    # CREATING A MASK TO DETECT GREEN COLORED OBJECTS
    lower_green = np.array([30, 50, 50])
    upper_green = np.array([90, 255, 255])
    mask = cv2.inRange(hsv, lower_green, upper_green)

    # Find the contours of the green-colored objects
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Checking green objects
    if detect_green_ball and contours:  # Calculating distance using ultrasonic sensor
        distance = measure_distance()
        if distance < distance_threshold:
            for contour in contours:    # Drawing bounding box around green object and distance
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(roi_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(roi_frame, f"Distance: {distance:.2f}cm", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    cv2.imshow("Green Ball Detection", roi_frame)
    if key == ord('*'):   # Exit pressing '*'
        break

# Release camera, board, and close all windows
cap.release()
board.exit()
cv2.destroyAllWindows()