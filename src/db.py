import os
import json
import style
import img_util
import ig
import cv2


def visualizeClothingDatabase():
  clothing_db = getClothingDatabase()
  for _, entry in clothing_db.items():
    img = cv2.imread(entry['path'])
    cv2.destroyAllWindows()
    cv2.imshow(entry['caption'], img)
    cv2.waitKey()
  cv2.destroyAllWindows()


def getOutfitHistory():
  return json.load(open('user_db/outfit_history.json'))


def addOutfitHistory(outfit_ids):
  history = getOutfitHistory()
  history.append(outfit_ids)
  json.dump(history, open('user_db/outfit_history.json', 'w'))


def getClothingDatabase():
  return json.load(open('user_db/clothing_db.json'))  


def addClothingByImage(img):
  db = getClothingDatabase()
  if len(db):
    cloth_id = int(max([int(k) for k in db.keys()])) + 1
  else:
    cloth_id = 0
  desc = img_util.analyzeByAzure(img)
  # print(json.dumps(desc, indent=4))
  db[cloth_id] = {
    'path': 'user_db/clothing_img/' + str(cloth_id) + '.jpg',
    'caption': desc['description']['captions'][0]['text'],
    'tags': desc['description']['tags'],
    'color': desc['color']['dominantColors'],
    'accent': desc['color']['accentColor']
  }
  cv2.imwrite(db[cloth_id]['path'], img)
  json.dump(db, open('user_db/clothing_db.json', 'w'))
  return db[cloth_id]


def removeClothingById(cloth_id):
  db = getClothingDatabase()
  cloth_id = str(cloth_id)
  if cloth_id in db.keys():
    del db[cloth_id]
  json.dump(db, open('user_db/clothing_db.json', 'w'))


def getIgFollowing():
  follow = json.load(open('user_db/ig_follow.json'))
  return follow


if __name__ == '__main__':
  follow = getIgFollowing()
  for user in follow:
    ig.getImagesFromIgUser(user, 3)

  while True:
    img = img_util.captureImage()
    addClothingByImage(img)
    print(json.dumps(getClothingDatabase(), indent=4, sort_keys=True))
    input()
