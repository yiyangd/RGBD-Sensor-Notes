from ultralytics import YOLO
import numpy as np
import cv2
class YOLOv8:
    def __init__(self, model):
        self.model = YOLO(model)
        # Generate Random Colors
        np.random.seed(2)
        self.colors = np.random.randint(0,255, (90,3))
        
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
    
    
    def draw_masks(self, img, masks, classes):   
        img_copy = np.zeros_like(img)
        for mask, class_id in zip(masks, classes):
            color = self.colors[class_id]
            cv2.polylines(img, [mask], True, (int(color[0]),int(color[1]),int(color[2])), 4)
            cv2.fillPoly(img_copy, [mask], (int(color[0]),int(color[1]),int(color[2])))
            img = cv2.addWeighted(img, 1, img_copy, 0.3, 0)
        return img
        
    
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