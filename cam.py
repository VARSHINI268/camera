import cv2
import numpy as np

WINDOW_NAME = "Camera Feed"
COLORS = {
    '1': (0, 0, 255),
    '2': (0, 255, 0),
    '3': (255, 0, 0),
    '4': (0, 255, 255),
    '5': (255, 0, 255),
    '6': (255, 255, 0),
    '7': (255, 255, 255),
}


def open_camera():
    backends = [cv2.CAP_DSHOW, cv2.CAP_MSMF, cv2.CAP_ANY]
    for backend in backends:
        for index in [0, 1, 2, 3, 4]:
            cap = cv2.VideoCapture(index, backend)
            if not cap.isOpened():
                continue

            cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            ret, _ = cap.read()
            if ret:
                return cap, backend, index

            cap.release()

    return None, None, None


def draw_shape(img, start, end, color, shape, thickness=3):
    if shape == "rectangle":
        cv2.rectangle(img, start, end, color, thickness)
    elif shape == "circle":
        center = ((start[0] + end[0]) // 2, (start[1] + end[1]) // 2)
        radius = max(abs(end[0] - start[0]), abs(end[1] - start[1])) // 2
        cv2.circle(img, center, max(radius, 10), color, thickness)
    elif shape == "line":
        cv2.line(img, start, end, color, thickness)


def add_help_text(img):
    h, w = img.shape[:2]
    cv2.putText(img, "Colors: 1-7 | Shapes: R/C/L | E clear | Q quit", (10, h - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)


def main():
    cap, backend, index = open_camera()
    if cap is None:
        print("No camera detected. Please allow camera access in Windows privacy settings and try again.")
    else:
        print(f"Camera opened successfully using backend {backend} on device {index}.")

    state = {
        "color": COLORS['1'],
        "shape": "rectangle",
        "drawing": False,
        "start": None,
        "canvas": None,
    }

    cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)

    def mouse_callback(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            state["drawing"] = True
            state["start"] = (x, y)
        elif event == cv2.EVENT_MOUSEMOVE and state["drawing"]:
            state["current_end"] = (x, y)
        elif event == cv2.EVENT_LBUTTONUP:
            if state["drawing"] and state["start"] is not None:
                draw_shape(state["canvas"], state["start"], (x, y), state["color"], state["shape"], 3)
            state["drawing"] = False
            state["start"] = None

    cv2.setMouseCallback(WINDOW_NAME, mouse_callback)

    while True:
        if cap is not None and cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                print("Camera feed lost. Switching to demo mode.")
                cap.release()
                cap = None
                frame = np.zeros((480, 640, 3), dtype=np.uint8)
            else:
                frame = cv2.flip(frame, 1)
        else:
            frame = np.zeros((480, 640, 3), dtype=np.uint8)
            cv2.putText(frame, "Camera unavailable - demo mode", (70, 220),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
            cv2.putText(frame, "Allow camera access in Windows privacy settings if needed.", (45, 270),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1, cv2.LINE_AA)

        h, w = frame.shape[:2]
        if state["canvas"] is None or state["canvas"].shape[:2] != (h, w):
            state["canvas"] = np.zeros((h, w, 3), dtype=np.uint8)

        display = frame.copy()
        display = cv2.addWeighted(display, 0.85, state["canvas"], 0.75, 0)

        if state["drawing"] and state["start"] is not None and "current_end" in state:
            draw_shape(display, state["start"], state["current_end"], state["color"], state["shape"], 3)

        # Draw some geometric guide shapes on the frame
        cv2.rectangle(display, (30, 30), (220, 180), (0, 255, 0), 2)
        cv2.circle(display, (w // 2, h // 2), 70, (255, 0, 0), 2)
        cv2.line(display, (10, h - 10), (220, h - 120), (0, 0, 255), 2)
        cv2.ellipse(display, (w - 120, 100), (80, 40), 0, 0, 360, (0, 255, 255), 2)

        add_help_text(display)
        cv2.putText(display, f"Mode: {state['shape'].title()} | Color: {state['color']}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1, cv2.LINE_AA)

        cv2.imshow(WINDOW_NAME, display)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('r'):
            state["shape"] = "rectangle"
        elif key == ord('c'):
            state["shape"] = "circle"
        elif key == ord('l'):
            state["shape"] = "line"
        elif key == ord('e'):
            state["canvas"] = np.zeros((h, w, 3), dtype=np.uint8)
        elif key in [ord(ch) for ch in COLORS.keys()]:
            state["color"] = COLORS[chr(key)]

    if cap is not None:
        cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()