# Step 2: Run on laptop/Raspberry Pi with a camera. Tells the ESP32 what to do.
import os, time, cv2, requests
from ultralytics import YOLO

ESP32_IP = "192.168.1.50"          # <-- change to your ESP32's IP (shown in Serial Monitor)
MODEL_PATH = "runs/detect/train/weights/best.pt"
CONF = 0.6                          # minimum confidence
NEED_FRAMES = 3                     # detect in 3 frames in a row to avoid false alarms
BOX_HEIGHT_NEAR = 150               # bbox height (pixels) treated as "close enough" - tune this
GEMINI_KEY = os.getenv("GEMINI_API_KEY")   # optional, for the report

model = YOLO(MODEL_PATH)
cap = cv2.VideoCapture(0)           # 0 = webcam, or a video file / IP camera URL
hits, active = 0, False

def send(path):
    try:
        requests.get(f"http://{ESP32_IP}/{path}", timeout=1)
    except requests.RequestException:
        print("ESP32 not reachable")

def gemini_report():
    if not GEMINI_KEY: return
    url = ("https://generativelanguage.googleapis.com/v1beta/models/"
           f"gemini-2.5-flash:generateContent?key={GEMINI_KEY}")
    prompt = (f"Write a 3-line traffic incident report. Event: ambulance detected, "
              f"green corridor given. Time: {time.ctime()}.")
    r = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]}, timeout=15)
    print(r.json()["candidates"][0]["content"]["parts"][0]["text"])

while True:
    ok, frame = cap.read()
    if not ok: break

    found = False
    for box in model(frame, conf=CONF, verbose=False)[0].boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        if (y2 - y1) >= BOX_HEIGHT_NEAR:          # big box = ambulance is close
            found = True
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(frame, "AMBULANCE", (x1, y1 - 8), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    hits = hits + 1 if found else 0
    if hits >= NEED_FRAMES and not active:
        send("ambulance"); active = True; gemini_report()
    elif hits == 0 and active:
        time.sleep(3)                             # hold green a bit while it passes
        send("normal"); active = False

    cv2.imshow("Ambulance Detection", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"): break

cap.release(); cv2.destroyAllWindows()
