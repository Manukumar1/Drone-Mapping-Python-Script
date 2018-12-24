# -*- coding: utf-8 -*-
"""
Created on Tue Dec 18 23:44:44 2018

@author: Manu kumar
"""

"""Importing all the required packages"""

import glob     # glob finds all the pathnames matching a specified pattern
import pysrt    # pysrt is used to edit or create SubRip files.
import piexif   # Piexif simplifies interacting with EXIF data in Python.
import csv      # csv is used to read and write sequences.

from datetime import datetime, timedelta  # The datetime module supplies classes for manipulating dates and times
import haversine  # haversine is used to calculate distance between two GPS coordinates


"""Declaring all the required information/variables"""
                      
imgDirectory = "images"
videoDirectory = "videos"
POIfileName = "assets.csv"
imgFormat = "*.jpg"
videoFormat = "*.srt"

def imgMapping(imgDirectory):
      
      '''Make a dict to map all the images from the image directory 
      to their GPS coordinates from the EXIF data stored within them '''
      
      imgToGPScoordinates = {}

      for img in glob.glob('images/*.jpg'):           # finds all the images having .JPG image format inside the "images" folder
            imgName = img.strip('images\ ')   
            img_path = '/'.join([imgDirectory, imgName])

            imgMetadata = getMetadataImage(img_path)
            imgToGPScoordinates[imgName] = (imgMetadata)    # imgToGPScoordinates stores all the image's latitude and longitude info
 
      return imgToGPScoordinates

def getImgWithinRadius(currCoordinate, imgToGPScoordinates, Radius):
      
      """Get all the Images within the specified radius"""
      """By calculating the distance between the two coordinates by using haversine formula"""
      
      imgDir = []
      
      for img, nextCoordinate in imgToGPScoordinates.items():
            dist = (haversine.distance((currCoordinate), (nextCoordinate)))
            if dist <= Radius:              # To know if the image is within the radius
                  imgDir.append(img)

      return imgDir           # List of all such images

def getSubtitlesSlice(subs, currTime, endTime):
      
      """Get the items within the time interval by slicing the subtitle SRT file"""
      
      slicedSub = subs.slice(starts_after={'minutes': currTime.minute, 'seconds': currTime.second}, 
                             ends_before={'minutes': endTime.minute, 'seconds': endTime.second})
      return slicedSub

def getCoordinatesWithinSub(sub):
      """The SRT file has 3 parts in each data item: currLongitude, currLatitude, 0"""
      
      currLon, currLat, zero = sub.text.split(',')

      # As we only need the currLatitude and currLongitude information. We are also reversing the order of output of the coordinate.
      return (currLat, currLon)

def getImageListWithinRadius(subsList, imgToGPScoordinates, Radius):
      """List/directory of Images within specified radius from the subtitle items's coordinates"""
      
      imgDir = []
      for sub in subsList:
            imgDir = imgDir + getImgWithinRadius(getCoordinatesWithinSub(sub), imgToGPScoordinates, Radius)
      
      return imgDir


def readFromCSVfile(CSVfileName):
      """Function to read data from a CSV file and store it into a CSVdata list"""
      CSVdata = []
      
      with open(CSVfileName, mode='r') as CSV_file:
            CSV_reader = csv.DictReader(CSV_file)
            for row in CSV_reader:
                  CSVdata.append(row)

      return CSVdata

def writeToCSVfile(data, CSVfileName):
      """Function to write data into a CSV file"""
      
      with open(CSVfileName, mode='w') as newCSVfile:
            CSV_writer = csv.writer(newCSVfile, dialect='excel')
            CSV_writer.writerows(data)
            
def getMetadataImage(imageName):
      """ Function to extract the Metadata/EXIF data from an image file"""
      
      exif_dict = piexif.load(imageName) 
      GPSinfo = exif_dict.pop("GPS")      # Returns exif data as a dictionary with the “GPS” key
      img = imageName[7:]                 # To slice the image name to exact file name(and ignore the file directory)
      
      """Example of Metadata : 
            
      GPSInfo	{0: b'\x02\x03\x00\x00', 
      1: 'N', 
      2: ((19, 1), (9, 1), (188978, 10000)),    # Latitude
      3: 'E', 
      4: ((73, 1), (0, 1), (191383, 10000)),    # Longitude
      5: b'\x00', 6: (63739, 1000)} """
      
      try:
           GPS_data = []
           
           Lat = [GPSinfo[2][0],GPSinfo[2][1],GPSinfo[2][2]]
           
           Lon = [GPSinfo[4][0],GPSinfo[4][1],GPSinfo[4][2]]
           
           #Latitude
           GPS_data.append((float(Lat[0][0]))/(float(Lat[0][1])))      #Degrees
           GPS_data.append((float(Lat[1][0]))/(float(Lat[1][1])))      #Minutes
           GPS_data.append((float(Lat[2][0]))/(float(Lat[2][1])))      #Seconds
           
           #Longitude
           GPS_data.append((float(Lon[0][0]))/(float(Lon[0][1])))      #Degrees
           GPS_data.append((float(Lon[1][0]))/(float(Lon[1][1])))      #Minutes
           GPS_data.append((float(Lon[2][0]))/(float(Lon[2][1])))      #Seconds
           
           OutputGPSdata = DMStoDD(GPS_data[0], GPS_data[1], GPS_data[2], GPS_data[3], GPS_data[4], GPS_data[5])
           # To convert the coordinate from Degree-minutes-seconds format to Decimal-Degree format.
           # After the conversion, OutputGPSdata will get the coordinate in DD form for Latitude and Longitude.

      except:
            print("End of folder/files detected")
            OutputGPSdata = 0
      
      if(OutputGPSdata == 0):
            return []   # If an image file has no GPSInfo, then we will return an empty list element.
      
      return OutputGPSdata[0],OutputGPSdata[1]  # To return Latitude, Longitude coordinates

def DMStoDD(deg1, mins1, secs1, deg2, mins2, secs2):
      """ To convert coordinate from Degree-minutes-seconds format to Decimal-Degree format"""
      
      dd1 = deg1 + (mins1/60) + (secs1/3600)    # For Latitude
      
      dd2 = deg2 + (mins2/60) + (secs2/3600)    # For Longitude
      
      return dd1, dd2

def ImagesNearVideo(video, vidLocation, imgToGPScoordinates):
      """ Function for finding all the images that lie near the coordinates listed in the SRT subtitle file. """
      
      srt = pysrt.open(vidLocation)
      currentTime = datetime(2018, 1, 1, minute = 0, second = 0)
      nextTime = currentTime + timedelta(seconds = 1)             # To find all the coordinates in the SRT file for a single second
      
      DataForCSV = []
      DataForCSV.append(["Time(in sec)", "Images"])         # Used in writing column names in a CSV file
      
      while True:
         slices = getSubtitlesSlice(srt, currentTime, nextTime)
         if not slices:
               break
         imgList = getImageListWithinRadius(slices, imgToGPScoordinates, vidRadius)       # To get the list of images wihin radius for each second slice of the SRT file
         currentTime = nextTime                             # increament the currentTime
         nextTime = nextTime + timedelta(seconds = 1)       # increament the nextTime
         
         DataForCSV.append([currentTime.strftime("%M:%S"), ", ".join(imgList)])           # To append new row to the CSV file with currentTime and image list data

      writeToCSVfile(DataForCSV, FileNameGenerator("video_" + video, "csv"))
      
      print("CSV file for video: {0} generated and saved.".format("video_" + video))      # Output message for console screen to indicate CSV file generation to the user


def AllVideos(vidLocation, imgToGPScoordinates):
      """ To execute through each video file in the video directory in the same procedure"""
      
      for vid in glob.glob('videos/*.srt'):           # finds all the subtitle files having .SRT subtitle format inside the "videos" folder
            vid = vid.strip('videos\ ')   
            vid_path = '/'.join([vidLocation, vid])
            
            ImagesNearVideo(vid, vid_path, imgToGPScoordinates)   # Used to run over all the SRT files and get data.


def FileNameGenerator(filename, extension):
      """Function used to generate a filename. It is used whenever we are generating a new file(e.g. CSV files)"""
      
      fileName = filename.split(".")[0]   # Retain only the filename part without the previous extension
      
      return fileName + "." + extension   # Output the new generated filename
      
def imagesForPOI(POIfile, imgToGPScoordinates, Radius):
      """Function to read the POI CSV file and write new output data in a new CSV file"""
      
      POIdata = readFromCSVfile(POIfile)  
      
      imageList = []
      imageList.append(["asset_name", "longitude", "latitude", "images"])        # Used in writing column names in a CSV file
      
      for asset in POIdata:
            currCoordinate = (asset["latitude"], asset["longitude"])
            imgs = getImgWithinRadius(currCoordinate, imgToGPScoordinates, Radius)
            imageList.append([asset["asset_name"], asset["longitude"], asset["latitude"], ", ".join(imgs)])   
            # To append new row to the CSV file with asset_name, longitude, latitude and image name data
            
      writeToCSVfile(imageList, FileNameGenerator("imgFrom" + POIfile, "csv"))
      
      print("CSV file for POI: {0} generated and saved.".format("imgFromassets.csv"))     # Output message for console screen to indicate CSV file generation to the user

      

"""--------------------- Taking Inputs from users ----------------------"""

vidRadius = int(input("Enter the radius(in meters) of video coverage: "))
POIRadius = int(input("Enter the radius(in meters) for Points of Interest: "))


"""-------------------------- To run the script -------------------------"""
imgToGPScoordinates = imgMapping("images")

AllVideos(videoDirectory, imgToGPScoordinates)

imagesForPOI(POIfileName, imgToGPScoordinates, POIRadius)