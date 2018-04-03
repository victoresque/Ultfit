import requests
import json


def getWeather():
  city_id = '1668341' # Taipei
  api_key = '-'
  r = requests.get('http://api.openweathermap.org/data/2.5/forecast?id=' + city_id + '&APPID=' + api_key)
  r = json.loads(r.text)
  return {
    "temp": int(r['list'][0]['main']['temp'] - 273.15),
    "temp_min": int(r['list'][0]['main']['temp_min'] - 273.15),
    "temp_max": int(r['list'][0]['main']['temp_max'] - 273.15),
    "weather": r['list'][0]['weather'][0]['main']
  }


if __name__ == '__main__':
  print(json.dumps(getWeather(), indent=4))
