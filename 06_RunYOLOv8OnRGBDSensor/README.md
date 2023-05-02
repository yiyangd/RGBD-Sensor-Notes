# RGBD Sensor Note 06 | Run YOLOv8 on RealSense
> This is the 6th article in the "RGBD Sensor Notes" series, documenting how to run the YOLOv8 computer vision algorithm on the Intel RealSense D435i depth sensor for real-time object detection and segmentation.
> - [Code]()
> - [Video](https://youtu.be/1NZR5wN5G9A)

### Step 1. Code Refactoring
Refactor the code from [Computer-Vision-Note 03](https://github.com/yiyangd/Computer-Vision-Notes/blob/main/03_YOLOv8_Detection_Segmentation/yolov8_detect_segment.py) into `YOLOv8.py`
#### 1.1. class YOLOv8(model)
`__init__(self, model)` is an initialization method that takes a `pre-trained model` as an argument. 
- It creates a YOLO model instance and generates a random array of 90 colors (to be used in subsequent drawing operations).
```py
from ultralytics import YOLO
import numpy as np
import cv2
class YOLOv8:
    def __init__(self, model):
        self.model = YOLO(model)
        # Generate Random Colors
        np.random.seed(2)
        self.colors = np.random.randint(0,255, (90,3))
```
#### 1.2. yolo.run()
Performs object detection on the input image. It takes an image and predicts using the YOLOv8 model. 
- It returns `bounding boxes`, `classes`, `confidence scores`, and optional `masks` (if available) from the prediction results.
```py
def run(self, img):
    # Prediction
    results = self.model.predict(img, 
                    conf=0.4, 
                    show=True, 
                    save=True, 
                    save_crop=True 
                    )
    # Working with Results
    result = results[0]
    self.names = result.names

    boxes = np.array(result.boxes.xyxy.cpu(), dtype="int") # boxes with xyxy format, (N, 4)
    classes = np.array(result.boxes.cls.cpu(), dtype="int") # classes for N boxes, (N, 1)
    scores = np.array(result.boxes.conf.cpu(), dtype="float").round(2) # confidence score, (N, 1)
    masks = []
    if result.masks is not None:
        for mask in result.masks.xy:
            mask = np.array(mask,dtype=np.int32)
            masks.append(mask)

    return boxes, classes, scores, masks
```
#### 1.3. yolo.draw_masks()
Draws predicted `masks` on the input image. 
- It takes the image, masks, and classes as input, generates a color for each mask, and draws it on the image. 
- Returns the image with masks drawn.

```py
def draw_masks(self, img, masks, classes):   
    img_copy = np.zeros_like(img)
    for mask, class_id in zip(masks, classes):
        color = self.colors[class_id]
        cv2.polylines(img, [mask], True, (int(color[0]),int(color[1]),int(color[2])), 4)
        cv2.fillPoly(img_copy, [mask], (int(color[0]),int(color[1]),int(color[2])))
        img = cv2.addWeighted(img, 1, img_copy, 0.3, 0)
    return img
```
#### 1.4. yolo.draw_boxes()
Draws predicted `bounding boxes` and **related information** on the input image. 
- It takes the `image, depth, bounding boxes, classes, and confidence scores` as input. 
- Then, it **draws a rectangle around each bounding box** and adds the **corresponding labels** (including class, confidence score, and depth information). 
- Returns the image with bounding boxes and labels drawn.

```py
def draw_boxes(self, img, depth, boxes, classes, scores):
    for box, class_id, score in zip(boxes, classes, scores):
        color = self.colors[class_id]

        (left, top, right, bottom) = box

        center_x = (left + right) // 2
        center_y = (top + bottom) // 2
        depth_mm = depth[center_y, center_x]
        cv2.rectangle(img = img, 
            pt1 = (left, top), 
            pt2 = (right, bottom), 
            color = (int(color[2]),int(color[1]),int(color[0])), 
            thickness = 2)     

        cv2.putText(img = img, 
            text = str(self.names[class_id]) + " " + str(score), 
            org = (left + 10, top - 25), 
            fontFace = cv2.FONT_HERSHEY_SIMPLEX, 
            fontScale = 0.7, 
            color = (int(color[0]),int(color[2]),int(color[1])), 
            thickness = 2)

        cv2.putText(img = img, 
            text = "{} cm".format(depth_mm / 10), 
            org = (left + 10, top - 5), 
            fontFace = cv2.FONT_HERSHEY_SIMPLEX, 
            fontScale = 0.7, 
            color = (int(color[0]),int(color[2]),int(color[1])), 
            thickness = 2)
    return img
```

### Step 2. Open Sensor and Run YOLOv8 in main.py

```py
import cv2
from RGBDSensor import *
from YOLOv8 import *
# Initialize RGBD Sensor and YOLO Model
sensor = RGBDSensor()
yolo = YOLOv8("yolov8m-seg.pt")

while True:
    color_image, depth_image = sensor.get_images()
    boxes, classes, scores, masks = yolo.run(color_image)

    color_image = yolo.draw_masks(color_image, masks, classes)
    color_image = yolo.draw_boxes(color_image, depth_image, boxes, classes, scores)

    # Apply color map to depth image for visualization
    depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.3), 
                                    cv2.COLORMAP_JET)
    # Display RGB and depth images
    rgbd_img = np.concatenate((color_image,depth_colormap), axis=1)
    cv2.imshow("RGB-Depth Image", rgbd_img)
    if cv2.waitKey(1) == ord('q'):
        break

# Release resources and stop the pipeline
cv2.destroyAllWindows()
sensor.release()
```
