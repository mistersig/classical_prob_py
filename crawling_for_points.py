import requests
from bs4 import BeautifulSoup
import pandas as pd
import re


def webpage(url):
page = requests.get(url)
page_content = BeautifulSoup(page.content, 'lxml')
return page_content


def html_telefone_parser(html):
telefone_num = [] #list
for digits in html:
for store_tel in digits.find_all("a",{"class":"phone_number"}):
telefone_num.append(store_tel.text)
return telefone_num

def html_storeid_parser(html):
sid = [] #list
for store in html:
for name in store.find_all("div", class_="store_header"):
sid.append(name.text)
return sid



def html_address_parser(html):
a = [] #list
for location in html:
for lac in location.find_all("div", {"class":"store_address info_icon map_pin"}):
for l in lac.find_all("p"):
a.append(l.text)
parsed = address_parser(a)
return parsed


def address_parser(a):
'''
Unique function for this crawler called in html_address_parser for efficiency
'''

##minor clean up for address_parser to work with slicing indicies
a.insert(a.index('5276 Monahans Ave.'),'5276 Monahans Ave. Suite J-200')
a.pop(a.index('5276 Monahans Ave.'))
a.pop(a.index('Suite J-200'))

address = a[::2]
city_st_zip = a[1::2]

city = []
st_zip=[]
for x in city_st_zip:
city.append(x.split(',')[0])
st_zip.append(x.split(',')[1])

state = []
zip_codes = []
for x in st_zip:
state.append(x.split(' ')[1])
zip_codes.append(x.split(' ')[2])

return address,city,state,zip_codes



def crawler_csv_output(acsz,sid,tel,ll,fname):
'''
acsz: address, city, state, zip
'''
new_csv = pd.DataFrame(
   {'store_id': sid,
   'telefone': tel,
   'address': acsz[0],
   'city':acsz[1],
   'state': acsz[2],
   'zipcode': acsz[3],
   'latitude':ll[0],
   'longitude':ll[1]
   
   })

# new_csv=new_csv.drop_duplicates(['store_id'], keep='first')
print(new_csv)


new_csv.to_csv(fname, sep=',', encoding='utf-8', index=False)
print('complete')




def latlon_parser(html):
'''
lat long
'''

regex = r".*?]"
matchObject = re.findall(regex, html)
lat = []
lng = []
for x in matchObject:
x = re.sub(r"\s+", ' ',x.replace('\n', ' ').replace('\r', '') )
# print(x)
for y in x.split(','):
# print(y[-10:])
if 'lat' in y:
# lat.append(y[-10:])
lat.append( re.sub(":|g", "", y[-10:]))
elif 'lng' in y:
lng.append( re.sub(":|g", "", y[-13:-1]))
else:
pass
return lat,lng



def main():
'''
Main function where the code will be run.
'''
website_url = "https://www.grimaldispizzeria.com/locations/"

# soup = BeautifulSoup(open('output.html'), 'html.parser') ##for testing
soup = webpage(website_url) #live

#
html_address = soup.find_all("div", {"class":"container locations_row"})
#lat/long
html_latlong = soup.find_all("script")[14].string

#Parser variables from functions
address_city_st_zip = html_address_parser(html_address)
store_id = html_storeid_parser(html_address)
store_phone = html_telefone_parser(html_address)
latlng = latlon_parser(html_latlong)

file_name= 'grimaldis.csv'
crawler_csv_output(address_city_st_zip,store_id,store_phone,latlng,file_name)









####### Start of the
if __name__ == '__main__':
main()














