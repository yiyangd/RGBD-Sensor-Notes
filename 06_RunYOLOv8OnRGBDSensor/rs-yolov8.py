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