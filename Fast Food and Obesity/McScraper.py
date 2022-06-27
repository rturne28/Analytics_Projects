import json
import pandas as pd
import numpy as np
import urllib.request, urllib.parse, urllib.error
from requests import get
import sys
import ssl
import fastfooddata
from time import sleep
import re

fast_food = sys.argv[-1]
if fast_food not in ['mcdonalds', 'tacobell', 'dominos', 'sonic', 'arbys', 'wendys']:
    sys.exit('Input must be one of these: mcdonalds, tacobell, dominos, sonic, arbys, wendys')

class API:
    def __init__(self, restaurant_name):
        self.restaurant = 0
        match restaurant_name:
            case 'mcdonalds':
                self.restaurant = fastfooddata.MickyD(restaurant_name) #creates instance of MickyD
            case 'tacobell':
                self.restaurant = fastfooddata.TacoHell(restaurant_name)
            case 'dominos':
                self.restaurant = fastfooddata.Inceptionos(restaurant_name)
            case 'sonic':
                self.restaurant = fastfooddata.Hedgehog(restaurant_name)
            case 'arbys':
                self.restaurant = fastfooddata.TheMeats(restaurant_name)
            case 'wendys':
                self.restaurant = fastfooddata.WenDeez(restaurant_name)

    def interact(self, baseurl):

        # ctx = ssl.create_default_context()
        # ctx.check_hostname = False
        # ctx.verify_mode = ssl.CERT_NONE
        complete_url = baseurl + urllib.parse.urlencode(self.restaurant.params)

        req = get(complete_url, headers=self.restaurant.header)#, verify=False)
        sitestr = req.text
        if self.restaurant.name == 'wendys':
            pre = re.search('^.*?{', sitestr)
            sitestr = sitestr.strip(pre[0].strip(pre[0][-1])).strip(')')
        js = json.loads(sitestr)
        return js


# Cleaning: only want TN, drop the dubplicate lat+long
zip_codes_df = pd.read_csv('./zip_code_database.csv')
rawTN_zc = zip_codes_df.loc[(zip_codes_df['state']=='TN')] # clean for just TN
rawTN_zc = rawTN_zc.loc[(rawTN_zc['decommissioned']!=1)] # clean decommed zips
unique_latslongs = rawTN_zc.drop_duplicates(subset = ['latitude', 'longitude'])
# unique_latslongs.to_csv('clean_TN_zips.csv')

def loopReturnedLocations(ff_inst):
    for item in ff_inst.jsobj_base:
        ff_inst.fillAddressComponents(item)
        ff_inst.df_list.append([ff_inst.store_lat, ff_inst.store_long,\
                        ff_inst.street_address, ff_inst.city, ff_inst.state,\
                        ff_inst.zipcode])

def getFastFoodDF(clean_postal_df, restaurant_name):
    APIobj = API(restaurant_name)
    ff_obj = APIobj.restaurant
    count = 0
    if ff_obj.name == 'mcdonalds' or ff_obj.name == 'tacobell' or\
       ff_obj.name == 'arbys':
        for (lat,long) in zip(clean_postal_df['latitude'], clean_postal_df['longitude']):
            ff_obj.params['latitude']  = lat
            ff_obj.params['longitude'] = long
            count += 1
            print('{} query {}'.format(ff_obj.name, count))
            jsonobject = APIobj.interact(ff_obj.baseurl)
            ff_obj.setJSObjBase(jsonobject)
            loopReturnedLocations(ff_obj)
    else:
        for zipcode in clean_postal_df['zip']:
            if ff_obj.name == 'chickfila':
                ff_obj.params['q'] = zipcode
            elif ff_obj.name == 'dominos':
                ff_obj.params['c'] = zipcode
            elif ff_obj.name == 'sonic':
                ff_obj.params['search'] = zipcode
            elif ff_obj.name == 'wendys':
                ff_obj.params['address'] = zipcode
            count += 1
            print('{} query {}'.format(ff_obj.name, count))
            sleep(2)
            jsonobject = APIobj.interact(ff_obj.baseurl)
            ff_obj.setJSObjBase(jsonobject)
            loopReturnedLocations(ff_obj)

    df = pd.DataFrame(ff_obj.df_list, columns=['Latitude', 'Longitude', 'Main Address',\
                                           'City', 'State', 'Zip Code'])
    # This requires another dropping of duplicates, as the same store may be
    #   returned from multiple searches
    df = df.drop_duplicates(subset = ['Latitude', 'Longitude'])
    # As this algorithm works by finding the nearest MDs to each GPS location,
    #   some that are returned might be in different States
    df = df.loc[(df['State']=='TN')]
    return df

def getCountiesDataFrame(df):
    params = dict()
    params['censusYear'] = 2020
    params['showall'] = 'false'
    params['format'] = 'json'
    county_url = 'https://geo.fcc.gov/api/census/block/find?'
    c_list = []
    cnt = 0
    for (lat,long) in zip(df['Latitude'], df['Longitude']):
        params['latitude']  = lat #35.8681377
        params['longitude'] = long #-84.09 #-84.0907246
        cnt+=1
        print('county query #', cnt)
        complete_url = county_url + urllib.parse.urlencode(params)
        req = get(complete_url)
        json_obj = json.loads(req.text)
        county = json_obj['County']['name']
        fips = json_obj['County']['FIPS']
        c_list.append([lat, long, county, fips])
    counties_df = pd.DataFrame(c_list, columns=['Latitude', 'Longitude', 'County', 'FIPS'])
    return counties_df

df = getFastFoodDF(unique_latslongs, fast_food)
# # print(df)
df.to_csv('{}.csv'.format(fast_food))
# df = pd.read_csv('./mcdonalds.csv')
countiesdf = getCountiesDataFrame(df)
countiesdf.to_csv('{}_counties.csv'.format(fast_food))
master_df = df.merge(countiesdf, on=['Latitude', 'Longitude'], indicator=True)
master_df.to_csv('{}_master.csv'.format(fast_food))
