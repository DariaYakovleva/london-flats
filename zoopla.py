
def getZooplaFlats(flatType, district, minBeds, maxPrice, minPrice=0, additional_params={}):
  ZOOPLA = 'https://www.zoopla.co.uk'
  urlDistrict = 'london/' + district if district in ['kensington', 'paddington'] else district
  query = '/{}/property/{}?beds_min={}&price_frequency=per_month&price_max={}&price_min={}&results_sort=newest_listings&q={}&search_source=to-rent&added=24_hours&include_shared_accommodation=false'
  url = ZOOPLA + query.format(flatType, urlDistrict, minBeds, maxPrice, minPrice, district)
  # print(url)
  r = requests.get(url)
  soup = BeautifulSoup(r.text, 'html.parser')

  flats = []
  for res in soup.find_all('div'):
    if res.get('data-testid', '').startswith('search-result_listing') or res.get('data-testid', '').startswith('regular-listings'):
      for res2 in res.find_all('div'):
        if res2.get('data-testid', '').startswith('extended-results-banner') \
          or 'No more exact results' in res2.text or 'No exact results found' in res2.text:
          break
        for link in res2.find_all('a'):
          flatLink = link.get('href')
          if 'search_identifier' in flatLink:
            flatLink = ZOOPLA + flatLink[0:flatLink.find('?') - 1]
            flats.append(flatLink)

  return list(set(flats))


def parseZooplaFlat(url):
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

  for tag in soup.find_all('p'):
    if (tag.get('data-testid', '') == 'price'):
      price = tag.string
    if (tag.get('data-testid', '') == 'availability'):
      availability = tag.string
  for tag in soup.find_all('address'):
    if (tag.get('data-testid', '') == 'address-label'):
      address = tag.string
  for tag in soup.find_all('div'):
    if (tag.get('data-testid', '').find('floorplan') != -1):
      floorPlanLink = tag.find('img').get('src')
    if tag.text in ['Freehold', 'Leasehold', 'Share of freehold']:
      tenure = tag.string.lower()
  for tag in soup.find_all('img'):
    if (tag.get('alt', '').find('Property photo') != -1):
      photo = tag.get('src')

  postcode = address.replace(',', '').split(' ')[-1]
  stats = 'https://crystalroof.co.uk/postcodes/{}'.format(postcode)

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
