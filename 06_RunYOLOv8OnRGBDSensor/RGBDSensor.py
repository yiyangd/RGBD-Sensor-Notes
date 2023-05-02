import pyrealsense2 as rs
import numpy as np

class RGBDSensor:
    def __init__(self):
        # Create a RealSense pipeline object
        self.pipeline = rs.pipeline()

        # Create a RealSense configuration object and set the resolution and frame rate
        config = rs.config()
        config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 15)
        config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 15)
        # Start the pipeline and get the color and depth sensor objects
        self.pipeline.start(config)
        
        # Set the exposure and gain values for the color sensor
        self.color_sensor = self.pipeline.get_active_profile().get_device().query_sensors()[1]
        self.color_sensor.set_option(rs.option.exposure, 1000)
        self.color_sensor.set_option(rs.option.gain, 32)
        # Create alignment object
        self.align = rs.align(rs.stream.color)

    def get_images(self):
        # Wait for RealSense data streams
        frames = self.pipeline.wait_for_frames()
        aligned_frames = self.align.process(frames)
        
        # Get color and depth frames
        color_frame = aligned_frames.get_color_frame()
        depth_frame = aligned_frames.get_depth_frame()
        
        # If there are no valid frames, continue waiting for the next one
        if not color_frame or not depth_frame:
            return None, None
        
        # Apply filter to fill the Holes in the depth image
        spatial = rs.spatial_filter()
        spatial.set_option(rs.option.holes_fill, 3)
        filtered_depth = spatial.process(depth_frame)

        hole_filling = rs.hole_filling_filter()
        filled_depth = hole_filling.process(filtered_depth)

        # Convert color and depth data to NumPy arrays
        color_image = np.asanyarray(color_frame.get_data())
        depth_image = np.asanyarray(depth_frame.get_data())
        
        return color_image, depth_image

    def release(self):
        self.pipeline.stop()