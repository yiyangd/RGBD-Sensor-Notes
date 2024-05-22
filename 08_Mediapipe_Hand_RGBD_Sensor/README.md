## RGBD Sensor Note 08 - Mediapipe
> This note is the 8th in a series of **RGBD Sensors Notes**  documenting an introduction to the **Google Mediapipe library** and how it was deployed on the Realsense sensor to implement the **Hand Landmarker** gesture keypoint tracking task.



### 0. Intro to MediaPipe Solutions
**MediaPipe Solutions** provides a suite of **APIs, libraries models and tools** for developers to use across multiple development platforms:

![](https://files.mdnice.com/user/1474/2c819c52-c84a-4985-b325-43f0bfc1a4e7.png)

### 1. MediaPipe Hand Landmarker Task
#### 1.1. Intro
The **MediaPipe Hand Landmarker Task**  lets you **detect the landmarks of the hands** in an image. You can use this Task to **localize key points of the hands** and **render visual effects over the hands**. 
![](https://files.mdnice.com/user/1474/f26cc518-f061-4b7d-8889-3ba69dc3247d.png)
This task **operates on image data** with a machine learning (ML) model **as static data** or a **continuous stream** and **outputs:** 
- **hand landmarks** in **image coordinates**, 
- **hand landmarks** in **world coordinates**
- **handedness(left/right hand)** of multiple detected hands.

#### 1.2. Model
The **Hand Landmarker** uses a **model bundle** with two packaged models: a **palm detection model** and a **hand landmarks detection model**. 
- The **Palm detection model** locates hands within the input image
- the **hand landmarks detection model** identifies specific hand landmarks on the **cropped hand image defined by the palm detection model**.

![](https://files.mdnice.com/user/1474/b3e90218-d710-4a81-a1f5-ac3a7496ca92.png)

The **hand landmark model** bundle **detects the keypoint localization of 21 hand-knuckle coordinates** within the **detected hand regions**. 
- The model was trained on **approximately 30K real-world images**, as well as **several rendered synthetic hand models** imposed over various backgrounds.
#### 1.3. Install Mediapipe and Model Bundle

Website: https://ai.google.dev/edge/mediapipe/solutions/setup_python

The `latest version` is `0.10.0` in 2023.05.25 
```shell
$ python -m pip install mediapipe
```
### 2. Implement Mediapipe with the Sensor
#### 2.1. Import Libraries
`MediaPipe Tasks` provides three prebuilt libraries for `vision`, `text`, `audio`. 
- The MediaPipe Tasks `vision` module contains tasks that **handle image or video inputs**. 
- To import the MediaPipe Tasks `vision` library, import the following dependency.

```python
import cv2
from RGBDSensor import *
import mediapipe as mp
from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2
import numpy as np
import datetime as dt
```
#### 2.2. Prepare APIs from Mediapipe
```python
# ===== RealSense Configuration =====
sensor = RGBDSensor()

# ===== Mediapipe Configuration =====
BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
HandLandmarkerResult = mp.tasks.vision.HandLandmarkerResult
VisionRunningMode = mp.tasks.vision.RunningMode
```
- `mp.tasks.BaseOptions` represents external model asset used by the Task APIs.
- `mp.tasks.vision.HandLandmarker` performs **hand landmarks detection** on images
- `mp.tasks.vision.HandLandmarkerOptions` set configuration options for the task
- `mp.tasks.vision.HandLandmarkerResult` represents a single hand detected in the image with three attributes:
  - Classification of `handedness`
  - Detected `hand_landmarks` **in normalized image coordinates**
  - Detected `hand_world_landmarks` in **world coordinates**
- `mp.tasks.vision.RunningMode`: `IMAGE`, `VIDEO` and `LIVE_STREAM`
  - Hand Landmarker uses **tracking** in `VIDEO` or `LIVE_STREAM` mode to avoid **triggering palm detection model on every frame**, which helps **reduce latency**.
#### 2.3. Create the Task
The **MediaPipe Hand Landmarker task** uses the `create_from_options` function to set up the task. 
- The `create_from_options` function accepts **values for configuration options to handle**. 
```python
# Create a hand landmarker instance with the image mode:
options = HandLandmarkerOptions(
    base_options=BaseOptions(model_asset_path='hand_landmarker.task'),
    running_mode=VisionRunningMode.IMAGE,
    num_hands=2,
    min_hand_detection_confidence=0.1
)

landmarker = HandLandmarker.create_from_options(options)
```
#### 2.4. Prepare Data
Prepare the input as an **image file** or a **numpy array**, then **convert it to a `mediapipe.Image` object**. 
```python
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
    )
    ### ...
```

#### 2.5. Run the Task
The `Hand Landmarker` uses the `detect`, `detect_for_video` and `detect_async` functions to **trigger inferences** on `IMAGE`, `VIDEO` and `LIVE_STREAM` running mode. 

```python
while True:
    # ... code in 2.4
    # Perform hand landmarks detection on the provided single image.
    # The hand landmarker must be created with the image mode.
    hand_landmarker_result = landmarker.detect(mp_image)
    # ...
```
The **Hand Landmarker** generates a `hand_landmarker_result` object for each detection run. The result object contains 
- hand landmarks in image coordinates
  - There are **21 hand landmarks**, each composed of `x`, `y` and `z` coordinates. 
  - The `x` and `y` coordinates are normalized to `[0.0, 1.0]` by the image width and height, respectively. 
  - The `z` coordinate represents the **landmark depth**, with the **depth at the wrist being the origin**. 
    - The smaller the value, the closer the landmark is to the camera. The magnitude of z uses roughly the same scale as x.
- hand landmarks in world coordinates and 
  - representing **real-world 3D coordinates in meters** with **the origin at the hand’s geometric center**.
- handedness(left/right hand) of the detected hands.

#### 2.6. Visualize
```python
    # Process the classification result. In this case, visualize it.
    annotated_image = draw_landmarks_on_image(mp_image.numpy_view(), hand_landmarker_result)
    #annotated_image = cv2.flip(annotated_image,1)
    cv2.imshow("Hand", cv2.cvtColor(annotated_image, cv2.COLOR_RGB2BGR))
    #cv2.imshow("Image", color_image_rgb)
    if cv2.waitKey(1) == ord('q'):
        break
  
# Release resources and stop the pipeline
cv2.destroyAllWindows()
sensor.release()
```

```python
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
```
#### Resources:  
[1] https://medium.com/@smart-design-techology/hand-detection-in-3d-space-888433a1c1f3      
[2] https://github.com/cansik/realsense-pose-detector     
[3] https://developers.google.com/mediapipe/solutions/vision/hand_landmarker    
[4] https://developers.google.com/mediapipe/solutions/setup_python    
[5] https://developers.google.com/mediapipe/api/solutions/python/mp/tasks/vision  
