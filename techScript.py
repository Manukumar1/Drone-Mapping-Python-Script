# -*- coding: utf-8 -*-
"""
Created on Tue Dec 18 23:44:44 2018

@author: Manu kumar
"""

"""Importing all the required packages"""

import glob
import pysrt
import piexif
import csv

from datetime import datetime, timedelta
import haversine

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

      for img in glob.glob('images/*.jpg'):           # finds all the images having .JPG image format
            imgName = img.strip('images\ ')   
            img_path = '/'.join([imgDirectory, imgName])
#            print(img_path)
            imgMetadata = getMetadataImage(img_path)

            imgToGPScoordinates[imgName] = (imgMetadata)    # imgToGPScoordinates stores all the image's latitude and longitude info
 
      return imgToGPScoordinates

def getImgWithinRadius(currCoordinate, imgToGPScoordinates, Radius):
      
      """Get all the Images within the specified radius"""
      """By calculating the distance between the two coordinates by using haversine formula"""
      
      imgDir = []
      
#      for nextCoordinate in range(len(imgToGPScoordinates)):
      for img, nextCoordinate in imgToGPScoordinates.items():
#            dist = (haversineNew.distance(currCoordinate, nextCoordinate))
            dist = (haversine.distance((currCoordinate), (nextCoordinate)))
            if dist <= Radius:
                  imgDir.append(img)
#      print(imgDir)
      return imgDir           # Directory of all such images

def getSubtitlesSlice(subs, currTime, endTime):
      
      """Get the items within the time interval by slicing the subtitle SRT file"""
      
      slicedSub = subs.slice(starts_after={'minutes': currTime.minute, 'seconds': currTime.second}, 
                             ends_before={'minutes': endTime.minute, 'seconds': endTime.second})
      return slicedSub

def getCoordinatesWithinSub(sub):
      """The SRT file has 3 parts in each data item: currLongitude, currLatitude, 0"""
      currLon, currLat, zero = sub.text.split(',')

      # As we only need the currLatitude and currLongitude information
      return (currLat, currLon)

def getImageListWithinRadius(subsList, imgToGPScoordinates, Radius):
      """List/directory of Images within specified radius from the subtitle items's coordinates"""
      
      imgDir = []
      for sub in subsList:
            imgDir = imgDir + getImgWithinRadius(getCoordinatesWithinSub(sub), imgToGPScoordinates, Radius)
      
      return imgDir


def readFromCSVfile(CSVfileName):
      
      CSVdata = []
#      assetNameList = []
#      longitudeList = []
#      latitudeList = []
      
      with open(CSVfileName, mode='r') as CSV_file:
            CSV_reader = csv.DictReader(CSV_file)
            for row in CSV_reader:
                  CSVdata.append(row)
#                  assetNameList.append(row['asset_name'])
#                  longitudeList.append(row['longitude'])
#                  latitudeList.append(row['latitude'])
                  
#      CSVdata = [assetNameList,longitudeList,latitudeList]
      return CSVdata

def writeToCSVfile(data, CSVfileName):
      with open(CSVfileName, mode='w') as newCSVfile:
            CSV_writer = csv.writer(newCSVfile, dialect='excel')
            CSV_writer.writerows(data)
            
def getMetadataImage(imageName):
      
      exif_dict = piexif.load(imageName) 
      GPSinfo = exif_dict.pop("GPS")     # Returns exif data as a dictionary with the “GPS” key
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

      except:
            print("End of folder/files detected")
            OutputGPSdata = 0
      
      if(OutputGPSdata == 0):
            return []
      
      return OutputGPSdata[0],OutputGPSdata[1]

def DMStoDD(deg1, mins1, secs1, deg2, mins2, secs2):
      """ To convert coordinate from Degree-minutes-seconds format to Decimal-Degree format"""
      
      dd1 = deg1 + (mins1/60) + (secs1/3600)
      
      dd2 = deg2 + (mins2/60) + (secs2/3600)
      
      return dd1, dd2

def ImagesNearVideo(video, vidLocation, imgToGPScoordinates):
      
      srt = pysrt.open(vidLocation)
      currentTime = datetime(2018, 1, 1, minute = 0, second = 0)
      nextTime = currentTime + timedelta(seconds = 1)             # To find all the coordinates in the SRT file for a single second
      
      DataForCSV = []
      DataForCSV.append(["Time(in sec)", "Images"])
      
      while True:
         slices = getSubtitlesSlice(srt, currentTime, nextTime)
         if not slices:
               break
         imgList = getImageListWithinRadius(slices, imgToGPScoordinates, vidRadius)
         currentTime = nextTime
         nextTime = nextTime + timedelta(seconds = 1)
         
         DataForCSV.append([currentTime.strftime("%M:%S"), ", ".join(imgList)])

      writeToCSVfile(DataForCSV, FileNameGenerator("video_" + video, "csv"))
      
      print("CSV file for video: {0} generated and saved.".format("video_" + video))

def AllVideos(vidLocation, imgToGPScoordinates):
      for vid in glob.glob('videos/*.srt'):
            vid = vid.strip('videos\ ')   
            vid_path = '/'.join([vidLocation, vid])
            
            ImagesNearVideo(vid, vid_path, imgToGPScoordinates)

def FileNameGenerator(filename, extension):
      fileName = filename.split(".")[0]   # Retain only the filename part without the previous extension
      
      return fileName + "." + extension
      
def imagesForPOI(POIfile, imgToGPScoordinates, Radius):
      POIdata = readFromCSVfile(POIfile)
      
      imageList = []
      imageList.append(["asset_name", "longitude", "latitude", "images"])
      for asset in POIdata:
            currCoordinate = (asset["latitude"], asset["longitude"])
            imgs = getImgWithinRadius(currCoordinate, imgToGPScoordinates, Radius)
            imageList.append([asset["asset_name"], asset["longitude"], asset["latitude"], ", ".join(imgs)])
      writeToCSVfile(imageList, FileNameGenerator("imgFrom" + POIfile, "csv"))
      print("CSV file for POI: {0} generated and saved.".format("imgFromassets.csv"))

      
#--------------------- Taking Inputs from users ----------------------
vidRadius = int(input("Enter the radius(in meters) of video coverage: "))
POIRadius = int(input("Enter the radius(in meters) for Points of Interest: "))

#-------------------------- To run the script -------------------------
imgToGPScoordinates = imgMapping("images")

AllVideos(videoDirectory, imgToGPScoordinates)

imagesForPOI(POIfileName, imgToGPScoordinates, POIRadius)