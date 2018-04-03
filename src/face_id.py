import json
import numpy as np
import cv2
import requests
import img_util


def addPersonGroup():
  print('Adding person group "makentu"...')
  try:
    face_api_url = "https://westus.api.cognitive.microsoft.com/face/v1.0/persongroups/makentu"
    subscription_key = '-'
    headers  = {'Ocp-Apim-Subscription-Key': subscription_key,
                'Content-Type': 'application/json'}
    params = {}
    body = {'name': 'makentu'}
    response = requests.put(face_api_url, headers=headers, params=params, json=body)
    response.raise_for_status()
    print('Group added!')
  except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))
    print('Group adding failed!')


def addPerson(name):
  print('Adding person '+name+'...')
  try:
    face_api_url = "https://westus.api.cognitive.microsoft.com/face/v1.0/persongroups/makentu/persons"
    subscription_key = '-'
    headers  = {'Ocp-Apim-Subscription-Key': subscription_key,
                'Content-Type': 'application/json'}
    params = {}
    body = {'name': name}
    response = requests.post(face_api_url, headers=headers, params=params, json=body)
    personId = json.loads(response.text)['personId']
    id_db = json.load(open('user_db/azure_personid.json'))
    id_db[name] = personId
    json.dump(id_db, open('user_db/azure_personid.json', 'w'))
    response.raise_for_status()
    print('Person added!')
  except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))
    print('Person adding failed!')


def addFace(img, name):
  print('Adding face to Azure Face API...')
  cv2.imwrite('tmp/tmp.jpg', img)
  id_db = json.load(open('user_db/azure_personid.json'))
  personId = id_db[name]
  try:
    face_api_url = "https://westus.api.cognitive.microsoft.com/face/v1.0/persongroups/makentu/persons/"+personId+"/"+"/persistedFaces"
    subscription_key = '-'
    headers  = {'Ocp-Apim-Subscription-Key': subscription_key,
                'Content-Type': 'application/octet-stream'}
    params   = {}
    image_path = 'tmp/tmp.jpg'
    image_data = open(image_path, "rb").read()
    response = requests.post(face_api_url, headers=headers, params=params, data=image_data)
    print(response.status_code)
    response.raise_for_status()
    analysis = response.json()
    print('Face added!')
  except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))
    print('Face adding failed!')
  return analysis


def trainPersonGroup():
  print('Training person group makentu...')
  try:
    face_api_url = "https://westus.api.cognitive.microsoft.com/face/v1.0/persongroups/makentu/train"
    subscription_key = '-'
    headers  = {'Ocp-Apim-Subscription-Key': subscription_key}
    response = requests.post(face_api_url, headers=headers)
    response.raise_for_status()
    print('Trained!')
  except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))
    print('Training failed!')


def detectFace(img):
  print('Upload to Azure Face API to detect face...')
  cv2.imwrite('tmp/tmp.jpg', img)
  try:
    face_api_url = "https://westus.api.cognitive.microsoft.com/face/v1.0/detect"
    subscription_key = '-'
    headers  = {'Ocp-Apim-Subscription-Key': subscription_key,
                'Content-Type': 'application/octet-stream'}
    params   = {}
    '''
    params   = {'returnFaceLandmarks': 'true',
                'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise'}
    '''
    image_path = 'tmp/tmp.jpg'
    image_data = open(image_path, "rb").read()
    response = requests.post(face_api_url, headers=headers, params=params, data=image_data)
    response.raise_for_status()
    analysis = response.json()
    print('Face detection done!')
  except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))
    print('Face detection failed!')
  if len(analysis):
    return analysis[0]['faceId']
  else:
    return None


def identifyByFace(img):
  faceId = detectFace(img)
  if faceId is None:
    return None
  print('Upload to Azure Face API to identify person...')
  try:
    face_api_url = "https://westus.api.cognitive.microsoft.com/face/v1.0/identify"
    subscription_key = '-'
    headers  = {'Ocp-Apim-Subscription-Key': subscription_key,
                'Content-Type': 'application/json'}
    params   = {}
    body     = {'faceIds': [faceId],
                'personGroupId': 'makentu'}
    response = requests.post(face_api_url, headers=headers, params=params, json=body)
    print(response.text)
    response.raise_for_status()
    analysis = response.json()
    print('Face identification done!')
  except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))
    print('Face identification failed!')
  if len(analysis):
    if len(analysis[0]['candidates']):
      return analysis[0]['candidates'][0]['personId']
    else:
      return None
  else:
    return None


def faceIdToName(faceId):
  id_db = json.load(open('user_db/azure_personid.json'))
  for key, value in id_db.items():
    if value == faceId:
      return key
  return 'No this person'


if __name__ == '__main__':
  # Done creating person group
  # addPersonGroup()

  # Done adding people
  # addPerson('Victor Huang')
  # addPerson('Danny Tsai')
  # addPerson('Adelaide Hsu')
  # addPerson('Chen')
  
  '''
  img = img_util.captureImage()
  cv2.imshow('', img)
  cv2.waitKey()
  name = input("Name of person: ")
  print(name)
  input()
  result = addFace(img, name)
  '''

  # trainPersonGroup()

  img = img_util.captureImage()
  faceId = identifyByFace(img)
  if faceId:
    print(faceIdToName(faceId))
