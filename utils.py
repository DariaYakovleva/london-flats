from env import REDIS_CLIENT, Params
import re

CHATS_KEY = 'chats'


def getChats():
  chats = REDIS_CLIENT.get(CHATS_KEY).decode("utf-8")
  return list(map(int, chats.split(',')))


def getParamKey(chat_id, param):
  return '{}_{}'.format(chat_id, param.name)


def getChatParams(chat_id):
  params = {}
  for param in Params:
    value = REDIS_CLIENT.get(getParamKey(chat_id, param))
    if value != None:
      params[param] = value.decode("utf-8")
  return params


def addChat(chat_id):
  chats = REDIS_CLIENT.get(CHATS_KEY).decode("utf-8")
  chats = set(chats.split(','))
  chats.add(str(chat_id))
  REDIS_CLIENT.set(CHATS_KEY, ','.join(list(chats)))


def deleteChat(chat_id):
  chats = REDIS_CLIENT.get(CHATS_KEY).decode("utf-8")
  chats = set(chats.split(','))
  if str(chat_id) in chats:
    chats.remove(str(chat_id))
    REDIS_CLIENT.set(CHATS_KEY, ','.join(list(chats)))


def calculateHash(flat):
  hash = ''.join(map(str, re.findall(r'\d+', flat['Price'])))
  hash += ''.join(re.split(r' |,', flat['Address'].lower()))
  return hash
