def getRightMoveFlats(flatType, district, minBeds, maxPrice, minPrice=0):
  RIGHTMOVE = 'https://www.rightmove.co.uk'
  query = '/property-{}/find.html?locationIdentifier={}&minBedrooms={}&maxPrice={}&minPrice={}&propertyTypes=&maxDaysSinceAdded=1&includeLetAgreed=false&mustHave=&dontShow=houseShare%2Cretirement%2Cstudent'
  url = RIGHTMOVE + query.format(flatType, district, minBeds, maxPrice,
                                 minPrice)
  # print(url)
  r = requests.get(url)
  soup = BeautifulSoup(r.text, 'html.parser')

  flats = []
  for res in soup.find_all('div'):
    if (res.get('data-test', '').find('propertyCard') != -1):
      flatId = int(res.get('id').split('-')[1])
      if (flatId > 0):
        flatLink = RIGHTMOVE + '/properties/{}'.format(flatId)
        flats.append(flatLink)

  return list(set(flats))


import requests
from bs4 import BeautifulSoup


def parseRightMoveFlat(url):
  # https://www.crummy.com/software/BeautifulSoup/bs4/doc/
  r = requests.get(url)
  soup = BeautifulSoup(r.text, 'html.parser')

  title = soup.title.string
  price = 0
  address = ''
  availability = ''
  floorPlanLink = ''
  photo = ''
  tenure = ''
  propertyType = ''

  for tag in soup.find_all('span'):
    if tag.text.find('£') != -1 and len(tag.text) > 1:
      price = tag.string
    if (tag.text.find(' pcm') != -1):
      price = tag.string
  for tag in soup.find_all('h1'):
    if (tag.get('itemprop', '') == 'streetAddress'):
      address = tag.string
  for tag in soup.find_all('div'):
    if (tag.text.find('Let available date') != -1):
      availability = tag.text
  for tag in soup.find_all('img'):
    alt = tag.get('alt', '')
    if (alt.find('Floor Plan') != -1 or alt.find('FP') != -1
        or alt.find('Floorplan') != -1):
      floorPlanLink = tag.get('src')
    if (alt.find('Photo') != -1 or alt.find('(Main)') != -1
        or alt.find('Picture No. 01') != -1):
      photo = tag.get('src')
  for tag in soup.find_all('p'):
    if tag.text in ['Freehold', 'Leasehold', 'Share of Freehold']:
      tenure = tag.string.lower()

  # postcode = address.replace(',', '').split(' ')[-1]
  # stats = 'https://crystalroof.co.uk/postcodes/{}'.format(postcode)

  # TODO fix me
  if title.find('terraced') != -1:
    propertyType = 'terraced'

  return {
    'Title': title,
    'Price': price,
    'Address': address,
    'Availability': availability,
    'Link': url,
    # 'Stats': stats,
    'Photo': photo,
    'FloorPlanLink': floorPlanLink,
    'PropertyType': propertyType,
    'Tenure': tenure,
  }