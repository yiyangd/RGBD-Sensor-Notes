# 三种计算深度的技术和深度传感器

> 此篇笔记是「深度传感器」笔记系列的第3篇，记录了普通相机拍摄的彩色图片（RGB Images）和深度相机拍摄的深度图片（Depth Images）的区别，以及不同深度相机的种类与深度计算的技术对比(结构光相机，立体深度相机，飞行时间和雷达传感器)


### 1. RGB Images vs Depth Images
#### 1.1. RGB Images
![Color Image = RGB Matrices](https://files.mdnice.com/user/1474/ec242f40-66a0-48fb-a45a-b76e6dbcd4b7.jpg)

Standard digital cameras output RGB images as a 2D grid of pixels. Each pixel has values associated with it – usually we think of those as Red, Green and Blue, or RGB. Each attribute has a number from 0 to 255. Thousands to millions of pixels together create the kind of photographs we are all very familiar with.   
标准数码相机输出图像作为一个2D网格的像素。每个像素都有相关的数值-通常我们认为那些是红色，绿色和蓝色(RGB)。每个属性都有一个从0到255的数字。成千上万的像素一起创造了我们都非常熟悉的平面照片。

RGB data can be used for object recognition and tracking, as well as basic scene understanding. Identifying the exact dimensions of physical objects is still a challenge, even using machine learning. This is where depth cameras can help.  
RGB数据可用于物体识别和跟踪，以及基本的场景理解。识别物理物体的确切尺寸仍然是一个挑战(即使使用机器学习)。这就是深度相机可以帮助的地方。


#### 1.2. Depth Images
![Each different color in the depth map represents a different distance from the camera](https://files.mdnice.com/user/1474/4e995f28-1356-48eb-ab27-c533bb820e15.jpg)

Using a depth camera, you can add a brand‑new channel of information, with distance to every pixel, or “depth.” Some depth cameras have both an RGB and a depth system, which can give pixels with all four values, or RGBD.    
使用深度相机，你可以增加一个全新的信息渠道，每个像素都有距离，或 "深度"。有些深度相机同时具有RGB和深度系统，可以得到具有所有四个数值的像素，或称RGBD。
- each different color in the depth map represents a different distance from the camera. In above case, cyan is closest to the camera, and red is furthest.   
深度图中的每种不同颜色代表与相机的不同距离。在上图情况下，青色离相机最近，红色离相机最远
### 2. Types of Depth Camera
There are a variety of different methods for calculating depth, all with different strengths and weaknesses and optimal operating conditions.   
计算深度的方法多种多样，各有优缺点和最佳操作条件。 

Which one you pick will almost certainly depend on what you are trying to build – how far does it need to see? What sort of accuracy do you need? Does it need to operate outdoors?  
你选择哪一个几乎肯定取决于你想要建立什么 - 它需要看多远？你需要什么样的精确度？需要在户外操作吗？

Here’s a quick breakdown of camera types and roughly how each one works.  
这里有一个快速分解的相机类型和大致每一个相机类型的工作原理。
#### 2.1. Coded Light Cameras
![RealSense Depth Camera SR305](https://files.mdnice.com/user/1474/f1f68e4d-8042-4dea-b038-55152ca04fbc.png)

Coded light cameras are designed for **short range indoor applications**. Coded light offers affordable depth calculations with our onboard 3D imaging ASIC.  
编码光相机是为**短距离的室内应用**而设计的。编码光通过我们的板载3D成像ASIC提供了便利的深度计算。

![How Coded Light Works](https://files.mdnice.com/user/1474/1065b4d4-dac8-4d89-9f26-7b20fe45afa2.jpg)  

Coded light **projects** a known pattern onto a scene and **evaluates** how this pattern deforms on surfaces.   
编码光将一个已知的图案**投射**到一个场景中，并**评估**这个图案在表面上的变形情况。  
For example, if the pattern is a series of stripes projected onto a ball, the stripes would deform and bend around the surface of the ball in a specific way.   
例如，如果图案是一系列投射到一个球上的条纹，那么这些条纹将以一种特定的方式在球的表面变形和弯折。

These patterns also vary over time, enabling finer detail to be composited from multiple depth images. Through deformation analysis, vision systems calculate the depth and surface information of objects.     
这些图案也随着时间的推移而变化，使更精细的细节能够从多个深度图像中合成。通过变形分析，视觉系统计算出物体的深度和表面信息。    

![Applications](https://files.mdnice.com/user/1474/c055943f-d37c-4e99-a0c2-384290e45822.png)

Applications include: face analytics and tracking, scanning and mapping, scene segmentation, hand and finger tracking and augmented reality.  
应用包括: 人脸分析和跟踪、扫描和绘图、场景分割、手指跟踪和增强现实。
#### 2.2. Stereo Depth Cameras 立体深度相机
Stereo depth cameras have two sensors, spaced a small distance apart. A stereo camera takes the two images from these two sensors and compares them. Since the distance between the sensors is known, these comparisons give depth information.   
立体深度摄像机有两个传感器，间隔一小段距离。立体摄像机从这两个传感器获取两幅图像并进行比较。由于传感器之间的距离是已知的，这些比较提供了深度信息。
![](https://files.mdnice.com/user/1474/d495881a-6325-4f97-a53c-eb5980f13090.jpg)

Stereo cameras work in a similar way to how we use two eyes for depth perception. Our brains calculate the difference between each eye. Objects closer to us will appear to move significantly from eye to eye (or sensor to sensor), where an object in the far distance would appear to move very little.  
立体摄像机的工作原理类似于我们用双眼拍摄深度知觉。我们的大脑计算每只眼睛之间的差异。靠近我们的物体会显著地从一只眼睛移动到另一只眼睛(或者传感器移动到传感器) ，而远处的物体似乎很少移动。
#### 2.2.1. Stereoscopic Vision 立体视觉
![Depth from Stereo algorithm finds disparity by matching blocks in left and right images](https://files.mdnice.com/user/1474/0fd845f7-cf7a-4db9-a206-658ad453551d.png)

**Depth from Stereo** is a classic computer vision algorithm inspired by the **human binocular vision system**. It relies on *two parallel view‑ports* and **calculates depth by estimating disparities between matching key‑points in the left and right images**:    
**立体深度**是一种经典的计算机视觉算法，其灵感来自**人类的双眼视觉系统**。它依赖于*两个平行的视口*，通过**估计左右图像中匹配的关键点之间的差异来计算深度**：

![](https://files.mdnice.com/user/1474/f8becb62-17ae-4863-97de-c8fda6b2c0ca.png)

There are several challenges that any actual product has to overcome:  
任何实际产品都必须克服以下几个挑战:
- Ensuring that the images are in fact coming from two parallel views  
确保图像实际上来自两个平行视图
- **Filtering out bad pixels** where matching failed due to **occlusion**  
**过滤掉**由于**遮挡**导致匹配失败的坏像素

![](https://files.mdnice.com/user/1474/8ea5df43-a712-420a-b480-f97ce1ce32ff.png)

#### 2.2.2. Calibration and Rectification
Having two exactly parallel view‑ports is challenging. While it is possible to generalize the algorithm to any two calibrated cameras (by **matching along epipolar lines**), the more common approach is **image rectification**. During this step left and right images are re‑projected to a common virtual plane:  
拥有两个完全平行的视口是一种挑战。虽然有可能将该算法推广到任何两台经过校准的相机（通过**沿两极线进行匹配**），但更常见的方法是**图像矫正**。在这一步骤中，左边和右边的图像被重新投射到一个共同的虚拟平面：

![Image Rectification illustrated (Source: Wikipedia)](https://files.mdnice.com/user/1474/a594dc87-ac56-4539-9e36-fcf84eb47530.jpg)
#### 2.2.3. Intel® RealSense™ D400 series cameras

![D457 was Launched on Sep 30. 2022](https://files.mdnice.com/user/1474/19e78553-5b43-4b96-8d42-8b35fce20f73.png)

Intel RealSense D400 cameras:  
英特尔 RealSense D400相机:

1. Come fully calibrated, producing hardware‑rectified pairs of images  
来完全校准，生成由硬件校正的一对图像
2. Perform all depth calculations at up to 90 FPS  
执行所有深度计算的帧速率高达90 FPS
3. Offer sub‑pixel accuracy and high fill-rate  
提供子像素精度和高填充率
4. Provide an on‑board texture projector for tough lighting conditions  
为恶劣的照明条件提供一个板载纹理投影仪
5. Run on standard USB 5V power-source, drawing about 1‑1.5 W  
运行在标准的 USB 5V 电源，绘制约1-1.5 W
6. Designed from the ground up to: 
- Address conditions critical to robotic/drone developers  
解决机器人/无人机开发者的关键条件
- Overcome the limitations of structured light  
克服结构光的局限性

![](https://files.mdnice.com/user/1474/2b1835c0-ccc0-4c14-8804-68099ec62961.png)


### 2.3. Time of Flight and LIDAR Sensors 飞行时间与激光雷达传感器
#### 2.3.1. How Lidar works
![](https://files.mdnice.com/user/1474/5f991478-ce62-4b26-8938-c08942218d2b.jpg)

Each kind of depth camera **relies on known information** in order to extrapolate depth. For example, in stereo, the distance between sensors is known; In coded light or structured light, the pattern of light is known.  
每种深度相机都**依赖于已知的信息**，以便推断出深度。例如，在立体深度传感中，传感器之间的距离是已知的；在编码光或结构光中，光的模式是已知的。 

**In the case of time of flight cameras, the speed of light is the known variable used to calculate depth**. LiDAR sensors, which you may be familiar with from things like **self-driving cars** are a type of time of flight camera which **use laser light to calculate depth**.   
**对于飞行时间相机来说，光速是用于计算深度的已知变量**。LiDAR传感器，你可能在**自动驾驶汽车**等方面很熟悉，是一种飞行时间相机，使**用激光来计算深度**。 

**All types of time of flight device emit some kind of light, sweep it over the scene, and then time how long that light takes to get back to a sensor on the camera.**   
**所有类型的飞行时间设备都会发出某种光，在场景上扫过，然后计算光需要多长时间回到相机上的一个传感器**。

Depending on **the power and wavelength of the light**, **time of flight sensors** can measure depth at significant distances – for example, *being used to map terrain from a helicopter*.   
根据**光的功率和波长**，**飞行时间传感器**可以在很远的地方测量深度--例如，*被用于从直升机上绘制地形图*。  
#### 2.3.2. RealSense L515

![Intel® RealSense™ LiDAR Camera L515](https://files.mdnice.com/user/1474/37b73904-fbb0-4361-916b-7832853577f8.png)


The new Intel® RealSense™ LiDAR Camera L515 is a new type of time-of-flight or LiDAR based camera. While most types of LiDAR devices have mechanical systems which spin around to sweep the environment with light which is then detected, the L515 uses a proprietary miniaturized scanning technology. This technology allows the L515 to be the world’s smallest high resolution LiDAR depth camera.

#### Resources:
- https://www.intelrealsense.com/beginners-guide-to-depth/
- https://www.researchgate.net/figure/Color-image-and-RGB-matrices_fig1_339435251
- https://www.zybuluo.com/TangWill/note/1443661
