
from ultralytics import YOLO

model = YOLO("yolov8n.pt")                       # small pretrained model
model.train(data="dataset/data.yaml", epochs=50, imgsz=640)
metrics = model.val()                            # prints precision, recall, mAP
print("mAP50:", metrics.box.map50)               # use this real number for your accuracy claim
# Best weights are saved at: runs/detect/train/weights/best.pt
