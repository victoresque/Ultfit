import os
import subprocess
import db
import cv2
import img_util
import random


def resizeIgImages():
  follow = db.getIgFollowing()
  filenames = []
  for user in follow:
    img_files = os.listdir('ig_img/'+user+'/')
    for img_file in img_files:
      path = 'ig_img/'+user+'/'+img_file
      filenames.append(path)
  for filename in filenames:
    img = cv2.imread(filename)
    img = cv2.resize(img, (400, int(img.shape[1] * (400 / img.shape[0]))))
    cv2.imwrite(filename, img)


def getImagesFromIgUser(user, maximum):
  maximum = maximum - 1
  subprocess.call(['instagram-scraper', user, '--latest', '--maximum',
            str(maximum), '--destination', 'ig_img/'+user])
  subprocess.call(['rm', 'instagram-scraper.log'])


def removeImagesNotOutfit():
  follow = db.getIgFollowing()
  for user in follow:
    img_files = os.listdir('ig_img/'+user+'/')
    for img_file in img_files:
      path = 'ig_img/'+user+'/'+img_file
      img_util.removeIfNotOutfit(path)


def getImagesFromIgFollows():
  follow = db.getIgFollowing()
  for user in follow:
    getImagesFromIgUser(user, 3)
  resizeIgImages()
  removeImagesNotOutfit()


def visualizeIgDatabase():
  follow = db.getIgFollowing()
  filenames = []
  for user in follow:
    img_files = os.listdir('ig_img/'+user+'/')
    for img_file in img_files:
      path = 'ig_img/'+user+'/'+img_file
      filenames.append(path)
  random.shuffle(filenames)
  filenames = filenames[:4]
  for filename in filenames:
    img = cv2.imread(filename)
    cv2.destroyAllWindows()
    cv2.imshow('', img)
    cv2.waitKey()
  cv2.destroyAllWindows()


if __name__ == '__main__':
  print(getImagesFromIgUser('vichuang1997', 3))
