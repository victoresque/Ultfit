import json
import db
import ig
import outfit
import weather
import img_util


if __name__ == '__main__':
  '''
    TODO(0): face recognition for member recognition

    TODO(1): calculate user clothing encode
    TODO(1): add/remove from database

    TODO(1): split clothing parts in instagram photo
    TODO(1): calculate instagram photo encode

    TODO(1): use encode, weather, and instagram photo to calculate a score
    TODO(0): randomly get an outfit for you

    TODO(0): tinder-like interface
  '''
  while True:
    print("\n------------------------------\n"
          "* Main interface\n"
          "    0: GET MY OUTFIT TODAY!!!\n"
          "    1: * capture image and add clothing\n"
          "    2: * download from instagram followers (with clean up)\n"
          "\n"
          "    3: * get weather\n"
          "    4: * view clothing database\n"
          "    5: * view random IG images\n"
          "\n"
          "    6: * remove clothing\n"
          "    7: * view raw database\n"
          "    8: * clean up IG images\n"
          "------------------------------\n")
    opt = int(input("option: "))
    
    if opt == 0:
      f = outfit.getOutfit()

    elif opt == 1:
      img = img_util.captureImage()
      db.addClothingByImage(img)

    elif opt == 2:
      ig.getImagesFromIgFollows()

    elif opt == 3:
      print(json.dumps(weather.getWeather(), indent=4, sort_keys=True))

    elif opt == 4:
      db.visualizeClothingDatabase()

    elif opt == 5:
      ig.visualizeIgDatabase()

    elif opt == 6:
      id = input('  Enter cloth id: ')
      db.removeClothingById(id)

    elif opt == 7:
      print(json.dumps(db.getClothingDatabase(), indent=4, sort_keys=True))
      
    elif opt == 8:
      ig.resizeIgImages()
      ig.removeImagesNotOutfit()

