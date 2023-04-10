import pyrealsense2 as rs
import numpy as np
import cv2
import matplotlib.pyplot as plt

def plotHeatmap(depth_image):
    # 提取深度值矩阵
    depth_matrix = np.zeros((480, 640))
    for y in range(480):
        for x in range(640):
            depth_matrix[y, x] = depth_image[y, x] / 10  # convert mm to cm

    # 可视化深度值矩阵
    fig, ax = plt.subplots()
    heatmap = ax.imshow(depth_matrix, cmap='jet', vmin=0, vmax=200)
    cbar = ax.figure.colorbar(heatmap, ax=ax)
    cbar.ax.set_ylabel('Depth (cm)', rotation=-90, va="bottom")
    plt.show()


def depthOfCenter(depth_frame):
    width = depth_frame.get_width()
    height = depth_frame.get_height()
    depth = depth_frame.get_distance(int(width/2),int(height/2))
    print("The sensor is facing an object", depth, " meters away")


# Create a RealSense pipeline object
pipeline = rs.pipeline()

# Create a RealSense configuration object and set the resolution and frame rate
config = rs.config()
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)

# Start the pipeline and get the color and depth sensor objects
pipeline.start(config)

color_sensor = pipeline.get_active_profile().get_device().query_sensors()[1]

# Set the exposure and gain values for the color sensor
color_sensor.set_option(rs.option.exposure, 1000)
color_sensor.set_option(rs.option.gain, 32)
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

    # Apply color map to depth image for visualization
    depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.1), cv2.COLORMAP_JET)

    # Display RGB and depth images
    cv2.imshow('Color image', color_image)
    cv2.imshow('Depth image', depth_colormap)

    plotHeatmap(depth_image)
    depthOfCenter(depth_frame)

    # Exit the loop when 'q' key is pressed
    if cv2.waitKey(1) == ord('q'):
        break

# Release resources and stop the pipeline
cv2.destroyAllWindows()
pipeline.stop()










