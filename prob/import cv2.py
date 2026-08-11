"""
half_gray.py
Module for splitting a webcam feed into normal + grayscale halves.
"""

import cv2


def process_frame(frame):
    """Take a BGR frame, return it with the right half converted to grayscale."""
    height, width = frame.shape[:2]

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_bgr = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

    output = frame.copy()
    output[:, width // 2:] = gray_bgr[:, width // 2:]

    return output


def run(camera_index=0):
    """Open the camera and display the half-grayscale feed until 'q' is pressed."""
    cap = cv2.VideoCapture(camera_index)

    if not cap.isOpened():
        print("Cannot open camera")
        return

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            output = process_frame(frame)
            cv2.imshow("Half Grayscale", output)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    run()