from env import Params, REDIS_CLIENT, DISTRICTS_MAP
from zoopla import getZooplaFlats
from rightmove import getRightMoveFlats, parseRightMoveFlat
from telegramBot import sendFlat, logStatus
from datetime import datetime
from utils import getChats, getChatParams, calculateHash


def runSearch(chatId, params):
  flatType = params[Params.FLAT_TYPE]
  minBeds, minPrice, maxPrice = map(
    int,
    [params[Params.MINBEDS], params[Params.MINPRICE], params[Params.MAXPRICE]])
  districts = [
    x.strip().lower().replace(' ', '-')
    for x in params[Params.DISTRICTS].split(',')
  ]
  filters = params.get(Params.FILTERS, {})

  print(chatId, flatType, minBeds, minPrice, maxPrice, districts, filters)

  not_found = []
  flatHashes = {}
  for district in districts:
    code = DISTRICTS_MAP.get(district, None)
    if code is None:
      not_found.append(district)
      continue
    rightMoveFlats = getRightMoveFlats(flatType, code, minBeds, maxPrice,
                                       minPrice)
    rightMoveNew = 0
    for flatLink in rightMoveFlats:
      redisKey = '{}_{}'.format(chatId, flatLink)
      if (REDIS_CLIENT.get(redisKey) != None):
        continue
      rightMoveFlat = parseRightMoveFlat(flatLink)
      if filters and (rightMoveFlat['Tenure'] not in filters
                      or rightMoveFlat['PropertyType'] not in filters):
        continue
      sendFlat(district, rightMoveFlat, chatId)
      REDIS_CLIENT.set(redisKey, 1)
      flatHashes[calculateHash(rightMoveFlat)] = 1
      rightMoveNew += 1
    print('[{}] rightmove, {}, new: {}/{}'.format(chatId, district,
                                                  rightMoveNew,
                                                  len(rightMoveFlats)))
    if rightMoveNew == 0:
      continue

    zooplaFlats = getZooplaFlats(flatType, district, minBeds, maxPrice,
                                 minPrice)
    zooplaNew = 0
    for flatLink, zooplaFlat in zooplaFlats.items():
      # print(flatLink, redis_client.get(flatLink))
      if flatHashes.get(calculateHash(zooplaFlat), 0):
        # print('SAME FLAT FOUND', zooplaFlat)
        continue
      redisKey = '{}_{}'.format(chatId, flatLink)
      if (REDIS_CLIENT.get(redisKey) != None):
        continue
      if filters and (zooplaFlat['Tenure'] not in filters
                      or zooplaFlat['PropertyType'] not in filters):
        continue
      sendFlat(district, zooplaFlat, chatId)
      REDIS_CLIENT.set(redisKey, 1)
      zooplaNew += 1
    print('[{}] zoopla, {}, new: {}/{}'.format(chatId, district, zooplaNew,
                                               len(zooplaFlats)))

  if not_found:
    print('[ERROR] No districts for rightmove: {}'.format(','.join(not_found)))


date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
print('[START]', date)

chats = getChats()
print('[CHATS]', chats)
for chat_id in chats:
  params = getChatParams(chat_id)
  try:
    runSearch(chat_id, params)
  except Exception as e:
    print(str(e))
    logStatus('[ERROR] {}, {}'.format(chat_id, str(e)))

print('[END]')
