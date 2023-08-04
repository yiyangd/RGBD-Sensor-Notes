## RGBD Sensor Note 09 | Intro Luxonis, DepthAI and OAK-D Camera
> This note is the 9th in the series of RGBD Sensor Notes, documenting the introduction to the Luxonis platform and the OAK depth camera, as well as how to complete an implementation of an object recognition task using DepthAI APIs.
> - Demo: https://youtu.be/pYx9zhSR9Io
> - Code: https://github.com/yiyangd/RGBD-Sensor-Notes/

### 1. Luxonis Platform[1]

![https://www.luxonis.com/](https://files.mdnice.com/user/1474/f827a3a3-6916-474f-92c3-7bc724f6c74c.png)

**Luxonis** is a **Spatial AI and CV platform**, which **allows robots and computers to perceive the world like a human** can - **what objects or features are** - and **where they are in physical world**   
**Luxonis**是一个**空间AI和计算机视觉平台**，能**让机器人和计算机像人类一样感知世界**--**物体或其特征是什么**，以及它们**在物理世界中的位置**
- by building and maintaining the **open-source DepthAI ecosystem** to **fuse AI capabilities with depth perception** on the **OAK camera**     
并且开发和维护开源的DepthAI生态系统**将AI功能**与 **OAK摄像机**本身的**深度感知相融合**  

![https://docs.luxonis.com/projects/hardware/en/latest/](https://files.mdnice.com/user/1474/cb3e2615-d937-413e-9a5d-1033ec037c2f.png)

### 2. DepthAI API Docs Overview[2]
**DepthAI API** allows users to **connect** to, **configure** and **communicate** with their OAK devices  
**DepthAI API** 允许用户**连接**、**配置** OAK 设备并与其**通信**

![https://docs.luxonis.com/projects/api/en/latest/](https://docs.luxonis.com/projects/api/en/latest/_images/api_diagram.png)

- `Host` side is a **computer, like PC or RPi**, to which **an OAK device is connected**.
- `Device` side is the **OAK device itself**. If something is happening on the device side, it means that it’s running on the **Robotics Vision Core (RVC)**.
- `Pipeline` is a **complete workflow on the device side**, consisting of **nodes and connections** between them. 
- `Node` is a **single functionality** of the DepthAI. Nodes have **inputs or outputs**, and have **configurable properties**.

![https://docs.luxonis.com/projects/api/en/latest/references/python/#module-depthai.node](https://files.mdnice.com/user/1474/207e8b66-1c31-4d27-9445-d73f950928ba.png)

- `Connection` is a `link` between one **node’s output** and **another one’s input**. 
  - In order to define the `pipeline` dataflow, the `connections` define where to **send messages** in order to achieve an expected result
- `XLink` is a **middleware that is capable to exchange data between `Device` and `Host`**. 
  - `XLinkIn` node allows **sending the data from the `Host` to a `Device`**, while `XLinkOut` does the opposite.
- `Messages` are **transferred between linked Nodes**, as defined by a `Connection`.

### 3. Implement an Object Detection Task by using DepthAI APIs

#### 3.1. Create a Empty Pipeline[3]
**Pipeline** is **a collection of nodes and links** between them.
-  This **flow** provides an **extensive flexibility** that users get for their **OAK device**. 
- When `pipeline` object is **passed to** the `Device` object, `pipeline` gets **serialized to JSON** and **sent to the OAK device** via `XLink`.
- When starting an OAK `Device`, we need to create a `pipeline`, including `nodes` and `connections` which will get executed on the **VPU(vision processing unit)**

```python
import depthai as dai
# Pipeline tells DepthAI what operations to perform when running - you define all of the resources used and flows here
pipeline = dai.pipeline()
```
#### 3.2. Create a ColorCamera Node[4]


```python
# Set ColorCamera Node as the Output
cam_rgb = pipeline.create(depthai.node.ColorCamera)
```

`ColorCamera` Node is a source of `ImgFrame` Messages, which can be controlled at runtime with the `InputControl` and `InputConfig`

![](https://files.mdnice.com/user/1474/f496679c-a67c-4b61-b6b1-fb74d8ff1fac.png)

- **ISP (image signal processor)** is used for **bayer transformation**, **demosaicing**, **noise reduction**, and other **image enhancements**. 
  - It interacts with the 3A algorithms: **auto-focus**, **auto-exposure**, and **auto-white-balance**, 
  - which are **handling Image Sensor adjustments** such as **exposure time**, **sensitivity (ISO)**, and **lens position** (if the camera module has a **motorized lens**) at runtime. 
- **Image Post-Processing** converts **image frames**(Input) from the **ISP** into `video`/`preview`/`still`  Frames(Output)

![`isp` Output from the ColorCamera](https://files.mdnice.com/user/1474/5f463ac9-6875-45f6-85c6-87b3088ed90b.png)

- If we aren’t **downscaling ISP**, the `video` output is **cropped to 4k (max 3840x2160** due to the limitation). 
- The $\color{orange}\text{Yellow Rectangle}$ represents a cropped `preview` output when **the preview size is set to a 1:1 aspect ratio** (eg. when using a `300x300 preview size` for the **MobileNet-SSD NN model**) because the `preview` output is derived from the `video` output.



```python
# Set preview output size, as a tuple <width, height>
cam_rgb.setPreviewSize(300, 300) 
# Select the camera sensor resolution (1080P..4K)
cam_rgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_1080_P) 
# Set planar or interleaved data of preview output frames
cam_rgb.setInterleaved(False) 
```

#### 3.3. Create a Network Node[5]
```python
# Set a Network Node to detect 
detection_nn = pipeline.create(depthai.node.MobileNetDetectionNetwork)
```

`MobileNet Detection Network` Node **runs neural inference** on input data, **decodes the result of the NN on device**
- this means that `output message` of this node is NOT a byte array but a `ImgDetections`[6] which contains a list of `detections`  (`label`, `confidence`, and the bounding box information(`xmin`, `ymin`, `xmax`, `ymax`))

```python
# Blob is the Neural Network file, compiled for MyriadX. It contains both the definition and weights of the model
# Use blobconverter to Convert NN to MyriadX blob file
import blobconverter  
# Load network blob into assets and use once pipeline is started.
detection_nn.setBlobPath(blobconverter.from_zoo(name='mobilenet-ssd', shaves=6))
# Or Set path of the blob (NN model). 
#detection_nn.setBlobPath("/path/to/model.blob")
# Set the confidence threshold to filter out the incorrect results
detection_nn.setConfidenceThreshold(0.5)
```
- `blobconverter.from_zoo(name='model-name')` function **returns Path** to the model, so we can directly put it inside the **detection_nn.setBlobPath() function**.
- With this Node, the **output from nn** will **be parsed on device side** and we’ll **receive a ready to use detection objects**

#### 3.4. Connect/Link TWO Nodes
Connect the  `preview` (Output) of `ColorCamera` Node to `detection_nn` Input.

```python
cam_rgb.preview.link(detection_nn.input)
```
#### 3.5. Use `XlinkOut` Node
`XLinkOut` Node is used to **send data from the `device` to the `host`** via `XLink`.

```python
# Send camera preview (ImgFrame) to the host via XLink
xout_rgb = pipeline.create(depthai.node.XLinkOut)
xout_rgb.setStreamName("rgb")
cam_rgb.preview.link(xout_rgb.input)
# Send NN output (ImgDetection) to the host via XLink
xout_nn = pipeline.create(depthai.node.XLinkOut)
xout_nn.setStreamName("nn")
detection_nn.out.link(xout_nn.input)
```

#### 3.6. Initialize the DepthAI Device[7]
`Device` represents an **OAK camera**. On all of our devices there’s a powerful Robotics Vision Core (RVC). 
- The **RVC** is **optimized for performing AI inference algorithms** and **for processing sensory inputs**
  - (eg. calculating stereo disparity from two cameras).
```python
# Upload the pipeline to the device
with depthai.Device(pipeline) as device:
  # Print MxID, USB speed, and available cameras on the device
  print('MxId:',device.getDeviceInfo().getMxId())
  print('USB speed:',device.getUsbSpeed())
  print('Connected cameras:',device.getConnectedCameras())
```
- from this point on, **the pipeline will be running on the device**, producing results we requested
#### 3.7. Initialize the Input/Output Queues
As `XLinkOut` Nodes has been defined in the pipeline (#3.5), we’ll **define now a Host Side Output Queues** to **access the produced results**
- these **Queues** will be located on the **Host Computer** (in RAM)
```python
with depthai.Device(pipeline) as device:
    # ...
    # From this point, the Device will be in "running" mode and will start sending data via XLink
    # Get two output queues with their stream names from the device
    q_rgb = device.getOutputQueue("rgb")
    q_nn = device.getOutputQueue("nn")
```
- When we define an **Output Queue**, the `device` can push new `messages` to it at any point in time, and the `Host` can read from it at any point in time. 
- Usually, **when the Host is reading very fast** from the Queue, the **Queue (regardless of its size) will stay empty most of the time**.
- But as we **add things on the host side** (additional processing, analysis, etc), it may happen that the **device will be writing to the queue faster than the host can read from it**.
  - and then **the messages in the queue will start to add up** 
  - so we can set both `maxSize` and `blocking` flags to determine the behavior of the queue:
```python
# When initializing the queue
q = device.getOutputQueue(name="name", maxSize=5, blocking=False)
# Or afterwards
q.setMaxSize(10)
q.setBlocking(True)
```
#### 3.8. Fetch Ｒesults from Nodes
To **Fetch latest results** from both `NN` Node and `ColorCamera` Node, we need:
- The `tryGet` method **returns either the latest result** or **None** if the **queue is empty**.

```python
# 2 Placeholders - one for rgb frame and one for nn results
frame = None
detections = []    
# Main host-side application loop
while True:
    # we try to fetch the data from nn/rgb queues. tryGet will return either the data packet or None if there isn't any
    in_rgb = q_rgb.tryGet()
    in_nn = q_nn.tryGet()
```
- use `getCVFrame` to receive a frame from `ColorCamera`, and access `detections` array to receive detection objects from `NN`

```python
    if in_rgb is not None:
        # If the packet from RGB camera is present, we're retrieving the frame in OpenCV format using getCvFrame
        frame = in_rgb.getCvFrame()

    if in_nn is not None:
        # when data from nn is received, we take the detections array that contains mobilenet-ssd results
        detections = in_nn.detections
```
#### 3.10. Display the Results
```python
    if frame is not None:
        for detection in detections:
            # for each bounding box, we first normalize it to match the frame size
            bbox = frameNorm(frame, (detection.xmin, detection.ymin, detection.xmax, detection.ymax))
            # and then draw a rectangle on the frame to show the actual result
            cv2.rectangle(frame, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (255, 0, 0), 2)
        # After all the drawing is finished, we show the frame on the screen
        cv2.imshow("preview", frame)

    # at any time, you can press "q" and exit the main loop, therefore exiting the program itself
    if cv2.waitKey(1) == ord('q'):
        break
```
Due to **neural network implementation** details, **bounding box coordinates** in **inference results** are represented as floats from `<0-1>` range - so **relative to frame width/height** 
- e.g. if image has **200px width** and `nn` returned `x_min` coordinate equal to **0.2**, this means the **actual (normalised)** `x_min` coordinate is `40px`
* we need to define a helper function, `frameNorm()`, that will **convert these <0-1> values into actual pixel positions**
```python
# Since the detections returned by nn have values from <0..1> range, they need to be multiplied by frame width/height to
# receive the actual position of the bounding box on the image
def frameNorm(frame, bbox):
    normVals = np.full(len(bbox), frame.shape[0])
    normVals[::2] = frame.shape[1]
    return (np.clip(np.array(bbox), 0, 1) * normVals).astype(int)
```

![](https://files.mdnice.com/user/1474/9a9caa2b-3605-4db8-aebb-2254401290d2.png)







#### Resources
[1]https://docs.luxonis.com/en/latest/  
[2]https://docs.luxonis.com/en/latest/pages/spatial-ai/  
[3]https://docs.luxonis.com/projects/api/en/latest/components/pipeline/  
[4]https://docs.luxonis.com/projects/api/en/latest/components/nodes/color_camera/  
[5]https://docs.luxonis.com/projects/api/en/latest/components/nodes/mobilenet_detection_network/    
[6]https://docs.luxonis.com/projects/api/en/latest/components/messages/img_detections/#imgdetections  
[7]https://docs.luxonis.com/projects/api/en/latest/components/device/
