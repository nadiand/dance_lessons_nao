import cv2
import time

def take_pics(cap, number_of_pics = 3, sleep_time = 0.5):
    print("Start taking pictures")
    while True:
        # Read the video frame-by-frame
        ret, frame = cap.read()
        if not ret:
            print("Error: Unable to capture video.")
            break
        for i in range(0, number_of_pics):
            cv2.imwrite('captured_image' + str(i) + '.jpg', frame)
            time.sleep(sleep_time)
        print("Stop taking pictures")
        break

def open_camera():
    # Open a connection to the webcam (default camera is device 0)
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not access the webcam.")
        return
    print("Camera opened")
    return cap



cap = open_camera()
take_pics(cap)
cap.release()


