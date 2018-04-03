import os
import db
import ig
import style
import cv2
import img_util
import weather
import numpy as np


def getOutfit():
  weather_data = weather.getWeather()
  print(weather_data)

  clothing_encode = []
  clothing_weather = []
  clothing_type = []
  clothing_db = db.getClothingDatabase()
  for _, entry in clothing_db.items():
    img = cv2.imread(entry['path'])
    enc = style.getStyleEncodeFromImg(img)
    clothing_encode.append(enc)

    if 'pants' in entry['tags']:
      clothing_type.append('lower')
    elif 'shirt' in entry['tags']:
      clothing_type.append('upper')
    else:
      clothing_type.append('-----')

    if 'pants' in entry['tags']:
      clothing_weather.append('cold')
    elif 'shorts' in entry['tags']:
      clothing_weather.append('hot')
    else:
      clothing_weather.append('warm')

  ig_clothing_encode = []
  ig_clothing_type = []
  follow = db.getIgFollowing()
  for user in follow:
    img_files = os.listdir('ig_img/'+user+'/')
    for img_file in img_files:
      path = 'ig_img/'+user+'/'+img_file
      img = cv2.imread(path)
      img_upper, img_lower = img_util.split_clothing(img)
      enc = style.getStyleEncodeFromImg(img_upper)
      ig_clothing_encode.append(enc)
      ig_clothing_type.append('upper')
      enc = style.getStyleEncodeFromImg(img_lower)
      ig_clothing_encode.append(enc)
      ig_clothing_type.append('lower')
  
  print(clothing_encode)
  print(clothing_type)
  print(ig_clothing_encode)
  print(ig_clothing_type)
  

def calculateSimilarity(enc1, enc2):
  return np.abs(enc1 - enc2)


def calculateScore(weather_data, outfit1, outfit2):
  score = 1.0

  enc1_upper = outfit1[0]['enc']
  enc1_lower = outfit1[1]['enc']
  enc2_upper = outfit2[0]['enc']
  enc2_lower = outfit2[1]['enc']

  score = score * calculateSimilarity(enc1_upper, enc2_upper)
  score = score * calculateSimilarity(enc1_lower, enc2_lower)

  type1_upper = outfit1[0]['weather']
  type1_lower = outfit1[1]['weather']

  if weather_data['temp'] < 20: # cold
    score = score if type1_upper == 'cold' else score * 0.9
    score = score if type1_lower == 'cold' else score * 0.9
  elif weather_data['temp'] > 30: # hot
    score = score if type1_upper == 'hot' else score * 0.9
    score = score if type1_lower == 'hot' else score * 0.9

  return score
