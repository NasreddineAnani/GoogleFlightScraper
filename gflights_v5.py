import asyncio
import pandas as pd
from pyppeteer import launch
import html5lib
import requests
import urllib
import urljoin
from bs4 import BeautifulSoup
import re
import time
import csv

t0 = time.time()

# MAKE SURE USING PYTHON3.6 

# ROUNDTRIP ONLY (!!!)

# WHERE DO YOU WANT TO GO ---- Departure/Arrival Flight Destination Parameters
dep_city = ('San Francisco')
arv_city = ('Denver') # IF YOU INPUT VALUE HERE, THEN DISREGARD NEXT 2 QUESTIONS

# DO YOU WANT TO CHOOSE ARRIVAL DESTINATION BASED BY THE TOP UNITED STATES AIRPORTS?
Answer = ('yes') # INPUT yes/no

# IF ABOVE ANSWER IS YES, CHOOSE YOUR STARTING/ENDING POINTS. FOR EXAMPLE, CHOOSE 0 IF YOU'D LIKE TO START WITH THE MOST POPULAR AIRPORT, 
# THEN SPECIFY ENDPOINT TO DETERMINE # OF AIRPORTS TO SEARCH {IF start_point = 0 and end_point = 20, then you'll look through the top 21 airports}
start_point = 0
end_point   = 50 # 55 = max range

# WHEN DO YOU WANT TO LEAVE -- Departure/Arrival Flight Date Parameters
dep_date = '7/11/2019'
arv_date = '7/14/2019'

# HOW MANY STOPS DO YOU WANT? - Put 0 for Non-Stop flight { 2 is the MAX }
num_stops = '2'

# FOR YOUR DEPARTING FLIGHT --- WHAT TIME DO YOU WANT TO LEAVE AT? ~ ** Must be at least a 3 hour window! ** ~
dep_leave_time_1 = '6:15AM'
dep_leave_time_2  = '8:45pM'

# DO YOU WANT TO DOWNLOAD YOUR DATA?
csv_file_download = 'Yes'

# IS THERE A DIFFERENT AIRPORT DISPLAYING IN RESULTS? CHANGE AIRPORT BY ADJUSTING LIST INDEX (0 is default). ONLY APPLICABLE IF CHOOSING CUSTOM DEPARTURE/ARRIVAL DESTINATIONS
dep_IATA_index = '0'
arv_IATA_index = '2'

#_______________________________________________________________#

masterlist       = []
roundtrip_urls   = []

#_______________________________________________________________#

dep_leave_time_1 = dep_leave_time_1.lower()
dep_leave_time_2 = dep_leave_time_2.lower()

time_array_list  = ['12','1','2','3','4','5','6','7','8','9','10','11']

#_______________________________________________________________#

def popular_airports(start_point,end_point, x):
    p = requests.get('https://www.faa.gov/airports/planning_capacity/passenger_allcargo_stats/passenger/')
    soup = BeautifulSoup(p.content, "html.parser")
    data = soup.find('table',{'id':'passengerboardingdata'})
    url = str(data.find_all('td')[1].find('a')).split('"><')[0].split('href="')[1]
    url = 'https://www.faa.gov' + url # form full url
    get_response = requests.get(url) # get info from webpage

    output = open('faa_file.xlsx', 'wb')
    output.write(get_response.content)
    output.close()

    x = []

    df    = pd.read_excel('faa_file.xlsx', sheet_name='ChangeinRevenuePassengerEnplan')
    df    = df['Locid'][start_point:end_point] # determines the range of airports you'll read in
    data  = df.to_string(header=False, index=False)

    for i in str(data).splitlines()[0:]:
        i = str(i.split(' ')[1])
        if len(i) == 3 and (getattr(i,'isupper')() == True): 
               x.append(i)
        else:
            continue
    return(x)

popular_airports = popular_airports(start_point,end_point,popular_airports)

#_______________________________________________________________#

# DEP_LEAVE_TIME

if dep_leave_time_1.find(':') >= 1 and dep_leave_time_1.find('am') >= 1:
    dep_leave_time_1 = "0" + str((time_array_list.index(dep_leave_time_1[0:dep_leave_time_1.find(':')])) + int(round(round(int(dep_leave_time_1[dep_leave_time_1.find(':')+1:dep_leave_time_1.find('am')]),0)/60))) + "00"
    if len(dep_leave_time_1) == 5:
        dep_leave_time_1 = dep_leave_time_1[1:5]
elif dep_leave_time_1.find(':') >= 1 and dep_leave_time_1.find('pm') >= 1:
    dep_leave_time_1 = str((time_array_list.index(dep_leave_time_1[0:dep_leave_time_1.find(':')])+12) + int(round(round(int(dep_leave_time_1[dep_leave_time_1.find(':')+1:dep_leave_time_1.find('pm')]),0)/60))) + "00"
elif dep_leave_time_1.find(':') == -1 and dep_leave_time_1.find('am') >= 1:
    dep_leave_time_1 = "0" + str(time_array_list.index(re.sub(" ","",dep_leave_time_1[0:dep_leave_time_1.find('am')]))) + "00"
    if len(dep_leave_time_1) == 5:
        dep_leave_time_1 = dep_leave_time_1[1:5]
elif dep_leave_time_1.find(':') == -1 and dep_leave_time_1.find('pm') >= 1:
    dep_leave_time_1 = str(time_array_list.index(re.sub("pm","",dep_leave_time_1))+12) + "00"

# DEP_LAND_TIME

if dep_leave_time_2.find(':') >= 1 and dep_leave_time_2.find('am') >= 1:
    dep_leave_time_2 = "0" + str((time_array_list.index(dep_leave_time_2[0:dep_leave_time_2.find(':')])) + int(round(round(int(dep_leave_time_2[dep_leave_time_2.find(':')+1:dep_leave_time_2.find('am')]),0)/60))) + "00"
    if len(dep_leave_time_2) == 5:
        dep_leave_time_2 = dep_leave_time_2[1:5]
elif dep_leave_time_2.find(':') >= 1 and dep_leave_time_2.find('pm') >= 1:
    dep_leave_time_2 = str((time_array_list.index(dep_leave_time_2[0:dep_leave_time_2.find(':')])+12) + int(round(round(int(dep_leave_time_2[dep_leave_time_2.find(':')+1:dep_leave_time_2.find('pm')]),0)/60))) + "00"
elif dep_leave_time_2.find(':') == -1 and dep_leave_time_2.find('am') >= 1:
    dep_leave_time_2 = "0" + str(time_array_list.index(re.sub(" ","",dep_leave_time_2[0:dep_leave_time_2.find('am')]))) + "00"
    if len(dep_leave_time_2) == 5:
        dep_leave_time_2 = dep_leave_time_2[1:5]
elif dep_leave_time_2.find(':') == -1 and dep_leave_time_2.find('pm') >= 1:
    dep_leave_time_2 = str(time_array_list.index(re.sub("pm","",dep_leave_time_2))+12) + "00"

else:
    print("ERROR")

if int(dep_leave_time_1) - int(dep_leave_time_2) >= 0:
    print("ERROR: please fix departure flight time parameter!")
    print
if int(dep_leave_time_2) - int(dep_leave_time_1) < 300:
    print("ERROR: please fix departure flight time parameter - window needs to be >= 3 hours!")
    print
#_______________________________________________________________#

dep_day = dep_date.split('/')[0]
dep_month = dep_date.split('/')[1]
dep_year = dep_date.split('/')[2]

arv_day = arv_date.split('/')[0]
arv_month = arv_date.split('/')[1]
arv_year = arv_date.split('/')[2]

if len(dep_day) == 1:
    dep_day = "0" + str(dep_day)
else:
    dep_day

if len(dep_month) == 1:
    dep_month = "0" + str(dep_month)
else:
    dep_month

if len(dep_year) == 2:
    dep_year = "20" + str(dep_year)
else:
    dep_year
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
if len(arv_day) == 1:
    arv_day = "0" + str(arv_day)
else:
    dep_day

if len(arv_month) == 1:
    arv_month = "0" + str(arv_month)
else:
    arv_month

if len(arv_year) == 2:
    arv_year = "20" + str(arv_year)
else:
    arv_year

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

rt_num_stops  = "s:" + str(num_stops) + "*" + str(num_stops) + ";"

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

def getIATA(x):
    parse   = urllib.parse.quote_plus(''.join([x,' IATA airport code']))
    url     = 'https://google.com/search?q=' + parse
    request = requests.get(url)
    soup    = BeautifulSoup(request.content, "html.parser")
    raw     = re.sub("'",'',re.sub(', ',' ',str(soup))).split(' ')
    y       = "{} IATA list: ".format(x) + str([i for i in raw if (getattr(i,'isupper')() == True and len(i) == 3) and i != 'USA' and i != 'FAA'])
    x       = [i for i in raw if (getattr(i,'isupper')() == True and len(i) == 3) and i != 'USA' and i != 'FAA']    
    print(y)
    return x 

dep_city = getIATA(dep_city)
arv_city = getIATA(arv_city)


####################################################################################################################################################################################################################

if len(dep_city) >= 2:
    dep_city = dep_city[int(dep_IATA_index)]
if len(dep_city) < 2:
    pass
else:
    pass

if len(arv_city) >= 2:
    arv_city = arv_city[int(arv_IATA_index)]
if len(arv_city) < 2:
    pass
else:
    pass

####################################################################################################################################################################################################################

if Answer.lower() == 'yes':
    masterlist = popular_airports
else:
    masterlist.append(arv_city)

####################################################################################################################################################################################################################
for arv_city_IATA in masterlist:
    try:

        roundtrip_url = "https://www.google.com/flights?hl=en#flt=" + "{}".format(dep_city) + "." + "{}".format(arv_city_IATA) + "." + "{}".format(dep_year) + "-" + "{}".format(dep_day) + "-" + "{}".format(dep_month) + "*"  + "{}".format(arv_city_IATA) + "." + "{}".format(dep_city) + "." + "{}".format(arv_year) + "-" + "{}".format(arv_day) + "-" + "{}".format(arv_month) + ";c:USD;e:1;" + "{}".format(rt_num_stops) + "dt:" + "{}".format(dep_leave_time_1) + "-" + "{}".format(dep_leave_time_2) + ";sd:1;t:f"
        roundtrip_urls.append(roundtrip_url)
    except:
        continue

####################################################################################################################################################################################################################

Airport_Dep_list = []
Airport_Arv_list = []
price_list       = []
url_list         = []
itinerary_list   = []
airline_list     = []


async def main(url):
    browser = await launch(
        headless=True,
        args=['--no-sandbox'],
        autoClose=True
    )
    page = await browser.newPage()
    await page.goto(url,
        {"waitUntil":"networkidle0"})

    data = await page.content()
    t1 = time.time()
    total = t1-t0
    try:
        try:
            cheapest_price     = int(re.sub('">',"",re.sub(",","",re.sub(" ","",str(data).split('flt-subhead1 gws-flights-results__price gws-flights-results__cheapest-price')[1]))).split('</div>')[0][1:len(re.sub('">',"",re.sub(",","",re.sub(" ","",str(data).split('flt-subhead1 gws-flights-results__price gws-flights-results__cheapest-price')[1]))).split('</div>')[0])])
        except:
            cheapest_price     = int(re.sub('">',"",re.sub(",","",re.sub(" ","",str(data).split('flt-subhead1 gws-flights-results__price gws-flights-results__cheapest-price')[1]))).split('</div>')[0][1:len(re.sub('">',"",re.sub(",","",re.sub(" ","",str(data).split('flt-subhead1 gws-flights-results__price gws-flights-results__cheapest-price')[1]))).split('</div>')[0])].split('$')[1])
        
        itineray_str_1         = str(data).split("$" + "{}".format(cheapest_price))[0]
        count                  = str(data).split("$" + "{}".format(cheapest_price))[0].count('>')  

        try:
            itineray_str_1     = str(itineray_str_1).split(' From')[0].split('>')[count]
        except:
            itineray_str_1     = str(itineray_str_1).split('.From')[0].split('>')[count]

        cheapest_price         = "$"+str(cheapest_price)
        itineray_str_2         = str(data).split(" round trip total.")[1] # Differs from single flight HTML
        itineray_str_2         = str(itineray_str_2).split('.<')[0]
        itinerary_str          = str(itineray_str_1 + "." + itineray_str_2)
        try:
            itinerary          = re.sub("From'.","",re.sub("From .","",itinerary_str))
            airline            = itinerary_str.split('by ')[1].split('.')[0]
        except:
            itinerary          = "None"
            airline            = "None"

        itinerary_str          = '\n'.join(re.sub(r'([A-Z])+([.]\s]*)',r'\1 ',re.sub("St. ","St ",re.sub("From'.","",re.sub("From .","",itinerary_str)))).split('.')) # example : John F Kennedy Airport becomes John F Kennedy Airport
        Status                 = "Success"

    except:
        try:
            try:
                itineray_str_1     = str(itineray_str_1).split(".From'")[0].split('Nonstop ')[1]
         #      itineray_str_2     = str(data).split("$" + str(cheapest_price))[0].split('.From')[1] # Differs from single flight HTML // for flights with stops
         #      itineray_str_2     = str(itineray_str_2).split('.<')[0]
                itinerary_str      = str(itineray_str_1)# + "." + itineray_str_2)
                try:
                    itinerary      = re.sub("From'.","",re.sub("From .","",itinerary_str))
                    airline        = itinerary_str.split('by ')[1].split('.')[0]
                except:
                    itinerary      = "None"
                    airline        = "None"

                itinerary_str      = '\n'.join(re.sub(r'([A-Z])+([.]\s]*)',r'\1 ',re.sub("St. ","St ",re.sub("From'.","",re.sub("From .","",itinerary_str)))).split('.')) # example : John F Kennedy Airport becomes John F Kennedy Airport
                Status             = "Success"


            except:
                if str(data).split('data-flt-ve="no_')[1][0:7] == 'results': ## Checking to see if there are no results --> if TRUE, then no flights available
                    Status         = "No Flight Available"
                    cheapest_price = "None"
                    itinerary_str  = "None"
                    itinerary      = "None"
                    airline        = "None"
                else:
                    Status         = "Code Error"
                    cheapest_price = "None"
                    itinerary_str  = "None"
                    itinerary      = "None"
                    airline        = "None"
        except:
            Status                 = "No Flight Available"
            cheapest_price         = "None"
            itinerary_str          = "None"
            itinerary              = "None"
            airline                = "None"

    Airport_Dep                    = url[41:44]
    Airport_Arv                    = url[45:48]

    Airport_Dep_list.append(Airport_Dep)
    Airport_Arv_list.append(Airport_Arv)
    price_list.append(cheapest_price)
    url_list.append(url)
    itinerary_list.append(itinerary)
    airline_list.append(airline)

    print(
             '\n'
            ,'Search Status: %s @ %ss' % (Status,round(total,2))
            ,'\n'
            ,'\n'
            ,'Price: %s' % cheapest_price
            ,'\n'
            ,'Itinerary: %s' % itinerary_str.encode('ascii', 'ignore').decode('ascii')
            ,'\n'
            ,url
            ,'\n'
            ,sep=''
            )   
    await browser.close()

for url in roundtrip_urls:
    df = asyncio.get_event_loop().run_until_complete(main(url))
    df

if csv_file_download.lower() == 'no':
    pass

else:
    if Answer.lower() == 'yes':
        filename = 'gflights_' + dep_city + '-' +'faa-list-' + dep_day + '-' + dep_month + 'to' + arv_day + '-' + arv_month + '.csv'
    else:
        filename = 'gflights_' + dep_city + '-' + arv_city + '-' + dep_day + '-' + dep_month + 'to' + arv_day + '-' + arv_month + '.csv'
    
    csv_file = open(filename, 'w')
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['Departing Airport', 'Arriving Airport', 'Price', 'Airline', 'Departure Date','Return Date', 'Itinerary', 'URL'])
    for i in range(0,len(url_list)):
        try:
            csv_writer.writerow([Airport_Dep_list[i], Airport_Arv_list[i], price_list[i], airline_list[i], dep_date, arv_date, itinerary_list[i], url_list[i]])
        except:
            csv_writer.writerow([Airport_Dep_list[i], Airport_Arv_list[i], "None", "None", "None", "None", "None", url_list[i]])
    csv_file.close()

t1 = time.time()
total = t1-t0
print('Finished @ %ss' % (round(total,2)))





