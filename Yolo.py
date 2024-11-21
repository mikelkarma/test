# pip install ultralytics opencv-python
import cv2
from ultralytics import YOLO
import threading

def captura_video(ip, frame_queue):
    video = cv2.VideoCapture(ip)
    while video.isOpened():
        ret, frame = video.read()
        if not ret:
            break
        if frame_queue.full():
            frame_queue.get()
        frame_queue.put(frame)
    video.release()

def processamento_yolo(frame_queue, model):
    while True:
        if not frame_queue.empty():
            frame = frame_queue.get()
            results = model(frame)
            results.render()
            cv2.imshow("Detecção com YOLO", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

def gerar_video(label, ip="http://192.168.10.150:8080/video"):
    model = YOLO("yolov8n.pt")
    frame_queue = cv2.Queue(maxsize=10)
    
    captura_thread = threading.Thread(target=captura_video, args=(ip, frame_queue))
    processamento_thread = threading.Thread(target=processamento_yolo, args=(frame_queue, model))

    captura_thread.start()
    processamento_thread.start()

    captura_thread.join()
    processamento_thread.join()

    cv2.destroyAllWindows()

gerar_video("Detecção com YOLO")
