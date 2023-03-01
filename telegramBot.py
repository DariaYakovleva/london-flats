import requests
import json
from env import ADMIN_CHAT_ID, BOT_API


def getBeds(title):
  beds = ['studio', '1 bed', '2 bed', '3 bed', '4 bed']
  for bed in beds:
    if bed in title.lower():
      return bed.replace(' ', '')


def logStatus(text):
  params = {'chat_id': ADMIN_CHAT_ID, 'text': text}
  requests.post(BOT_API + 'sendMessage', params)
  # print(text)


def sendFlat(district, flat, chatId):
  title = '#{} #{}'.format(district.replace('-', ''), getBeds(flat['Title']))
  text = '\n'.join([title] + [
    str(v)
    for k, v in flat.items() if k not in ['Photo', 'FloorPlanLink'] and v != ''
  ])
  photo = flat['FloorPlanLink'] if flat['FloorPlanLink'] else flat['Photo']

  if flat['FloorPlanLink'] and flat['Photo']:
    media = json.dumps([{
      'type': 'photo',
      'media': flat['Photo']
    }, {
      'type': 'photo',
      'media': flat['FloorPlanLink']
    }])
    params = {'chat_id': chatId, 'media': media, 'disable_notification': True}
    requests.post(BOT_API + 'sendMediaGroup', params)

    params = {
      'chat_id': chatId,
      'text': text,
      'disable_web_page_preview': True
    }
    requests.post(BOT_API + 'sendMessage', params)
  elif photo:
    params = {'chat_id': chatId, 'caption': text, 'photo': photo}
    requests.post(BOT_API + 'sendPhoto', params)
  else:
    params = {'chat_id': chatId, 'text': text}
    requests.post(BOT_API + 'sendMessage', params)
