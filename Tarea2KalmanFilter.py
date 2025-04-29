import cv2
import numpy as np
import torch
from ultralytics import YOLO

from sort import Sort, convert_x_to_bbox

torch.backends.cudnn.enabled = False

VIDEO = "modulo_4/Prueba2.mp4"
model = YOLO("yolov8m.pt").to("cuda")
tracker = Sort(max_age=30, min_hits=15, iou_threshold=0.3)

cap = cv2.VideoCapture(VIDEO)
while True:
    ok, frame = cap.read()
    if not ok:
        print("Fin del video")
        break

    # detección
    res = model(frame, conf=0.65, verbose=False)[0]
    dets = res.boxes.data.cpu().numpy()[:, :5] if res.boxes else np.empty((0, 5))

    # tracking
    for x1, y1, x2, y2, _, tid in tracker.update(dets).astype(int):
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(
            frame,
            f"ID {tid}",
            (x1, y1 - 5),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 0),
            2,
        )

    # pred Kalman (caja amarilla)
    for trk in tracker.trackers:
        px1, py1, px2, py2 = convert_x_to_bbox(trk.kf.x)[0].astype(int)

        cv2.rectangle(frame, (px1, py1), (px2, py2), (0, 255, 255), 1, cv2.LINE_4)

        cv2.putText(
            frame,
            f"ID {trk.id + 1} (pred)",
            (px1, py1 - 6),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 255, 255),
            1,
        )

    cv2.imshow("YOLOv8 + Kalman SORT", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
