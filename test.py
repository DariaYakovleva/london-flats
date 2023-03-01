from zoopla import getZooplaFlats
from rightmove import parseRightMoveFlat
from telegramBot import sendFlat
import requests
from env import REDIS_CLIENT, Params
from utils import getParamKey, getChatParams, addChat, calculateHash
from env import BOT_API

# chatId = -841210526
# url = 'https://www.zoopla.co.uk/to-rent/details/62812847'
# flat = parseZooplaFlat(url)
# sendFlat('fitzrovia', flat, chatId)

chatId = -848522648
url = 'https://www.rightmove.co.uk/properties/132123812'
flat = parseRightMoveFlat(url)
print(flat)
print(calculateHash(flat))
# sendFlat('covent-garden', flat, chatId)

# params = {'chat_id': -1001897744938, 'text': 'test'}
# res = requests.post(BOT_API + 'sendMessage', params)
# print(res, res.text)

# chat_id = -1001601617480
# REDIS_CLIENT.set(getParamKey(chat_id, Params.FLAT_TYPE), 'to-rent')
# REDIS_CLIENT.set(getParamKey(chat_id, Params.MINBEDS), 1)
# REDIS_CLIENT.set(getParamKey(chat_id, Params.MINPRICE), 0)
# REDIS_CLIENT.set(getParamKey(chat_id, Params.MAXPRICE), 2600)
# REDIS_CLIENT.set(
#   getParamKey(chat_id, Params.DISTRICTS),
#   'islington,angel,kensington,chelsea,notting-hill,wapping,mayfair,soho,covent-garden,ec1v,old-street'
# )

# getChatParams(chat_id)
# addChat(-1001601617480)

# getChatParams(16182175)

zooplaFlats = getZooplaFlats('to-rent', 'notting-hill', 1, 2500, 2000)
for flat in zooplaFlats.values():
  print(flat)
  print(calculateHash(flat))