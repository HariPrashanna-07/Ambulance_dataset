# 🚑 AutoSignal

An AI-powered Intelligent Traffic Signal Priority System that detects ambulances in real time using YOLOv8 and automatically provides a green signal to reduce emergency response time.

---

## 📌 Overview

AutoSignal uses computer vision to monitor traffic intersections and identify approaching ambulances. Once detected, the system communicates with an ESP32 traffic controller to switch the corresponding traffic signal to green while keeping all other directions red. After the ambulance passes, the traffic lights return to their normal operating cycle.

---

## ✨ Features

- 🚑 Real-time ambulance detection using YOLOv8
- 📹 Live webcam/video processing
- 🎯 High-confidence object detection
- 🔄 Automatic traffic signal prioritization
- 📡 Python-to-ESP32 serial communication
- ⚡ Low-latency inference
- 📊 Detection logging
- 🖥️ Easy integration with CCTV cameras

---

## 🛠️ Tech Stack

| Category | Technology |
|----------|------------|
| Language | Python |
| AI Model | YOLOv8 |
| Computer Vision | OpenCV |
| Deep Learning | PyTorch |
| Hardware | ESP32 |
| Communication | Serial (UART) |
| IDE | VS Code |

---

## 📂 Project Structure

```
AutoSignal
│
├── models/
│   └── best.pt
│
├── detection/
│   ├── detect.py
│   ├── tracker.py
│   └── utils.py
│
├── controller/
│   ├── serial_controller.py
│   └── esp32/
│       └── traffic_controller.ino
│
├── videos/
│
├── outputs/
│
├── requirements.txt
│
├── README.md
│
└── main.py
```

---

## ⚙️ Workflow

```
Camera
   │
   ▼
YOLOv8 Detection
   │
   ▼
Ambulance Detected?
   │
   ├── No → Continue Monitoring
   │
   ▼
Calculate Confidence
   │
   ▼
Send Command to ESP32
   │
   ▼
Traffic Signal Turns Green
   │
   ▼
Ambulance Crosses Junction
   │
   ▼
Restore Normal Traffic Cycle
```

---

## 🧠 How It Works

1. Live video is captured from a webcam or CCTV camera.
2. YOLOv8 detects vehicles in every frame.
3. If an ambulance is detected with confidence above the threshold, a trigger is generated.
4. Python sends a command through serial communication to the ESP32.
5. ESP32 changes the traffic lights.
6. After the ambulance passes, the system resumes the normal traffic sequence.

---

## 📥 Installation

Clone the repository

```bash
git clone https://github.com/yourusername/AutoSignal.git

cd AutoSignal
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run

```bash
python main.py
```

---

## 🧰 Requirements

- Python 3.10+
- OpenCV
- Ultralytics
- PyTorch
- PySerial
- NumPy

Install manually

```bash
pip install ultralytics opencv-python torch torchvision pyserial numpy
```

---

## 📷 Sample Output

```
Ambulance Detected
Confidence : 97.4%

Road 2 → GREEN
Road 1 → RED
Road 3 → RED
Road 4 → RED
```

---

## 🔮 Future Improvements

- Multi-camera support
- GPS integration
- LoRa communication
- Firebase dashboard
- Vehicle tracking using ByteTrack
- Distance estimation
- Emergency vehicle classification
- Cloud monitoring
- Traffic analytics dashboard



---

## 📜 License

This project is licensed under the MIT License.
