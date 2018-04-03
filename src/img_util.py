import json
import numpy as np
import cv2
import requests
import subprocess


def captureImage():
  cap = cv2.VideoCapture(0)
  ret, frame = cap.read()
  frame = cv2.resize(frame, (400, 300))
  cap.release()
  return frame


def analyzeByAzure(img):
  print('Upload to Azure to analyze image...')
  cv2.imwrite('tmp/tmp.jpg', img)
  try:
    vision_base_url = "https://westus.api.cognitive.microsoft.com/vision/v1.0/"
    vision_analyze_url = vision_base_url + "analyze"
    subscription_key = '-'
    headers  = {'Ocp-Apim-Subscription-Key': subscription_key, 
                'Content-Type': 'application/octet-stream' }
    params   = {'visualFeatures': 'Categories,Description,Color'}
    image_path = 'tmp/tmp.jpg'
    image_data = open(image_path, "rb").read()
    response = requests.post(vision_analyze_url, headers=headers, params=params, data=image_data)
    response.raise_for_status()
    analysis = response.json()
    print('Analysis completed!')
  except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))
    print('Analysis failed!')
  return analysis


def removeIfNotOutfit(path):
  print('Upload to Azure to check if image contains outfit...')
  try:
    vision_base_url = "https://westus.api.cognitive.microsoft.com/vision/v1.0/"
    vision_analyze_url = vision_base_url + "analyze"
    subscription_key = '-'
    headers  = {'Ocp-Apim-Subscription-Key': subscription_key, 
                'Content-Type': 'application/octet-stream' }
    params   = {'visualFeatures': 'Categories,Description,Color'}
    image_data = open(path, "rb").read()
    response = requests.post(vision_analyze_url, headers=headers, params=params, data=image_data)
    response.raise_for_status()
    analysis = response.json()
  except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))
  
  tags = analysis['description']['tags'][:6]
  if 'person' not in tags and 'man' not in tags and 'woman' not in tags\
    and 'wearing' not in tags and 'girl' not in tags and 'people' not in tags:
    print(path+' removed.')
    subprocess.call(['rm', path])


def split_clothing(img):
  height = img.shape[0]
  width = img.shape[1]
  return img[:height//2, :, :], img[height//2:, :, :] 


if __name__ == '__main__':
  img = captureImage()
  result = analyzeByAzure(img)
  print(result)
