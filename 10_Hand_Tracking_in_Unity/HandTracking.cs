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

    
    // Three Points on Palm
    public GameObject cube0, cube5, cube17;
    // Points on Index Finger
    public GameObject cube8, cube6;

    // Update is called once per frame. It updates hand points and bones based on the latest tracking data.
    void Update()
    {

        UpdateHandPoints(); // Updates the positions of hand points.

        UpdateHandBones();  // Updates the positions and orientations of hand bones.
        /*

        // Calculate the center point of the plane
        Vector3 centerPoint = (point0 + point5 + point17) / 3;

        // Calculate two vectors
        Vector3 U = (point5 - point0).normalized;
        Vector3 V = (point17 - point0).normalized;

        Vector3 U568 = (point5 - point6).normalized;
        Vector3 V568 = (point8 - point6).normalized;



        // Calculate the normal vector
        Vector3 normal = Vector3.Cross(U, V).normalized;
        Vector3 normal568 = Vector3.Cross(U568, V568).normalized;

        // Calculate the rotation's right vector (U vector) and up vector
        Vector3 right = U;
        Vector3 up = Vector3.Cross(normal, right).normalized;
        // Calculate the rotation's right vector (U vector) and up vector
        Vector3 right568 = U568;
        Vector3 up568 = Vector3.Cross(normal568, right568).normalized;

        // Using LookRotation to set the cube's rotation, still using Quaternion but not direct quaternion calculations
        Quaternion rotation = Quaternion.LookRotation(normal, up);
        Quaternion rotation568 = Quaternion.LookRotation(normal568, up568);

        // Update the cube's position and rotation
        //cube.transform.position = centerPoint;
        cube0.transform.position = point0;
        cube0.transform.rotation = rotation;
        
        cube5.transform.position = point5;
        cube5.transform.rotation = rotation;
        cube17.transform.position = point17;
        cube17.transform.rotation = rotation;

        cube8.transform.position = point8;
        cube8.transform.rotation = rotation568;
        cube6.transform.position = point6;
        cube6.transform.rotation = rotation568;
        

        // Output world coordinates of point0, point5, and point17
        Debug.Log("World Coordinates (in cm):");
        //Debug.Log("Point0 (Wrist): " + point0.ToString("F2"));
        //Debug.Log("Point5 (Index Finger Base): " + point5.ToString("F2"));
        //Debug.Log("Point12: " + point12.ToString("F2"));
        // After updating the cube's position and rotation:
        Matrix4x4 cubeMatrix = cube0.transform.localToWorldMatrix;
        Quaternion cubeRotation = cube0.transform.rotation;

        // Directly log the localToWorldMatrix (includes translation, rotation, and scale)
        //Debug.Log("Cube Matrix (localToWorldMatrix): \n" + cubeMatrix);

        // To display just the rotation matrix component, convert Quaternion to Matrix
        Matrix4x4 rotationMatrix = Matrix4x4.Rotate(cubeRotation);

        // Log the rotation matrix
        //Debug.Log("Cube Rotation Matrix: \n" + rotationMatrix);


        // Calculate the distance between point 0 and point 12
        float distance = Vector3.Distance(point0, point12);

        // Debug log the distance
        Debug.Log("Distance between Point 0 and Point 12: " + distance + " cms");
        */
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
                //localPositions[i] = handPoints[i].transform.localPosition;
            }
            //return localPositions;
        }

        //Vector3[] localPositions = new Vector3[handPoints.Length];


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

