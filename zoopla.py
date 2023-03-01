from datetime import datetime, timedelta
import requests

# https://developer.zoopla.co.uk/apps/myapps


def getZooplaFlats(flatType,
                   district,
                   minBeds,
                   maxPrice,
                   minPrice=0,
                   additional_params={}):
  urlDistrict = 'london/' + district if district in [
    'kensington', 'paddington'
  ] else district
  url = "https://zoopla.p.rapidapi.com/properties/list"
  createdSince = datetime.now() - timedelta(days=1)

  params = {
    "area": urlDistrict,
    "category": "residential",
    "created_since": createdSince.strftime("%Y-%m-%d %H:%M:%S"),
    "listing_status": flatType.split('-')[1],
    "minimum_beds": minBeds,
    "maximum_price": maxPrice,
    "minimum_price": minPrice,
    "include_retirement_homes": "no",
    "include_shared_accommodation": "no",
    "include_shared_ownership": "no",
    "order_by": "age",
    "ordering": "descending",
    "page_number": "1",
    "page_size": "40"
  }

  headers = {
    "X-RapidAPI-Key": "fed0b22f70msh5982570f82fb94cp1f1afejsn29b67d7e8a01",
    "X-RapidAPI-Host": "zoopla.p.rapidapi.com"
  }

  response = requests.request("GET", url, headers=headers,
                              params=params).json()

  flats = {}
  # print(len(response['listing']))
  for listing in response['listing']:
    url = listing['details_url'].split('?')[0]
    title = listing['title']
    price = '£' + listing[
      'price'] if flatType == 'for-sale' else '£{} pcm'.format(
        listing['rental_prices']['per_month'])
    address = listing.get('displayable_address', '')
    availability = listing.get('available_from_display', '')
    floorPlanLink = listing['floor_plan'][0] if 'floor_plan' in listing else ''
    photo = listing['image_url']
    tenure = ''
    propertyType = 'terraced' if title.find('terraced') != -1 else ''
    flats[url] = {
      'Title': title,
      'Price': price,
      'Address': address,
      'Availability': availability,
      'Link': url,
      'Photo': photo,
      'FloorPlanLink': floorPlanLink,
      'PropertyType': propertyType,
      'Tenure': tenure,
    }
    # print(flats[url])

  return flats
