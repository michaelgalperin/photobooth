import cv2

# Attempt to use the first camera (index 0)
cap = cv2.VideoCapture(0)

# Check if the camera was successfully opened
if cap.isOpened():
    ret, frame = cap.read()
    if ret:
        # Display the captured frame
        cv2.imshow('Test Frame', frame)
        cv2.waitKey(0)  # Wait for a key press to close the window
        cv2.destroyAllWindows()
    else:
        print("Failed to capture an image")
else:
    print("Failed to open the camera")

cap.release()
