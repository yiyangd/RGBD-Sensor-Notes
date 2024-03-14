from cvzone.HandTrackingModule import HandDetector
import cv2
import socket
from RGBDSensor import *
#from YOLOv8 import *
sensor = RGBDSensor()
#yolo = YOLOv8("yolov8x-seg.pt")
detector = HandDetector(detectionCon=0.4, maxHands=2)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverAddressPort = ("127.0.0.1", 5052)

while True:
    # Get image frame
    color_image, depth_image, depth_frame = sensor.get_images()
    (h, w, _) = color_image.shape # (480, 640)
    #import pdb; pdb.set_trace()
    depth_pcd = sensor.get_point_cloud(depth_frame)

    # Find the hand and its landmarks (画手)
    hands, color_image = detector.findHands(color_image)  # with draw
    # hands = detector.findHands(img, draw=False)  # without draw
    # 画物体
    #boxes, classes, scores, masks = yolo.run(color_image)
    # color_image = yolo.draw_masks(color_image, masks, classes)
    #color_image, width, height, center_x, center_y, center_z = yolo.draw_boxes(color_image, depth_image, boxes, classes, scores)
    
    data = []  #[x1, y1, z1, x2, y2, z2]
    data1 =[]  #[[x1, y1, z1], array[x2, y2, z2]]
    depth_pcd[:, :, 1] = -depth_pcd[:, :, 1] 
    if hands:
        # Hand 1
        hand = hands[0]
        #print(hand)
        lmList = hand["lmList"]  # List of 21 Landmark points
        for lm in lmList:
            if lm[1] < 480 and lm[0] < 640:
                distance = depth_image[lm[1],lm[0]]
                #data.extend([lm[0], h - lm[1], distance]) #lm[2]
                data.extend(depth_pcd[lm[1], lm[0]].tolist())
            else:
                data.extend([0,0,0])
                
                
                #data1.append(depth_pcd[lm[1], lm[0]])
        #import pdb; pdb.set_trace()
        #data.extend([width, height, center_x, h-center_y, center_z]) # assume the thickness of object is equal to the width
        #import pdb; pdb.set_trace()
        # print(data1)
        # landmark_pcd = np.array(data1)
        # pcd = o3d.geqometry.PointCloud()
        # pcd.points = o3d.utility.Vector3dVector(landmark_pcd) 
        # o3d.visualization.draw_geometries([pcd])
        
        
        data = [i * 100 for i in data]
        data = [round(x,2) for x in data] 
        #print(data) # 21 x 3 (x, 480-y, )
        #print(len(data))
        sock.sendto(str.encode(str(data)), serverAddressPort)
    else:
        # No hands, data is empty
        data = [0] * 63
        #data.extend([width, height, center_x, h-center_y, center_z])
        print(data)
        print(len(data))
        sock.sendto(str.encode(str(data)), serverAddressPort)
    
    # Apply color map to depth image for visualization
    depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.3), 
                                    cv2.COLORMAP_JET)
    # Display RGB and depth images
    #rgbd_img = np.concatenate((color_image,depth_colormap), axis=1)
    #cv2.imshow("RGB-Depth Image", rgbd_img)
    img = cv2.resize(color_image, (0,0), None, 0.5, 0.5)
    # Display the captured frame with hand landmarks
    cv2.imshow("Image", img)
    
    if cv2.waitKey(1) == ord('q'):
        break
    

# Release resources and stop the pipeline
cv2.destroyAllWindows()
sensor.release()