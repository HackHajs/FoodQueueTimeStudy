import cv2
import asyncio
import numpy as np

from http.server import BaseHTTPRequestHandler, HTTPServer
import socketserver


net = cv2.dnn.readNet("models/yolov3.weights", "models/yolov3.cfg")
layer_names = net.getLayerNames()
output_layers_indices = net.getUnconnectedOutLayers()

if isinstance(output_layers_indices, np.ndarray):
    output_layers_indices = output_layers_indices.flatten()

output_layers = [layer_names[i - 1] for i in output_layers_indices]

with open("models/coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]

video_capture = cv2.VideoCapture(1)

# setup http server
HTTP_PORT = 8000
html = open("src/template.html").read()

# message vars from opencv
npeople = -1
image = None


class FoodQueueServer(BaseHTTPRequestHandler):
    def do_GET(self):
        npeople, image = cv()
        time = (npeople * 30) / 60

        if self.path == "/":
            message = str(npeople) + " people, " + str(time) + " minutes"

            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(
                bytes(html.replace("%MESSAGE%", message), "utf-8"))
        elif self.path == "/queue.jpg":
            self.send_response(200)
            self.send_header("Content-type", "image/jpeg")
            self.end_headers()
            self.wfile.write(bytes(image))
        else:
            self.send_response(404)
            self.end_headers()


async def run_server():
    with socketserver.TCPServer(("", HTTP_PORT), FoodQueueServer) as httpd:
        print("serving at port", HTTP_PORT)
        httpd.serve_forever()


def cv():
    ret, frame = video_capture.read()
    if not ret:
        return None

    height, width, channels = frame.shape

    blob = cv2.dnn.blobFromImage(
        frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False
    )
    net.setInput(blob)
    outputs = net.forward(output_layers)

    boxes = []
    confidences = []
    class_ids = []

    for output in outputs:
        for detection in output:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)

                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

    npeople = 0

    img_encode = cv2.imencode('.jpg', frame)[1]
    data_encode = np.array(img_encode)
    image = data_encode.tobytes()

    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            if label not in ["person"]:
                continue
            npeople += 1
            color = (0, 255, 0)
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            cv2.putText(
                frame, label, (x, y +
                               30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2
            )

    return npeople, image


async def main():
    asyncio.create_task(run_server())
    asyncio.create_task(cv())
    while True:
        await asyncio.sleep(1)

asyncio.run(main())

video_capture.release()
cv2.destroyAllWindows()
