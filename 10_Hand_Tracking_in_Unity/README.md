## RGBD Sensor Note 10 - 3D Hand Tracking and Visualization in Unity
> This summary describes a three-part Unity3D project setup for UDP data communication and hand tracking visualization. Firstly, a `UDPReceive` script is detailed for setting up a Unity project to receive UDP data, using essential namespaces for networking and multi-threading, and outlining member variables and methods for initializing and managing UDP communication. Secondly, Python code for hand data collection from an RGBD sensor is presented, demonstrating network communication setup, video capture, and hand landmarks data sending over UDP. Lastly, a `HandTracking` script in Unity is introduced for visualizing hand movements in 3D space, utilizing GameObjects to represent hand points and bones, and updating their positions based on incoming UDP data. The setup involves creating and configuring GameObjects in Unity to visualize hand tracking data received over UDP, highlighting the integration of external sensor data into a Unity project for interactive applications.
> 
![https://youtu.be/66u2hyGuyK0](https://files.mdnice.com/user/1474/410c5f21-9dc0-4a6f-8617-8810e261fc7a.gif)


### 1. UDP Receive Script

Create a Unity3D project, add a `UDPReceive` Script in `Assets`
#### 1.1. Using Namespaces
These namespaces provide classes for *handling text, networking, sockets, and multi-threading*

```csharp
using UnityEngine;
using System;
using System.Text;
using System.Net;
using System.Net.Sockets;
using System.Threading;
// Define the UDPReceive class which inherits from MonoBehaviour to integrate with Unity.
```
#### 1.2. Member Variables in `UDPReceive` Class
```csharp
// Define the UDPReceive class which inherits from MonoBehaviour to integrate with Unity.
public class UDPReceive : MonoBehaviour
{
    // Thread to handle UDP receiving independently without blocking the main thread.
    Thread receiveThread; 
    // UDP client for network operations(sending and receiving data).
    UdpClient client; 
    // Port number to listen on for incoming data.
    public int port = 5052;
    // Control flag to start or stop receiving data.
    public bool startRecieving = true;
    // Flag to enable printing received data to the console.
    public bool printToConsole = false;
    // Variable to store received data.
    public string data;

    // the core functionality for receiving data.
```
#### 1.3. `ReceiveData()` Method
```csharp
    // the core functionality for receiving data.
    private void ReceiveData()
    {
        // Initialize the UdpClient on the specified port.
        client = new UdpClient(port);
        // Continuously listen for incoming data as long as startReceiving is true.
        while (startRecieving)
        {
            try
            {
                // Listen for data from any IP address.
                IPEndPoint anyIP = new IPEndPoint(IPAddress.Any, 0);
                // Receive data (blocking call) and store in byte array.
                byte[] dataByte = client.Receive(ref anyIP);
                // Convert byte array to string using UTF-8 encoding.
                data = Encoding.UTF8.GetString(dataByte);
                // Uncomment the below line to print received data to the Unity console if printToConsole is true.
                //if (printToConsole) { print(data); }
            }
            catch (Exception err) // Catch and handle any exceptions.
            {
                print(err.ToString());
            }
        }
    }
    // Start is called before the first frame update in Unity.
```

#### 1.4. `Start()` Method
```csharp
    // Start is called before the first frame update in Unity.
    public void Start()
    {
        // Initialize the receive thread with the ReceiveData method.
        receiveThread = new Thread(new ThreadStart(ReceiveData));
        // Set the thread to run in the background.
        receiveThread.IsBackground = true;
        // Start the receive thread.
        receiveThread.Start();
    }
}
```

This script is set up to continuously listen for and receive data over UDP on the specified port. 
- It's a basic framework for UDP communication in Unity for specific use cases, 
  - such as multiplayer game networking or communication with external hardware or software.


Create an Empty GameObject, name it `Manager`， Drag the Script to it

![](https://files.mdnice.com/user/1474/139e3587-ee30-4aa1-be59-8ee8aa2cc640.png)



### 2. Hand Data Collection from RGBD Sensor
#### 2.1. Network Communication and Video Capture Setup
```python
from cvzone.HandTrackingModule import HandDetector
import cv2
import socket
from RGBDSensor import *

sensor = RGBDSensor()

detector = HandDetector(detectionCon=0.4, maxHands=2)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverAddressPort = ("127.0.0.1", 5052)
```
#### 2.2. Send Hand Landmarks  over UDP
```python
# Main loop to continuously process video frames
while True:
    # Get image frame
    color_image, depth_image, depth_frame = sensor.get_images()
    (h, w, _) = color_image.shape # (480, 640)
    #import pdb; pdb.set_trace()
    depth_pcd = sensor.get_point_cloud(depth_frame)

    # Find the hand and its landmarks (画手)
    hands, color_image = detector.findHands(color_image)  # with draw
    
    data = []  #[x1, y1, z1, x2, y2, z2]
    data1 =[]  #[[x1, y1, z1], array[x2, y2, z2]]
    depth_pcd[:, :, 1] = -depth_pcd[:, :, 1] 
    if hands:
        # Hand 1
        hand = hands[0]
        lmList = hand["lmList"]  # List of 21 Landmark points
        for lm in lmList:
            if lm[1] < 480 and lm[0] < 640:
                distance = depth_image[lm[1],lm[0]]
                data.extend(depth_pcd[lm[1], lm[0]].tolist())

        data = [i * 100 for i in data]
        data = [round(x,2) for x in data] 

        sock.sendto(str.encode(str(data)), serverAddressPort)
    else:
        # No hands, data is empty
        data = [0] * 63
        sock.sendto(str.encode(str(data)), serverAddressPort)
    
    # Apply color map to depth image for visualization
    depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.3), 
                                    cv2.COLORMAP_JET)
    img = cv2.resize(color_image, (0,0), None, 0.5, 0.5)
    # Display the captured frame with hand landmarks
    cv2.imshow("Image", img)
    
    if cv2.waitKey(1) == ord('q'):
        break
    
# Release resources and stop the pipeline
cv2.destroyAllWindows()
sensor.release()
```

### 3.  `HandTracking` Script

This Unity script, `HandTracking` is designed for **tracking and visualizing hand movements and gestures** in 3D space by using GameObjects to represent *hand points (joints)* and *bones (connections between joints)*. 
- It **updates the positions and orientations of these GameObjects** based on **incoming UDP data**, likely representing real-time tracking data from our RGB-D Sensor. 

#### 3.1. Two Game Object Arrays to store points and bones
```csharp
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

// The HandTracking class is responsible for visualizing hand movement in 3D space using Unity GameObjects.
public class HandTracking : MonoBehaviour
{
    // Reference to a UDPReceive component that listens for UDP packets containing hand tracking data.
    public UDPReceive udpReceive;
    // Arrays of GameObjects representing the tracked points and bones of the hand.
    public GameObject[] handPoints; // Points like fingertips and joints.
    public GameObject[] handBones; // Visual connections (bones) between the points.
    // Update is called once per frame. It updates hand points and bones based on the latest tracking data.
```
Drag the `HandTracking` Script to `Manager` 
- Drag `Manager` to `Udp Receive` Field


![](https://files.mdnice.com/user/1474/d751d441-2848-4c82-a4b7-636141e60892.png)

#### 3.2. Create 21 Spheres and 20 Cylinders to Represent HandPoints and HandBones



Create an Empty GameObject - `Hand`
- right click `Hand`, create a Empty GameObject - `Points`
  -  right click `Points`, create a **`3D Object > Sphere`**
  - make it `red` rename it `Point`
  - duplicate it 20 times (in total there are 21 hand landmarks)
- right click `Hand`, create a Empty GameObject - `Bones`
  - right click `Bones`, create a **`3D Object > Cylinder`**
  - duplicate it 19 times (in total there are 20 hand bones between 21 landmarks)
  - rename them **`Cylinder[StartPoint][EndPoint]`**


![](https://files.mdnice.com/user/1474/923d7512-6a21-43c2-94f5-622aef5ff6f0.png)

- Drag **`Point (0)`** to **`Point (20)`** to **`Hand Points`** Field and Drag  **`Cylinder01`** to **`Cylinder1920`** to **`Hand Bones`** Field


![](https://files.mdnice.com/user/1474/5dd335b4-0fe2-4c60-89a1-cf9035b721c1.png)


#### 3.3. Parses UDP data to update HandPoints and HandBones positions

```csharp
    // Update is called once per frame. It updates hand points and bones based on the latest tracking data.
    void Update()
    {
        UpdateHandPoints(); // Updates the positions of hand points.
        UpdateHandBones();  // Updates the positions and orientations of hand bones.
    }

    // Parses UDP data to update hand point positions.
    void UpdateHandPoints()
    {
        string data = udpReceive.data; // Retrieve the latest data from the UDP receiver.
        if(string.IsNullOrWhiteSpace(data)) return; // If data is empty or whitespace, do not proceed.
        // Cleans the raw data string by removing leading and trailing brackets.
        data = data.Remove(0,1);
        data = data.Remove(data.Length - 1, 1);
        // Splits the cleaned data string into an array of point coordinates.
        string[] points = data.Split(',');
        // If the correct number of points is received, update each hand point's position.
        if(points.Length == 63) // Expected data format: 21 points * 3 coordinates (x, y, z) per point.
        {
            for (int i = 0; i < 21; i++)
            {
                float x = float.Parse(points[i * 3]) ;
                float y = float.Parse(points[i * 3 + 1]) ;
                float z = float.Parse(points[i * 3 + 2]) ;
                // Sets the local position of each hand point GameObject to the new coordinates.
                handPoints[i].transform.localPosition = new Vector3(x, y, z);
            }
        }
    }
    // Updates the visual representation of hand bones based on the positions of hand points.
    void UpdateHandBones()
    {
        for (int i = 0; i < handBones.Length; i++)
        {
            // Calculates the start and end points for each bone, with special handling for the wrist (i % 4 == 0).
            Vector3 startPoint = (i % 4 == 0) ? handPoints[0].transform.localPosition : handPoints[i].transform.localPosition;
            Vector3 endPoint = handPoints[i + 1].transform.localPosition;
            // Skips updating the bone if either point is at the origin 
            if (startPoint == Vector3.zero || endPoint == Vector3.zero)
            {
                continue; // preventing incorrect visualizations.
            }
            // Updates the position, orientation, and scale of the bone to match the current hand structure.
            UpdateCylinder(handBones[i], startPoint, endPoint);
        }
    }
    // Adjusts a cylinder GameObject to stretch between two points, representing a bone.
    void UpdateCylinder(GameObject cylinder, Vector3 start, Vector3 end)
    {
        Vector3 direction = end - start; // Direction vector from start to end point.
        cylinder.transform.position = start + direction / 2; // Sets the cylinder's position to the midpoint.
        cylinder.transform.up = direction.normalized; // Aligns the cylinder's up vector with the direction.
        float distance = Vector3.Distance(start, end); // Calculates the distance between the start and end points.
        // Adjusts the cylinder's scale to match the distance between the points, maintaining its diameter.
        cylinder.transform.localScale = new Vector3(cylinder.transform.localScale.x, distance / 2, cylinder.transform.localScale.z); 
    }
}
```

- run the python script and click the play button


![](https://files.mdnice.com/user/1474/410c5f21-9dc0-4a6f-8617-8810e261fc7a.gif)
