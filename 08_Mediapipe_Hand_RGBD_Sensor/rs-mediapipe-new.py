import cv2
from RGBDSensor import *
#from YOLOv8 import *
import numpy as np
import datetime as dt
import mediapipe as mp
from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2

import socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverAddressPort = ("127.0.0.1", 5052)


MARGIN = 10  # pixels
FONT_SIZE = 1
FONT_THICKNESS = 1
HANDEDNESS_TEXT_COLOR = (88, 205, 54) # vibrant green

def draw_landmarks_on_image(rgb_image, hand_landmarker_result):
    # Extracts the landmarks of the detected hands 
    # and their handedness from the detection result.
    hand_landmarks_list = hand_landmarker_result.hand_landmarks
    handedness_list = hand_landmarker_result.handedness
    #print(hand_landmarks_list)
    # Creates a copy of the original image on which we will draw the landmarks.
    annotated_image = np.copy(rgb_image)
    # Checks if any hand landmarks were detected
    if len(hand_landmarks_list) == 0:
        #annotated_image = cv2.flip(annotated_image,1)
        return annotated_image
    # Loop through the detected hands to visualize.
    for idx in range(len(hand_landmarks_list)):
        # Extracts the landmarks and handedness for the current hand
        hand_landmarks = hand_landmarks_list[idx]
        handedness = handedness_list[idx]

        # Draw the hand landmarks.
        hand_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
        hand_landmarks_proto.landmark.extend([
            landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z) for landmark in hand_landmarks
        ])
        solutions.drawing_utils.draw_landmarks(
            annotated_image,
            hand_landmarks_proto,
            solutions.hands.HAND_CONNECTIONS,
            solutions.drawing_styles.get_default_hand_landmarks_style(),
            solutions.drawing_styles.get_default_hand_connections_style()
        )
    # The image is flipped along the vertical axis before being returned 
    # to make it more visually intuitive for the viewer (as if they're looking in a mirror).
    # annotated_image = cv2.flip(annotated_image, 1)
    for idx in range(len(hand_landmarks_list)):
        hand_landmarks = hand_landmarks_list[idx]
        handedness = handedness_list[idx]
        height, width, _ = annotated_image.shape
        # Calculates the top left corner of the bounding box of the hand in the image. 
        # The top left corner is calculated using the maximum x-coordinate and minimum y-coordinate among the hand landmarks.
        x_coordinates = [landmark.x for landmark in hand_landmarks]
        if idx == 0:
            print(x_coordinates)
        y_coordinates = [landmark.y for landmark in hand_landmarks]
        text_x = width - int(max(x_coordinates) * width)
        text_y = int(min(y_coordinates) * height) - MARGIN
        # Puts the handedness text at the calculated position in the image 
        cv2.putText(annotated_image, f"{handedness[0].category_name}",
                    (text_x, text_y), cv2.FONT_HERSHEY_DUPLEX,
                    FONT_SIZE, HANDEDNESS_TEXT_COLOR, FONT_THICKNESS, cv2.LINE_AA)     
    

    return annotated_image

########
# ===== RealSense Configuration =====
sensor = RGBDSensor()

# ===== Mediapipe Configuration =====
BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
HandLandmarkerResult = mp.tasks.vision.HandLandmarkerResult
VisionRunningMode = mp.tasks.vision.RunningMode

# Create a hand landmarker instance with the image mode:
options = HandLandmarkerOptions(
    base_options=BaseOptions(model_asset_path='hand_landmarker.task'),
    running_mode=VisionRunningMode.IMAGE,
    num_hands=2,
    min_hand_detection_confidence=0.1
)

landmarker = HandLandmarker.create_from_options(options)


# Create a loop to read the latest frame from the sensor
while True:
    color_image, depth_image, depth_frame = sensor.get_images()
    (h,w,_) = color_image.shape # h = 480, 640
    depth_pcd = sensor.get_point_cloud(depth_frame)
    depth_pcd[:, :, 1] = -depth_pcd[:, :, 1] 
    # Convert color_image from frame to a MediaPipe’s Image object.
    # color_image = cv2.flip(color_image,1)
    color_image_rgb = cv2.cvtColor(color_image, cv2.COLOR_BGR2RGB)

    mp_image = mp.Image(
        image_format=mp.ImageFormat.SRGB, 
        data=color_image_rgb
    )   # mp_image.height = 480, mp_image.width = 640
    #import pdb; pdb.set_trace()

    # Perform hand landmarks detection on the provided single image.
    # The hand landmarker must be created with the image mode.
    hand_landmarker_result = landmarker.detect(mp_image)

    #import pdb; pdb.set_trace()
    #if (hand_landmarker_result.hand_world_landmarks):
    #    print(hand_landmarker_result.hand_world_landmarks[0][0].x)
    data = []
    if len(hand_landmarker_result.hand_landmarks) > 0:
        landmarks = hand_landmarker_result.hand_landmarks[0]
        # import pdb; pdb.set_trace()
        for i_mark, landmark in enumerate(landmarks):
            img_x, img_y = landmark.x, landmark.y
            img_x, img_y = int(img_x* 640) , int(img_y* 480)
            if img_x < 640 and img_y < 480:
                data.extend(depth_pcd[img_y, img_x].tolist())
            else:
                data.extend([0,0,0])
        data = [i * 100 for i in data]
        data = [round(x,2) for x in data]
        sock.sendto(str.encode(str(data)), serverAddressPort)
    else:
        data = [0] * 63
        sock.sendto(str.encode(str(data)), serverAddressPort)
    
    # STEP 5: Process the classification result. In this case, visualize it.
    annotated_image = draw_landmarks_on_image(mp_image.numpy_view(), hand_landmarker_result)
    
    #annotated_image = cv2.flip(annotated_image,1)

    cv2.imshow("Hand", cv2.cvtColor(annotated_image, cv2.COLOR_RGB2BGR))
    #cv2.imshow("Image", color_image_rgb)
    if cv2.waitKey(1) == ord('q'):
        break
    

# Release resources and stop the pipeline
cv2.destroyAllWindows()
sensor.release()
    
