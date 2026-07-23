import cv2
from datetime import datetime
from risk_engine import add_event, get_score, get_risk_level

# ----------------------------------------
# Log File
# ----------------------------------------

LOG_FILE = "events.log"


def log_event(message):
    with open(LOG_FILE, "a") as file:
        file.write(message + "\n")


# ----------------------------------------
# Load Haar Cascade
# ----------------------------------------

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

if face_cascade.empty():
    print("❌ Error loading Haar Cascade!")
    exit()

# ----------------------------------------
# Start Webcam
# ----------------------------------------

camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("❌ Unable to access webcam.")
    exit()

# ----------------------------------------
# Variables
# ----------------------------------------

face_present = True
absence_start = None

print("========================================")
print(" AI Face Monitoring Started")
print(" Press Q to Quit")
print("========================================")

# ----------------------------------------
# Main Loop
# ----------------------------------------

while True:

    success, frame = camera.read()

    if not success:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.3,
        minNeighbors=5
    )

    # ----------------------------------------
    # Face Missing
    # ----------------------------------------

    if len(faces) == 0:

        if face_present:

            face_present = False
            absence_start = datetime.now()

        
            message = f"[{absence_start.strftime('%Y-%m-%d %H:%M:%S')}] Face Missing"
            

            print(message)
            log_event(message)

            add_event("Face Missing", 2)

            print("--------------------------------")
            print("Risk Score :", get_score())
            print("Risk Level :", get_risk_level())
            print("--------------------------------")

        cv2.putText(
            frame,
            "FACE NOT DETECTED",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 255),
            2
        )

    # ----------------------------------------
    # Face Returned
    # ----------------------------------------

    else:

        if not face_present:

            face_present = True
            absence_end = datetime.now()

            duration = (
                absence_end - absence_start
            ).total_seconds()

            message = f"[{absence_end.strftime('%Y-%m-%d %H:%M:%S')}] Face Returned | Absent: {duration:.2f} sec"

            print(message)
            log_event(message)

        cv2.putText(
            frame,
            "FACE DETECTED",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )

    # ----------------------------------------
    # Draw Rectangle Around Face
    # ----------------------------------------

    for (x, y, w, h) in faces:

        cv2.rectangle(
            frame,
            (x, y),
            (x + w, y + h),
            (0, 255, 0),
            2
        )

    # ----------------------------------------
    # Show Camera
    # ----------------------------------------

    cv2.imshow("Online Exam Face Monitoring", frame)

    # Press Q to Exit

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# ----------------------------------------
# Cleanup
# ----------------------------------------

camera.release()
cv2.destroyAllWindows()
