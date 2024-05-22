## RGBD Sensor Notes Notes 02 | How to Install Sensor SDK on Linux

> This note is the second in a series of RGBD Sensor  Notes, documenting how to install the Intel® RealSense™ Depth Sensor SDK on Linux OS.
> 
### Video Tutorial

https://youtu.be/C5LLk8MkJkw?si=0GiKKcTONZQ2tL_5 

### Step 0. Go to librealsense Github Page
Go `https://github.com/IntelRealSense/librealsense/blob/master/doc/distribution_linux.md`
- and follow the document


![The latest released version is v2.55.1 on 2024.04.22 ](https://files.mdnice.com/user/1474/a172ebeb-fec1-4621-9458-b820c0c54164.png)

- The latest released version is v2.55.1 on 2024.04.22

### Step 1. Register the server's public key:
```shell
$ sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-key F6E65AC044F831AC80A06380C8B3A55A6F3EFCDE || sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-key F6E65AC044F831AC80A06380C8B3A55A6F3EFCDE
```

### Step 2. Add the server to the list of repositories:
```shell
$ sudo add-apt-repository "deb https://librealsense.intel.com/Debian/apt-repo $(lsb_release -cs) main" -u
```

### Step 3. Install the libraries
```shell
$ sudo apt-get install librealsense2-dkms
$ sudo apt-get install librealsense2-utils
$ sudo apt-get install librealsense2-dev
$ sudo apt-get install librealsense2-dbg
```
### Step 4. Verify the installation
Connect the Intel RealSense depth camera and run：
```SHELL
$ realsense-viewer
```
