import cv2
from RGBDSensor import *

# Initialize RGBD Sensor
sensor = RGBDSensor()

point = (0, 0)
# mouse callback function
def get_depth_by_mouse(event, x, y, flags, params):
    global point
    point = (x, y)
# Create mouse event
cv2.namedWindow("Color image")
cv2.setMouseCallback("Color image", get_depth_by_mouse)

while True:
    color_image, depth_image = sensor.get_images()

    # Show distance for a specific point
    cv2.circle(color_image, point, 4, (0, 0, 255))
    distance = depth_image[point[1], point[0]]

    cv2.putText(color_image, "{}mm".format(distance), 
                (point[0], point[1] - 20), 
                cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)

    # Apply color map to depth image for visualization
    depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.3), 
                                       cv2.COLORMAP_JET)
    # Display RGB and depth images
    cv2.imshow('Color image', color_image)
    cv2.imshow('Depth image', depth_colormap)

    if cv2.waitKey(1) == ord('q'):
        break

# Release resources and stop the pipeline
cv2.destroyAllWindows()
sensor.release()
