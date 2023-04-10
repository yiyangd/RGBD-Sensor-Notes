# 深度传感器笔记04 用Python打开传感器并测量距离
> 此篇笔记是「深度传感器」笔记系列的第4篇，记录了如何通过Python连接并打开RealSense深度传感器的摄像头，同时获得RGB和Depth数据
> - Video: https://youtu.be/6rwpmGlqzEE
### Step 1. Import Libraries
```py
import pyrealsense 2 as rs
import numpy as np
import cv2
```

### Step 2. Create RealSense Pipeline
Pipeline is the primary high level primitive controlling camera enumeration and streaming.
```py
pipeline = rs.pipeline()
```

### Step 3. Configuration Setting and Start Pipeline
Enable color and depth streams with a resolution of `640x480`, format of `bgr8` for color and `z16` for depth, and a frame rate of `30 fps`
- increasing the resolution and frame rate may affect camera performance, so we should balance our needs against hardware limitations.
```py
# Create a RealSense configuration object and set the resolution and frame rate
config = rs.config()

config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)

# Start the Pipeline
pipeline.start(config)
```

### Step 4. Set the exposure and gain values for the color sensor (Optional)
```py
# Set the exposure and gain values for the color sensor
color_sensor = pipeline.get_active_profile().get_device().query_sensors()[1]

color_sensor.set_option(rs.option.exposure, 1000)
color_sensor.set_option(rs.option.gain, 8)
```
Exposure is a camera parameter that controls the amount of time that the camera's shutter is open, allowing light to enter and hit the camera's image sensor. 
- Longer exposure times allow more light to enter the camera, resulting in brighter images, while shorter exposure times allow less light to enter, resulting in darker images.

In RealSense cameras, gain is a parameter that **controls the amplification of the camera's analog signal** before it is digitized into a digital image.
- increasing the gain too much can also introduce noise into the image, which can reduce the overall image quality

### Step 5. Loop through Aligned frames
```py
# Create alignment object
align = rs.align(rs.stream.color)

# Loop through frames and get color and depth data
while True:
    # Wait for RealSense data streams
    frames = pipeline.wait_for_frames()
    aligned_frames = align.process(frames)

    # Get color and depth frames
    color_frame = aligned_frames.get_color_frame()
    depth_frame = aligned_frames.get_depth_frame()

    # If there are no valid frames, continue waiting for the next one
    if not color_frame or not depth_frame:
        continue

    # Convert color and depth data to NumPy arrays
    color_image = np.asanyarray(color_frame.get_data())
    depth_image = np.asanyarray(depth_frame.get_data())

    #plotHeatmap(depth_image)

    # Apply color map to depth image for visualization
    depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.15), cv2.COLORMAP_JET)

    # Display RGB and depth images
    cv2.imshow('Color image', color_image)
    cv2.imshow('Depth image', depth_colormap)

    #depthOfCenter(depth_frame)
    # Exit the loop when 'q' key is pressed
    if cv2.waitKey(1) == ord('q'):
        break
```

### Step 6. Stop the Pipeline
```py
# Release resources and stop the pipeline
cv2.destroyAllWindows()
pipeline.stop()
```

### (Optional) Plot the Heatmap and Get Depth Data of the Center
```py
def depthOfCenter(depth_frame):
    width = depth_frame.get_width()
    height = depth_frame.get_height()
    depth = depth_frame.get_distance(int(width/2),int(height/2))
    print("The sensor is facing an object", depth, " meters away")
def plotHeatmap(depth_image):
    depth_matrix = np.zeros((480, 640))
    for y in range(480):
        for x in range(640):
            depth_matrix[y, x] = depth_image[y, x] / 10  # convert mm to cm

    fig, ax = plt.subplots()
    heatmap = ax.imshow(depth_matrix, cmap='jet', vmin=0, vmax=200)
    cbar = ax.figure.colorbar(heatmap, ax=ax)
    cbar.ax.set_ylabel('Depth (cm)', rotation=-90, va="bottom")
    plt.show()

```

#### Resources:
- https://dev.intelrealsense.com/docs/python2
