## RGBD Sensor 11 - RGB and Depth Camera Intrinsics & Extrinsics and Focal Length


### 1. Camera Projections from 3D Scene to 2D Image

A **Camera** is a **Mapping between the 3D world (object space) and a 2D image**. 
- The *drop from 3D world to a 2D image* is a **projection process** in which we *lose one dimension*.
  - The usual way of modelling this process is by **Central Projection** in which *a ray from a point in space* is drawn *from a 3D world point* through a fixed hole in space, **the Centre of Projection**.
  - This *ray will intersect a specific plane* in space chosen as the **image (focal or sensor) plane**
  -  The **intersection of the ray with the image plane** represents *the image of the point*.

  
#### The History of "Camera Obscūra" 
A **camera obscūra** is a *darkened（from latin word 'obscūra'） room（from latin word 'camera'）* with a *small hole (or lens)* at one side *through which an image is projected onto a wall* opposite the hole.
- The **image (or the principle of its projection)** of lensless camera obscuras is also referred to as *"pinhole image"*.

![Illustration of the camera obscura principle from James Ayscough's A short account of the eye and nature of vision (1755 fourth edition)](https://upload.wikimedia.org/wikipedia/commons/c/c2/1755_james_ayscough.jpg)

One of the **earliest known written records of a pinhole image** is found in the Chinese text called ***Mozi***, dated to the 4th century BC, traditionally ascribed to and named for *Mozi (circa 470 BC-circa 391 BC)*, a Chinese philosopher and the founder of Mohist School of Logic. 



!["景。光之人，煦若射，下者之人也高；高者之人也下。足蔽下光，故成景于上；首蔽上光，故成景于下。在远近有端，与于光，故景库内也。" -- 《墨子 - 经说下》](https://files.mdnice.com/user/1474/9e5451da-b447-48ff-b043-5ad203259b03.png)

- These writings explain *how the image in a "collecting-point" is inverted by an intersecting point (pinhole)* that *collects the (rays of) light*. 
- **Light coming from the foot of an illuminated person** gets ***partly hidden below*** (i.e., strikes below the pinhole) and ***partly forms the top of the image***. 
- **Rays from the head** are ***partly hidden above*** (i.e., strike above the pinhole) and ***partly form the lower part of the image***.


![The first use of the term "camera obscura" was by Johannes Kepler, in his first treatise about optics, Ad Vitellionem paralipomena quibus astronomiae pars optica traditur (1604)](https://files.mdnice.com/user/1474/fb5f5530-5483-4a52-8be3-f086fa7f45a6.png)

- **Camera Obscuras with a lens** in the opening have been used *since the second half of the 16th century* and became *popular as aids for drawing and painting*.
  - it allowed *tracing the projected image* to *produce a highly accurate representation* and *graphical perspective*.
  
![A camera obscura drawing aid tent in an illustration for an 1858 book on physics](https://upload.wikimedia.org/wikipedia/commons/d/d0/1858_-_Gagniet_%28d%29_Quarteley_%28g%29_-_Cours_de_Physique_%28A._Ganot%29.jpg)

- A **Camera Obscura without a lens** but *with a very small hole* is sometimes referred to as a **Pinhole Camera**, 



![Early pinhole camera. Light enters a dark box through a small hole (focal point) and creates an inverted 2D image on the wall (image plane) opposite the hole.](https://www.mathworks.com/help/vision/ug/camera-calibration-focal-point.png)

#### Pinhole (Linear) Camera Model

Once ***the light from a scene reaches the camera***, it must *still pass through the lens of camera (pinhole)* before *reaching the digital sensor or a film (wall of the room)*. 
- For many applications, it suffices to **treat the lens as an ideal pinhole** that simply ***projects all rays through a common center of projection***
- *Ignoring such effects as focus and lens thickness*, a reasonable **approximation** is that all ***the rays pass through a single point, the centre of the lens***


![Pinhole Camera Geometry](https://files.mdnice.com/user/1474/1aa69e20-5f26-4d67-a99f-bd45c9500a11.png)

- The **Centre of Projection** is called the *Camera Centre*. It is also known as the *Optical Centre*. 
- The ***Line from the Camera Centre perpendicular to the image (focal or sensor) plane*** is called *the Principal Axis* or *principal ray of the camera*, 
- and the ***Point where the principal axis meets the image plane*** is called the *principal point*.

#### Central Projection
We consider the **Central Projection** of ***Points in 3D space onto a 2D plane***. 
- Let the **Centre of Camera Projection** be the ***origin of a Euclidean coordinate system***, and consider the **Plane**
  $$Z = \color{red}f$$
  which is called the **image plane** or **focal plane**

Under the **Pinhole Camera Model**, a ***point in 3D space*** is ***mapped to the point on the 2D image plane*** 
- where *a line joining the point $\mathbf{X}$ to the centre of projection meets the image plane*.


![](https://files.mdnice.com/user/1474/430ea836-9c6a-40da-aa86-70a264cad974.png)

By **similar triangles**, one quickly computes that **the point in 3D space with coordinates**
$$
\mathbf{X} = \begin{bmatrix}
X \\ Y \\ \color{blue}Z
\end{bmatrix}
$$ 
is **mapped to the point on the image plane** 

$$\mathbf{x} = \begin{bmatrix}
\color{red}f\color{black} \ X/\color{blue}Z \\ 
\color{red}f\color{black} \ Y/\color{blue}Z \\ 
\color{red}f\color{black} \cancel{\color{blue}Z/Z}
\end{bmatrix}
= \begin{bmatrix}
\color{red}f\color{black} \ X / \color{blue}Z \ \\ 
\color{red}f\color{black}  \ Y / \color{blue}Z \  \\ \color{red}f\color{black} 
\end{bmatrix}
$$ 

Ignoring the final image coordinate, we see that

$$
\begin{bmatrix}
X \\ Y \\ \color{blue}Z
\end{bmatrix}
\rightarrow
\begin{bmatrix}
\color{red}f\color{black} \ X / \color{blue}Z \ \\ 
\color{red}f\color{black}  \ Y / \color{blue}Z \  
\end{bmatrix}
$$ 
describes the **Central Projection Mapping** from ***3D world to 2D image coordinates***.



### 2. Projective vs Euclidean Geometry 


#### Limitation of Euclidean Geometry
**Euclidean Geometry** is the geometry that *describes angles and shapes of objects*.
- however what we *perceive in real life* is *different* from what’s *described with Euclidean geometry* 

It is ***troublesome*** in one major respect – we need to ***keep making an exception*** to *reason* about some of the *basic concepts* of the *geometry* - such as *intersection of lines:*
- Two lines *almost always meet in a point*, but there are ***some pairs of lines that do NOT do so*** – those that we call **parallel**.
- A common linguistic device for getting around this is to say that **parallel lines meet “at infinity”**
  - However this is not altogether convincing, and conflicts with another dictum, that infinity does not exist, and is only a convenient fiction. 

![In Projective Geometry unlike Euclidean Geometry, two parallel lines meet at a "point at infinity". ](https://files.mdnice.com/user/1474/ea64989d-99fd-4b2a-b6ab-1539bcc10b4b.png)

By ***the addition of these points at infinity*** where ***parallel lines meet***, the **Euclidean Space** is *transformed into* a new type of geometric object, **Projective Space**.
- Since we are familiar with the *properties of Euclidean Space*, involving *concepts such as distances, angles, points, lines and incidence*,
- there is *nothing very mysterious about Projective Space* – it is just an extension of Euclidean space in which *two lines always meet in a point*, 
  - though *sometimes at mysterious points at infinity*.

![](https://files.mdnice.com/user/1474/c9871c80-d94a-4093-9f65-85f3fa5732a4.png)

When we look at a picture, we see **squares that are not squares**, or **circles that are not circles**.
- The **Transformation** that ***maps these planar objects onto the picture*** is an example of a **Projective Transformation**.

What **properties of geometry** are ***preserved*** by Projective Transformations?
- ***Shape and Lengths are NOT***, since *TWO perpendicular radii of a circle* are *stretched by different amounts* by the *projective transformation* 
- ***Angles, Distance, Ratios of Distances*** – ***NONE*** of these are preserved,
- **ONE property that is preserved** is that of **Straightness,**
  - we may *define a Projective Transformation of a Plane* as *any Mapping of the Points on the Plane* that *preserves straight lines.*

#### Extend Euclidean Space to Projective Space by Homogeneous Coordinates
**Points (pixel coordinates in an image)** in *2D Euclidean Space* can be denoted using *a pair of real numbers*, 

$$\mathbf{x} = \begin{bmatrix}
x \\ y 
\end{bmatrix} \in \mathcal{R}^2$$ 

- We may *add an extra coordinate* to this pair that we ***declare to represent the same point***

$$\mathbf{\bar{x}} 
= \begin{bmatrix}
x \\ y \\ \color{blue}1
\end{bmatrix} $$ 

$\ \mathbf{\bar{x}} \ $ is called the ***augmented vector***, by which we define  **Homogeneous Coordinates:**

$$
\begin{aligned}
\tilde{\mathbf{x}} &=

\color{red}\tilde{w} \ \color{black} \mathbf{\bar{x}} \\

&= \color{red}\tilde{w} \color{black}
\begin{bmatrix}
x \\ y \\ \color{blue}1
\end{bmatrix}
=
\begin{bmatrix}
\tilde{x} \\ \tilde{y} \\ \color{red}\tilde{w}
\end{bmatrix} \in \mathcal{P}^2
\end{aligned}
$$
- where **Vectors that Differ ONLY BY Non-ZERO Scale $ \color{red}\tilde{w} \neq 0$** are ***considered to be Equivalent***, so $\tilde{\mathbf{x}}=(x,y,\color{blue}{1}\color{black})^T$, $( \color{red}{2}\color{black}x,  \color{red}{2}\color{black}y, \color{red}{2}\color{black} )^T$ and $( \color{red}{\tilde{w}}\color{black}x,  \color{red}{\tilde{w}}\color{black}y, \color{red}{\tilde{w}}\color{black} )^T$ ***represent the same point***.
  - and we can **get the inhomogeneous coordinates back** by *dividing* by $\color{red}\tilde{w} \neq 0$ to get $\mathbf{x} = (x, y)^T$.
  - **homogeneous points whose last element** is $\color{red}\tilde{w} = 0$ are called ***ideal points*** or ***Points at Infinity*** and do *NOT have an equivalent inhomogeneous representation*.

- $\mathcal{P}^2 = \mathcal{R}^3 - (0,0,0)$ is called the **2D Projective Space**, which is ***extended from 2D Euclidean Space*** by *representing points as Homogeneous Vectors*
  - **Points at Infinity $\color{red}(\tilde{w} = 0)$** **in the 2D Projective Space** form a line, usually called *the line at infinity*. 
  - ***In 3D they form the plane at infinity***

- In Computer Vision problems, **Projective Space** is used as a convenient way of *representing the real 3D world*, ***by extending it to the 3D Projective Space***,
  - and **2D Images**, usually ***formed by Projecting the 3D world onto a 2D representation***, are for convenience *extended to be thought of as lying in the 2D Projective Space*

#### Central Projection using Homogeneous Coordinates

If **the 3D world and 2D image points** are represented by **Homogeneous Vectors**, 
- then **Central Projection** is very simply expressed as a ***Linear Mapping between their Homogeneous Coordinates***.

$$
\color{red}\mathbf{\tilde{x}}\color{black}= \mathbf{\tilde{P}} \color{blue}\mathbf{\bar{X}}
$$

$$
\begin{bmatrix}
\color{red}f\color{black} \ X / \color{blue}Z \ \\ 
\color{red}f\color{black}  \ Y / \color{blue}Z  \\ \color{blue}1 \  
\end{bmatrix}
\equiv
\begin{bmatrix}
\color{red}f\color{black} \ X \  \\ \color{red}f\color{black} \ Y \  \\ \color{blue}Z \ 
\end{bmatrix} 
=

\underbrace{
\begin{bmatrix}
\color{red}f & 0 & 0 & 0 \\
0 & \color{red}f & 0 & 0 \\
0 & 0 & \color{blue}1 & 0 \\
\end{bmatrix}}_{diag(f,f,1) \begin{bmatrix}
\mathbf{I} \mid \mathbf{0}
\end{bmatrix}}


\begin{bmatrix}
X \\ Y \\ \color{blue}Z \\ 1
\end{bmatrix}
$$

- which defines the **3 $\times$ 4 Homogeneous Camera Projection Matrix** for the *Pinhole Model of Central Projection* as

$$
\mathbf{\tilde{P}} = diag(f,f,1) \begin{bmatrix}
 \ \mathbf{I}\mid \mathbf{0} \
\end{bmatrix}
$$


### 3. Camera Intrinsics

#### Principal Point Offset
In practice, the **Origin of Coordinates** in the *Image Plane* is **NOT at the Principal Point**. Once we have **projected a 3D point through an ideal pinhole using a Projection Matrix**,
- we must still ***transform the resulting coordinates*** according to the *pixel sensor spacing* and the *relative position of the image plane to the origin (Principal Point Offset)*.

![The origins of the coordinate systems differ between image coordinates and camera coordinates.](https://files.mdnice.com/user/1474/ef48d570-a24f-435b-9775-3ac0051f0db8.png)

- **Image Sensors return Pixel Values** indexed by integer pixel with the coordinates **starting at the Upper-Left corner** of the image and **moving Down** and **to the Right**.

#### Mapping from 3D Camera to 2D Image Frame
Let $(c_x,c_y)^T$ be the **Pixel Coordinates of the Image Center** (Principal Point), and then Let $\color{red}(m_x,m_y)^T$ be the **Pixel Densities (pixels/mm)** in x and y directions, there is a mapping


$$
\begin{aligned}
\begin{bmatrix}
\ \color{red}m_x f \color{black} \ X / \color{blue}Z \color{black} + c_x  \ \\ 
\color{red}m_y f \color{black} \ Y / \color{blue}Z \color{black} + c_y  \\
\color{blue}1 \  
\end{bmatrix}
& \equiv
\begin{bmatrix}
 \color{red} m_x f\color{black} \ X + \color{blue}Z \color{black} c_x \  \\ \color{red} m_y f\color{black} \ Y + \color{blue}Z \color{black} c_y \  \\ \color{blue}Z \ 
\end{bmatrix} \\

& =

\begin{bmatrix}
\color{red}f_x & 0 & c_x & 0 \\
0 & \color{red}f_y & c_y & 0 \\
0 & 0 & \color{blue}1 & 0 \\
\end{bmatrix}


\begin{bmatrix}
X \\ Y \\ \color{blue}Z \\ 1
\end{bmatrix}
\end{aligned}
$$


- which defines the **3 $\times$ 3  Camera Calibration Matrix** to ***describes the Camera Intrinsics***:

$$\mathbf{K} = \begin{bmatrix}
\color{red}f_x & 0 & c_x  \\
0 & \color{red}f_y & c_y  \\
0 & 0 & \color{blue}1  \\
\end{bmatrix}$$


- Then the mapping can be expressed as
$$
\color{red}\mathbf{\tilde{x}}\color{black}= \mathbf{K} \begin{bmatrix}
\mathbf{I} \mid \mathbf{0}
\end{bmatrix} \color{blue}\mathbf{\bar{X}_{cam}}
$$
- **The camera is assumed to be located at the origin of a Euclidean coordinate system** with *the principal axis of the camera pointing straight down the Z-axis*, and 
  - the point $\color{blue}\mathbf{\bar{X}_{cam}}$ is expressed in this coordinate system.
  - Such a coordinate system may be called the **Camera Coordinate Frame**.
  
  



### 4. Camera Extrinsics
#### Mapping from 3D World to 3D Camera Frame
In general, **points in 3D space** will be expressed in terms of a *different Euclidean coordinate frame*, known as the ***World Coordinate Frame***.
- The *TWO Coordinate Frames* are related *via a rotation and a translation*. 



![The Euclidean Transformation between the World and Camera Coordinate Frames.](https://files.mdnice.com/user/1474/f0c7e405-4782-4a75-bafb-48624ce7215a.png)



Let $\color{blue}\mathbf{X_w}=(X, Y, Z)^T$ be **inhomogeneous coordinates of a 3D point** in the ***World Coordinate Frame***, and $\color{blue}\mathbf{{X}_{c}} = (X_{c}, Y_{c}, Z_{c})^T$ represents the **same 3D point** in the ***Camera Coordinate Frame***, then we may write

$$\color{blue}\mathbf{X_{c}}
\color{black}=
\mathbf{R} [\color{blue}\mathbf{X_w}\color{black} - \mathbf{C}]
$$

- where $\mathbf{C}$ represents the **Position Coordinates of the Camera Centre** in the ***World Coordinate Frame***,
- and $\mathbf{R}$ is a **$3 \times 3$ Orthonormal Rotation Matrix** representing the **Orientation** of the ***Camera Coordinate Frame***.
  - **each row** represents **the direction** of $X_{c}$, $Y_{c}$ and $Z_{c}$ ***w.r.t. World Frame***
  - they are **perpendicular (orthogonal)** with **lengths are 1 (normal)**


This equation may be written in *homogeneous coordinates* as

$$\color{blue}\tilde{\mathbf{X}}_{\mathbf{c}} 
\color{black}=
\begin{bmatrix}
\mathbf{R} & - \mathbf{RC} \\
0 & 1
\end{bmatrix}
\begin{bmatrix}

X \\ Y \\ Z \\ 1
\end{bmatrix}
=
\begin{bmatrix}
\mathbf{R} & - \mathbf{RC} \\
0 & 1
\end{bmatrix}
\color{blue}\bar{\mathbf{X}}_{\mathbf{w}}
$$
- which defines the **4 $\times$ 4  Camera Extrinsic Matrix** to ***describes the Camera Extrinsics***:

$$
\begin{bmatrix}
\mathbf{R} & - \mathbf{RC} \\
0 & 1
\end{bmatrix}

$$

### 5. Camera (Projection) Matrix  
Since the **Mapping from 3D Camera to 2D Image Pixel Frame** is 
$$
\color{red}\mathbf{\tilde{x}}\color{black}= \mathbf{K} \begin{bmatrix}
\mathbf{I} \mid \mathbf{0}
\end{bmatrix} \color{blue}\mathbf{\bar{X}_{cam}}
$$

Then the **Mapping from 3D World to 2D Image Pixel Frame** is 

$$
\color{red}\mathbf{\tilde{x}}\color{black}= \mathbf{KR} \begin{bmatrix}
\mathbf{I} \mid - \mathbf{C}
\end{bmatrix} \color{blue}

\bar{\mathbf{X}}_{\mathbf{w}}
$$


This is the **General Mapping** given by a **pinhole camera** and It is often convenient *NOT to make the camera centre explicit*, in this case let $\mathbf{t = -RC}$, then

$$ \mathbf{P}  
= \mathbf{K} \begin{bmatrix}
\mathbf{R} \mid \mathbf{t}
\end{bmatrix}
$$
is known as the **$3 \times 4$ Camera Matrix** which has ***9 Degrees of Freedom:***
- ***3 parameters*** ($f$, $c_x$, $c_y$) contained in $\mathbf{K}$ are called the *Internal Camera Parameters*
- ***3 parameters*** for $\mathbf{R}$ and ***3 parameters*** for $\mathbf{C}$ which **relate the Camera Orientation and Position to a World Frame** are called the *External Camera Parameters*

![The world points are transformed to camera coordinates using the extrinsic parameters. The camera coordinates are mapped into the image plane using the intrinsics parameters](https://www.mathworks.com/help/vision/ug/calibration-cameramodel-coords.png)

### 6. Camera Calibration Procedure

#### Step 1. Capture an Image of an Object with Known Geometry
![](https://files.mdnice.com/user/1474/e03181ea-c415-493a-9162-e06e1c9999a1.png)

Given a cube, we have known the location of every point in 3D.
- Let **the Origin World Coordinate Frame** be ***at one Corner*** and take a single image of this cube.

#### Step 2. Identify Correspondences between 3D Scene and 2D Image Points


![](https://files.mdnice.com/user/1474/c16778f3-93db-4172-b5c3-8f4d70b5fecd.png)

Consider a point in 3D World Frame is located at 

$$\color{purple} \mathbf{X_w} =
\begin{bmatrix}
X_w \\
Y_w \\
Z_w
\end{bmatrix} = 
\begin{bmatrix}
0 \\
3 \\
4
\end{bmatrix} \ 40
\text{(in cm)}
$$
And its 2D Image location is 

$$\color{purple} \mathbf{x} =
\begin{bmatrix}
u \\
v 
\end{bmatrix} = 
\begin{bmatrix}
56 \\
116
\end{bmatrix} \ 
\text{(in pixels)}
$$

- we can **do the same for all other visual features** and **establish a set of correspondences points from 3D to 2D** either by clicking on points manually or using an algorithm

#### Step 3. Set the Linear Equations
For each **Corresponding Point** $i$ in 3D Scene and 2D Image:

$$
\underbrace{
\begin{bmatrix}
u^{(i)} \\ v^{(i)} \\ 1
\end{bmatrix}}_{\textbf{Known } \color{purple} \mathbf{x}}

\equiv

\underbrace{
\begin{bmatrix}
p_{11} & p_{12} & p_{13} & p_{14} \\
p_{21} & p_{22} & p_{23} & p_{24} \\
p_{31} & p_{32} & p_{33} & p_{34} \\
p_{41} & p_{42} & p_{43} & p_{44} 
\end{bmatrix}}_{\color{red} \mathbf{P} \textbf{ is UnKnown}}

\underbrace{
\begin{bmatrix}
X_{w}^{(i)} \\ Y^{(i)}_{w} \\ Z^{(i)}_{w} \\ 1
\end{bmatrix}}_{ \textbf{Known } \color{purple} \mathbf{X_w}}
$$




- Expanding the Matrix as Linear Equations:

$$
u^{(i)} = 
\frac{p_{11} X_{w}^{(i)}+p_{12} Y_{w}^{(i)}+p_{13} Z_{w}^{(i)} + p_{14}}{p_{31} X_{w}^{(i)}+p_{32} Y_{w}^{(i)}+p_{33} Z_{w}^{(i)} + p_{34}} 
$$

$$
v^{(i)} = 
\frac{p_{21} X_{w}^{(i)}+p_{22} Y_{w}^{(i)}+p_{23} Z_{w}^{(i)} + p_{24}}{p_{31} X_{w}^{(i)}+p_{32} Y_{w}^{(i)}+p_{33} Z_{w}^{(i)} + p_{34}} 
$$

- Rearrange the Terms to get Known  $(2n \times 12)$ Matrix  $\mathbf{A}$ and Unknowned $\mathbf{p}$

$\underbrace{\begin{bmatrix}
X_{w}^{(1)} &  Y_{w}^{(1)} & Z_{w}^{(1)} & 1 & 0 & 0 & 0 & 0 & -u_1 X_w^{(1)} & -u_1 Y_w^{(1)} & -u_1 Z_w^{(1)} & -u_1\\
0 & 0 & 0 & 0 & X_{w}^{(1)} & Y_{w}^{(1)} & Z_{w}^{(1)} & 1 & -v_1 X_w^{(1)} & -v_1 Y_w^{(1)} & -v_1 Z_w^{(1)} & -v_1 \\
\vdots & \vdots & \vdots & \vdots & \vdots & \vdots & \vdots & \vdots & \vdots & \vdots & \vdots & \vdots \\
X_{w}^{(i)} &  Y_{w}^{(i)} & Z_{w}^{(i)} & 1 & 0 & 0 & 0 & 0 & -u_i X_w^{(i)} & -u_i Y_w^{(i)} & -u_i Z_w^{(i)} & -u_i\\
0 & 0 & 0 & 0 & X_{w}^{(i)} & Y_{w}^{(i)} & Z_{w}^{(i)} & 1 & -v_i X_w^{(i)} & -v_i Y_w^{(i)} & -v_i Z_w^{(i)} & -v_i \\
\vdots & \vdots & \vdots & \vdots & \vdots & \vdots & \vdots & \vdots & \vdots & \vdots & \vdots & \vdots \\
X_{w}^{(n)} &  Y_{w}^{(n)} & Z_{w}^{(n)} & 1 & 0 & 0 & 0 & 0 & -u_n X_w^{(n)} & -u_n Y_w^{(n)} & -u_n Z_w^{(n)} & -u_n\\
0 & 0 & 0 & 0 & X_{w}^{(n)} & Y_{w}^{(n)} & Z_{w}^{(n)} & 1 & -v_n X_w^{(n)} & -v_n Y_w^{(n)} & -v_n Z_w^{(n)} & -v_n
\end{bmatrix}}_{\text{Known } (2n \times 12) \text{ Matrix }  \mathbf{A}}
\underbrace{\begin{bmatrix}
p_{11} \\
p_{12} \\
p_{13} \\
p_{14} \\
p_{21} \\
p_{22} \\
p_{23} \\
p_{24} \\
p_{31} \\
p_{32} \\
p_{33} \\
p_{34} 
\end{bmatrix}}_{Unknown \ \mathbf{p}} =
\begin{bmatrix}
0 \\
0 \\
\vdots \\
0 \\
0 \\
\vdots \\
0 \\
0 \\
\end{bmatrix}$


![Solve $\mathbf{p}$ for $\mathbf{Ap=b=0}$](https://files.mdnice.com/user/1474/1edf66d3-f4d6-456c-ae06-8f1ea5ad12fd.png)

If matrix $\mathbf{A}$ has **MORE rows than columns (2n > 12)**, there are ***MORE equations than unknowns***, it often happens that $\mathbf{Ap=b=0}$ has ***NO solution***
- in this case, we could find **the best $\mathbf{p}$ (called least square solutions $\mathbf{\hat{p}}$)** that **minimizing** 
  $$
  \begin{aligned}
  \mathbf{E} &= \mathbf{\left\Vert Ap - b \right\Vert ^ 2 = \left\Vert Ap - 0 \right\Vert ^ 2} \\
  &= \mathbf{\left\Vert Ap \right\Vert ^ 2 = p^T A^T A p}
  \end{aligned}
  $$ 
  as small as possible,

#### Step 4. Least Squares Solution for $\mathbf{P}$
Since **Projection Matrix** acts on *Homogeneous Coordinates*, for any constanct $k \neq 0$, 

$$
\begin{aligned}
{\color{red} \tilde{x}} = 
& \begin{bmatrix}
\tilde{u} \\ \tilde{v} \\ \tilde{w}
\end{bmatrix} = \mathbf{P} {\color{blue}\bar{\mathbf{X}}_{\mathbf{w}}} \\

\equiv k
& \begin{bmatrix}
\tilde{u} \\ \tilde{v} \\ \tilde{w}
\end{bmatrix} =k \ \mathbf{P} {\color{blue}\bar{\mathbf{X}}_{\mathbf{w}}}
\end{aligned}
$$



- Therefore, Projection Matrices $\mathbf{P}$ and $k \mathbf{P}$ produce the **SAME Homogenous Pixel Coordinates**



![Scaling Projection Matrix, implies simultaneously scaling the World and Camera, which does NOT change the Image](https://files.mdnice.com/user/1474/a07b897f-8dd1-47f7-b66a-6d61fcc00fe3.png)

- We can **set projection matrix to some arbitrary scale** and it is convenient to set scale to

$$\min_{\mathbf{p}} \mathbf{\left\Vert Ap \right\Vert ^ 2} = \min_{\mathbf{p}} (\mathbf{p^T A^T A p})$$

$$\text{s.t. } \left\Vert  \mathbf{p} \right\Vert ^2 = \mathbf{p^T p} =1,$$

- Define a **Loss Function** and to minimize

$$L(\mathbf{p}, \lambda) = \mathbf{p^T A^T A p} - \lambda(\mathbf{p^T p} - 1)$$

- Let *the Partial Derivatives of Loss Function w.r.t. $\mathbf{p}$* be *0*:

$$\frac{\partial L}{\partial \mathbf{p}} = 2 \mathbf{A^T A p } - 2\lambda \mathbf{p} = 0$$
- it turns out that ***finding $\mathbf{p}$ that minimizes $L$*** is equivalent to ***solving the eigenvalue problem***:
$$\mathbf{A^T A p} = \lambda \mathbf{p}$$
- **Eigenvector** $\mathbf{p}$ **with Smallest Eigenvalue** $\lambda$ of matrix $\mathbf{A^T A p}$ minimizes the Loss Function 
$$L(\mathbf{p})$$
- Rearrange Solution $\mathbf{p}$ to form the Projection Matrix $\mathbf{P}$



#### Decompose (Extract) Intrinsic and Extrinsic Parameters
Given a **$3 \times 4$ Camera Matrix**
$$ \mathbf{P}  
= \begin{bmatrix}
p_{11} & p_{12} & p_{13} & p_{14} \\
p_{21} & p_{22} & p_{23} & p_{24} \\
p_{31} & p_{32} & p_{33} & p_{34}
\end{bmatrix}
$$

$$=
\underbrace{\begin{bmatrix}
\color{red}f_{x} & 0 & c_{x} & 0 \\
0 & \color{red}f_{y} & c_{y} & 0 \\
0 & 0 & \color{blue}1 & 0
\end{bmatrix}}_{{\begin{bmatrix}\mathbf{K \mid 0 } \end{bmatrix}}}
\underbrace{\begin{bmatrix}
r_{11} & r_{12} & r_{13} & t_{x} \\
r_{21} & r_{22} & r_{23} & t_{y} \\
r_{31} & r_{32} & r_{33} & t_{z} \\ 
0 & 0  & 0 & 1
\end{bmatrix}}_{\begin{bmatrix}
\mathbf{R} & \mathbf{t} \\
0 & 1
\end{bmatrix}}$$


- the first 3 columns of $\mathbf{P}$ is computed by 

$$=
\underbrace{\begin{bmatrix}
\color{red}f_{x} & 0 & c_{x}\\
0 & \color{red}f_{y} & c_{y}\\
0 & 0 & \color{blue}1 
\end{bmatrix}}_{{\mathbf{K}}}
\underbrace{\begin{bmatrix}
r_{11} & r_{12} & r_{13} \\
r_{21} & r_{22} & r_{23} \\
r_{31} & r_{32} & r_{33} 
\end{bmatrix}}_{\mathbf{R}}$$

#### Resources

[1] Richard Szeliski, *Computer Vision: Algorithms and Applications*, Springer; 2nd edition (2022)

[2] Richard Hartley, Andrew Zisserman, *Multiple View Geometry in Computer Vision*, Cambridge University Press; 2nd edition (2004)

[3] https://www.mathworks.com/help/vision/ug/camera-calibration.html  

[4] https://www.mauriciopoppe.com/notes/mathematics/geometry/projective-space/

