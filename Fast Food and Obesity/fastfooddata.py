from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET

class MickyD:
    def __init__(self, restaurant_name):
        self.name = restaurant_name
        self.params = dict()
        self.baseurl = 'https://mcdonalds.com/googleappsv2/geolocation?'
        self.header = {}
        self.params['radius']     = 9
        self.params['maxResults'] = 30
        self.params['country']    = 'us'
        self.params['language']   = 'en-us'
        self.params['latitude']   = 0 # placeholder
        self.params['longitude']  = 0 # placeholder
        self.jsobj_base     = ''
        self.store_lat      = ''
        self.store_long     = ''
        self.street_address = ''
        self.city           = ''
        self.state          = ''
        self.zipcode        = ''
        self.df_list        = []

    def setJSObjBase(self, json_obj):
        self.jsobj_base = json_obj['features']

    def fillAddressComponents(self, item):
        self.store_lat      = item['geometry']['coordinates'][1]
        self.store_long     = item['geometry']['coordinates'][0]
        self.street_address = item['properties']['addressLine1']
        self.city           = item['properties']['addressLine3']
        self.state          = item['properties']['subDivision']
        self.zipcode        = item['properties']['postcode'][0:5]

# '''
# can flesh this out later if need be
class SpicyDelux:
    'this is html!!!!!!'
    def __init__(self, restaurant_name):
        self.name = restaurant_name
        self.params = dict()
        self.baseurl = 'https://locator.chick-fil-a.com.yext-cdn.com/search?'
        self.header = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}
        self.params['per'] = 10
        self.params['q'] = 0 # placeholder
        self.jsobj_base     = ''
        self.store_lat      = ''
        self.store_long     = ''
        self.street_address = ''
        self.city           = ''
        self.state          = ''
        self.zipcode        = ''
        self.df_list        = []

    def setJSObjBase(self, json_obj):
        self.jsobj_base = json_obj['response']['entities']

    def fillAddressComponents(self, item):
        self.store_lat =      item['profile']['displayCoordinate']['lat']
        self.store_lat =      item['profile']['displayCoordinate']['long']
        self.street_address = item['profile']['address']['line1']
        self.city =           item['profile']['address']['city']
        self.state =          item['profile']['address']['region']
        self.zipcode =        item['profile']['address']['postalCode']


class TacoHell:
    def __init__(self, restaurant_name):
        self.name = restaurant_name
        self.params = dict()
        self.baseurl = 'https://www.tacobell.com/tacobellwebservices/v2/tacobell/stores?'
        self.header = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}
        # self.params['_'] = 1655317011830
        self.params['latitude']   = 0 # placeholder
        self.params['longitude']  = 0 # placeholder
        self.jsobj_base     = ''
        self.store_lat      = ''
        self.store_long     = ''
        self.street_address = ''
        self.city           = ''
        self.state          = ''
        self.zipcode        = ''
        self.df_list        = []

    def setJSObjBase(self, json_obj):
        self.jsobj_base = json_obj['nearByStores']

    def fillAddressComponents(self, item):
        self.store_lat      = item['geoPoint']['latitude']
        self.store_long     = item['geoPoint']['longitude']
        self.street_address = item['address']['line1']
        self.city           = item['address']['town']
        self.state          = item['address']['region']['isocode'][3:5]
        self.zipcode        = item['address']['postalCode']

class Inceptionos:
    def __init__(self, restaurant_name):
        self.name = restaurant_name
        self.params = dict()
        self.baseurl = 'https://order.dominos.com/power/store-locator?'
        self.header = {}
        self.params['type'] = 'Carryout'
        self.params['c'] = 0 # placeholder
        self.jsobj_base     = ''
        self.store_lat      = ''
        self.store_long     = ''
        self.street_address = ''
        self.city           = ''
        self.state          = ''
        self.zipcode        = ''
        self.df_list        = []

    def setJSObjBase(self, json_obj):
        self.jsobj_base = json_obj['Stores']

    def fillAddressComponents(self, item):
        self.store_lat      = item['StoreCoordinates']['StoreLatitude']
        self.store_long     = item['StoreCoordinates']['StoreLongitude']
        full_address   = item['AddressDescription'].split('\n')
        full_address = [i for i in full_address if i] #clean empty strings
        self.street_address = full_address[0]
        self.city           = full_address[1].split(',')[0]
        self.state          = full_address[1].split(',')[1].split()[0]
        zipc                = full_address[1].split(',')[1].split()[1]
        if len(zipc) > 5: # clean long zip codes
            self.zipcode = zipc[0:5]
        else:
            self.zipcode = zipc

class Hedgehog:
    def __init__(self, restaurant_name):
        self.name = restaurant_name
        self.params = dict()
        self.baseurl = 'https://maps.locations.sonicdrivein.com/api/getAsyncLocations?'
        self.header = {}
        self.params['template'] = 'search'
        self.params['level'] = 'search'
        self.params['search'] = 0 # placeholder
        self.jsobj_base     = ''
        self.store_lat      = ''
        self.store_long     = ''
        self.street_address = ''
        self.city           = ''
        self.state          = ''
        self.zipcode        = ''
        self.df_list        = []

    def setJSObjBase(self, json_obj):
        self.jsobj_base = json_obj['markers']

    def fillAddressComponents(self, item):
        self.store_lat      = item['lat']
        self.store_long     = item['lng']
        weird               = item['info']
        soup = BeautifulSoup(weird, 'html.parser')
        strg = soup.get_text()
        str_list = strg.split(',')
        finallist = []
        for j in range(2,7):
            if j == 3:
                continue
            almost = str_list[j].strip().split('\"')
            almost = [i for i in almost if i]
            finallist.append(almost[2])
        self.street_address = finallist[0]
        self.city           = finallist[1]
        self.state          = finallist[2]
        self.zipcode        = finallist[3]

class TheMeats:
    def __init__(self, restaurant_name):
        self.name = restaurant_name
        self.params = dict()
        self.baseurl = 'https://api.arbys.com/arb/web-exp-api/v1/location?'
        self.header = {}
        self.params['radius'] = 50
        self.params['limit'] = 10
        self.params['page'] = 0
        self.params['local'] = 'en-us'
        self.params['latitude']   = 0 # placeholder
        self.params['longitude']  = 0 # placeholder
        self.jsobj_base     = ''
        self.store_lat      = ''
        self.store_long     = ''
        self.street_address = ''
        self.city           = ''
        self.state          = ''
        self.zipcode        = ''
        self.df_list        = []

    def setJSObjBase(self, json_obj):
        self.jsobj_base = json_obj['locations']

    def fillAddressComponents(self, item):
        self.store_lat      = item['details']['latitude']
        self.store_long     = item['details']['longitude']
        self.street_address = item['contactDetails']['address']['line1']
        self.city           = item['contactDetails']['address']['city']
        self.state          = item['contactDetails']['address']['stateProvinceCode']
        self.zipcode        = item['contactDetails']['address']['postalCode']

class WenDeez:
    def __init__(self, restaurant_name):
        self.name = restaurant_name
        self.params = dict()
        self.baseurl = 'https://digitalservices.prod.ext-aws.wendys.com/LocationServices/rest/nearbyLocations?'
        self.header = {}
        self.params['lang'] = 'en'
        self.params['cntry'] = 'US'
        self.params['sourceCode'] = 'ORDER.WENDYS'
        self.params['version'] = '15.0.0'
        self.params['limit'] = 25
        self.params['radius']   = 20
        self.params['address']  = 0 # placeholder
        self.jsobj_base     = ''
        self.store_lat      = ''
        self.store_long     = ''
        self.street_address = ''
        self.city           = ''
        self.state          = ''
        self.zipcode        = ''
        self.df_list        = []

    def setJSObjBase(self, json_obj):
        # 'this is actually an XML object'
        # print(str_obj)
        # xml_obj = ET.fromstring(str_obj)
        # root = xml_obj.getroot()
        self.jsobj_base = json_obj['data']#root.findall('data')

    def fillAddressComponents(self, item):
        self.store_lat      = item['lat']#.find('lat').text
        self.store_long     = item['lng']#.find('lng').text
        self.street_address = item['address1']#.find('address1').text
        self.city           = item['city']#.find('city').text
        self.state          = item['state']#.find('state').text
        self.zipcode        = item['postal']#.find('postal').text
