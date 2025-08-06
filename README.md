# Drone Mapping

## Getting Started

First download the whole repository into your PC. Then all you need is to run the python program **techScript.py** , provide the inputs for:
* Radius(in meters) of video coverage
* Radius(in meters) for Points of Interest

### Prerequisites

First you should have **Python 3** or above version of Python installed in your PC. If it's not installed one can easily install it through following links:

* [Installing Python 3 on Windows](https://docs.python-guide.org/starting/install3/win/)
* [Installing Python 3 on Mac OS X](https://docs.python-guide.org/starting/install3/osx/)
* [Installing Python 3 on Linux](https://docs.python-guide.org/starting/install3/linux/)

We need to then, install **Anaconda** software.
* [Installing Anaconda on Windows](https://docs.anaconda.com/anaconda/install/windows/)
* [Installing Anaconda on macOS](https://docs.anaconda.com/anaconda/install/mac-os/)
* [Installing Anaconda on Linux](https://docs.anaconda.com/anaconda/install/linux/)


### Installing

After installing python 3 and Anaconda softwares succesfully, we need to install all the necessary packages in order to run the script.
```
pip install pysrt
```
```
pip install piexif
```

**glob, math, csv, datetime** are the other packages used for this script. As they come built-in with Python, hence we don't need to install them separately.

## Sample Input

Enter the radius(in meters) of video coverage: **35**


Enter the radius(in meters) for Points of Interest: **50**

## Running the tests

After entering the required details, click Enter key and wait for few seconds for the command line to display message as:

**CSV file for video: video_DJI_0301.csv generated and saved.**


**CSV file for POI: imgFromassets.csv generated and saved.**

## Sample Input/Output Console Screen
![alt text](https://github.com/Manukumar1/Skylark-Drones-Technical-Assignment/blob/master/SampleOutputConsoleScreen.png "SampleOutputConsoleScreen")

## Output Video CSV
![alt text](https://github.com/Manukumar1/Skylark-Drones-Technical-Assignment/blob/master/OutputVideoCSV.png "OutputVideoCSV")

## Output Assets CSV
![alt text](https://github.com/Manukumar1/Skylark-Drones-Technical-Assignment/blob/master/OutputAssetsCSV.png "OutputAssetsCSV")

## Built With

* [Anaconda Spyder 3.3.1](https://www.anaconda.com/download/) - The IDE used
* [Python 3.7](https://www.python.org/downloads/) - Programming language used

## Authors

* **Manukumar Rudresh** - [Manukumar1](https://github.com/Manukumar1)

See also the list of [contributors](https://github.com/Manukumar1/Skylark-Drones-Technical-Assignment/graphs/contributors) who participated in this project.

## Acknowledgments

* Wayne Dyck - [snippet](https://gist.github.com/rochacbruno/2883505) for Haversine formula to calculate the distance between two GPS coordinates.
