import redis
from enum import Enum

# https://console.aiven.io/project/dariyakovleva-6247/services/londonflats/overview
REDIS_URL = 'rediss://default:AVNS_QpNIzM-hvrBllJ6cIll@londonflats-dariyakovleva-6247.aivencloud.com:11674'
REDIS_CLIENT = redis.from_url(REDIS_URL)
TOKEN = '5618237141:AAHnMxz1dmA8tzfmz_b3HsqhpmPKNT_cqTI'
CHATS_KEY = 'chats'
ADMIN_CHAT_ID = 68741648

# chatId: https://api.telegram.org/bot5618237141:AAHnMxz1dmA8tzfmz_b3HsqhpmPKNT_cqTI/getUpdates
# https://core.telegram.org/bots/api#inputmediaphoto
TOKEN = '5618237141:AAHnMxz1dmA8tzfmz_b3HsqhpmPKNT_cqTI'
BOT_API = 'https://api.telegram.org/bot{}/'.format(TOKEN)

ADMIN_CHAT_ID = 68741648


class Params(Enum):
  FLAT_TYPE = 1
  MINBEDS = 2
  MAXBEDS = 3
  MINPRICE = 4
  MAXPRICE = 5
  DISTRICTS = 6
  FILTERS = 7


DISTRICTS_MAP = {
  'islington': 'REGION%5E87515',
  'angel': 'STATION%5E245',
  'kensington': 'REGION%5E87517',
  'chelsea': 'REGION%5E87498',
  'notting-hill': 'REGION%5E70331',
  'paddington': 'REGION%5E70403',
  'wapping': 'REGION%5E85209',
  'mayfair': 'REGION%5E87523',
  'soho': 'REGION%5E87529',
  'covent-garden': 'REGION%5E87501',
  'hampstead': 'REGION%5E87509',
  'paddington': 'REGION%5E70403',
  'belgravia': 'REGION%5E87493',
  'fitzrovia': 'REGION%5E93764',
  'marylebone': 'REGION%5E87522',
  'primrose-hill': 'REGION%5E87390',
  'sw11': 'OUTCODE%5E2497',
  'nw3': 'OUTCODE%5E1859',
  'e8': 'OUTCODE%5E762',
  'n1': 'OUTCODE%5E1666',
  'ec1v': 'OUTCODE%5E770',
  'battersea': 'STATION%5E18250',
  'old-street': 'STATION%5E6881',
  'london-bridge': 'STATION%5E5792',
  'hackney': 'REGION%5E87508',
  'cricklewood': 'REGION%5E70430',
  'camden': 'REGION%5E85261',
  'little-venice': 'REGION%5E70436',
  'kings-cross': 'REGION%5E87399',
  'w9': 'OUTCODE%5E2769',
  'whitechapel': 'REGION%5E85210',
  'bethnal-green': 'REGION%5E85224',
  'limehouse': 'REGION%5E85365',
  'wimbledon': 'REGION%5E87540',
  'wandsworth': 'STATION%5E9587',
  'dulwich': 'REGION%5E87503',
  'chiswick': 'REGION%5E85345',
  'southwark': 'STATION%5E8498',
  'shoreditch': 'STATION%5E10415',
  'bloomsbury': 'REGION%5E87494',
  'nw5': 'OUTCODE%5E1861',
  'kilburn': 'REGION%5E85233',
  'nw': 'REGION%5E93961',
  'herne-hill': 'REGION%5E85409',
  'richmond': 'STATION%5E7703',
  'fulham': 'REGION%5E87507',
  'north-sheen': 'REGION%5E85411',
  'haggerston': 'REGION%5E85390',
  'farringdon': 'STATION%5E3431',
  'isle-of-dogs': 'REGION%5E85364',
}
