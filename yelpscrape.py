# -*- coding: utf-8 -*-
import requests
from lxml import html
import json
import re
from bs4 import BeautifulSoup


    

def parse(website):
    # CONNECTING TO URL
    web_url = requests.get(website).text
    
    # PARSING HTML CODE USING BEAUTIFULSOUP
    soup = BeautifulSoup(web_url, 'lxml')
    
    # PARSING XML CODE
    parser = html.fromstring(web_url)
    
    # EXTRACTING RAW INFORMATION USING XPATH
    
    # Name
    names = parser.xpath("//*[@id=\"wrap\"]/div[4]/div/div[3]/div/div/div[2]/div[1]/div[1]/div/div/div[1]/h1/text()")
    # Speciality of Restaurant
    rtypes = parser.xpath("//*[@id=\"wrap\"]/div[4]/div/div[3]/div/div/div[2]/div[1]/div[1]/div/div/span[2]/span[1]/a/text()")
    # Address (2 xpaths are present)
    addr1 = parser.xpath("//*[@id=\"wrap\"]/div[4]/div/div[3]/div/div/div[2]/div[1]/section[3]/div[2]/div[1]/div/div/div/div[1]/address/p[1]/span/text()")
    addr2 = parser.xpath("//*[@id=\"wrap\"]/div[4]/div/div[3]/div/div/div[2]/div[1]/section[3]/div[2]/div[1]/div/div/div/div[1]/address/p[2]/span/text()")
    # Ratings by Customers
    ratings = parser.xpath("//*[@id=\"wrap\"]/div[4]/div/div[3]/div/div/div[2]/div[1]/div[1]/div/div/div[2]/div[1]/span/div/@aria-label")
    # Number of reviews
    reviews = parser.xpath("//*[@id=\"wrap\"]/div[4]/div/div[3]/div/div/div[2]/div[1]/div[1]/div/div/div[2]/div[2]/p/text()")
    # Website of Restaurant
    sites = parser.xpath("//*[@id=\"wrap\"]/div[4]/div/div[3]/div/div/div[2]/div[2]/div/div/section[1]/div/div[1]/div/div[2]/p[2]/a/text()")
    # Contact No.
    phones = parser.xpath("//*[@id=\"wrap\"]/div[4]/div/div[3]/div/div/div[2]/div[2]/div/div/section[1]/div/div[2]/div/div[2]/p[2]/text()")
    # Menu link
    menus = parser.xpath("//*[@id=\"wrap\"]/div[4]/div/div[3]/div/div/div[2]/div[2]/div/div/section[1]/div/div[4]/div/div[2]/p/a/@href")
    # Workin-Hours Table
    hour_table = soup.find('tbody',{'class':'lemon--tbody__373c0__2T6Pl'})
    
    
    # CLEANING OF RAW DATA
    
    # Converting name to string
    if names:
        name = names[0]
    else:
        name = "Not=Available"
    
    # Converting Speciality to string
    if rtypes:
        rtype = rtypes[0]
    else:
        # If list is empty
        rtype = "Not-Available"
    
    # Combining both the sub-addresses
    if (addr1 and addr2):
        addr = addr1[0] + ', ' + addr2[0]
    else:
        addr = "Not-Available"
    
    # Removing excess words from rating
    if not ratings:
        # If empty then
        rating = "Not-Available"
    else:
        # Raw data = 4 star rating
        # After processing , rating = 4
        rating = float(ratings[0].split(' ',1)[0])
        
    # Removing excess words from reviews
        if not reviews:
            # If empty then
            review = "Not-Available"
        else:
            # Raw data = 45 reviews
            # After processing , review = 45
            review = int(reviews[0].split(' ',1)[0]) 
            
    # Website if unavailable
        if not sites:
            site = "Not-Available"
        else:
            # Append "http://www." to the beginning of website
            part1 = "http://www."
            site = sites[0]
            site = part1 + site
            
    # Removing Brackets from phone numbers (using regex)
        if not phones:
            phone = "Not-Available"
        else:
            # Raw number = (212) 727-7900
            # stripped = 212 727-7900
            # phone = 212-727-7900
            stripped = re.sub(r'[\()]','',phones[0])
            phone = re.sub(r'\s','-',stripped)
    
    # Menu link if unavailable
        if not menus:
            menu = "Not-Available"
        else:
            menu = menus[0]
            
    # Extracting info from hour-table
    table_data = []
    if hour_table:
        table_rows = hour_table.find_all('tr')
        for table_row in table_rows:
            table_data.append(table_row.find('td').text.strip())
            
        # If two shifts are present on same day
        # then, insert 'and' between them
        
        i=0
        for day in table_data:
            match = re.search(r'm[0-9]',day)
            if match:
                shift1 = day[:match.start()+1]
                shift2 = day[match.start()+1:]
                day = shift1 + ' and ' + shift2
                table_data[i] = day
                
            i = i+1
        
    # CREATING WORKING HOURS FIELD
    if table_data:
        work_hour = {   'Monday':table_data[0],
                     'Tuesday':table_data[1],
                     'Wednesday':table_data[2],
                     'Thursday':table_data[3],
                     'Friday':table_data[4],
                     'Saturday':table_data[5],
                     'Sunday':table_data[6]}
    else:
        work_hour = "Not-Available"
    
    data={  'Name' : name , 
             'Speciality': rtype ,
             'Address': addr ,
             'Avg. Rating': rating , 
             'Total Reviews': review ,
             'Website': site ,
             'Contact No.': phone ,
             'Menu-Link': menu ,
             'Working-Hours': work_hour
                }
    return data

# These are the top 30 small business restaurants present in New York city
# according to yelp.com

websites={"https://www.yelp.com/biz/sall-restaurant-and-lounge-new-york-4" ,
          "https://www.yelp.com/biz/oak-tuscan-truffle-restaurant-new-york-3" , 
          "https://www.yelp.com/biz/superior-wonton-noodles-brooklyn", 
          "https://www.yelp.com/biz/lillo-cucina-italiana-brooklyn", 
          "https://www.yelp.com/biz/harts-restaurant-brooklyn-2", 
          "https://www.yelp.com/biz/heidis-house-by-the-side-of-the-road-new-york-2", 
          "https://www.yelp.com/biz/the-wild-son-new-york", 
          "https://www.yelp.com/biz/safari-restaurant-nyc-new-york", 
          "https://www.yelp.com/biz/bigoi-venezia-new-york", 
          "https://www.yelp.com/biz/piccante-brooklyn",
          "https://www.yelp.com/biz/thai-farm-kitchen-brooklyn?osq=small+restaurants",
          "https://www.yelp.com/biz/athena-mediterranean-cuisine-brooklyn-3?osq=small+restaurants",
          "https://www.yelp.com/biz/the-food-sermon-kitchen-brooklyn-2?osq=small+restaurants",
          "https://www.yelp.com/biz/lic-market-long-island-city?osq=small+restaurants",
          "https://www.yelp.com/biz/buena-vista-restaurant-and-bar-new-york?osq=small+restaurants",
          "https://www.yelp.com/biz/nostro-ristorante-brooklyn?osq=small+restaurants",
          "https://www.yelp.com/biz/le-french-diner-new-york?osq=small+restaurants",
          "https://www.yelp.com/biz/dek-sen-elmhurst-2?osq=small+restaurants",
          "https://www.yelp.com/biz/benito-one-new-york?osq=small+restaurants",
          "https://www.yelp.com/biz/provini-brooklyn?osq=small+restaurants",
          "https://www.yelp.com/biz/cotenna-new-york?osq=small+restaurants",
          "https://www.yelp.com/biz/da-franco-and-tony-ristorante-bronx?osq=small+restaurants",
          "https://www.yelp.com/biz/ortobello-restaurant-brooklyn?osq=small+restaurants",
          "https://www.yelp.com/biz/la-sir%C3%A8ne-soho-new-york?osq=small+restaurants",
          "https://www.yelp.com/biz/yes-chef-wine-bar-astoria?osq=small+restaurants",
          "https://www.yelp.com/biz/mokyo-new-york-2?osq=small+restaurants",
          "https://www.yelp.com/biz/hug-esan-elmhurst?osq=small+restaurants",
          "https://www.yelp.com/biz/le-succulent-brooklyn-2?osq=small+restaurants"
          "https://www.yelp.com/biz/suki-new-york-5?osq=small+restaurants",
          "https://www.yelp.com/biz/ajo-and-oregano-bronx?osq=small+restaurants",
          "https://www.yelp.com/biz/da-franco-and-tony-ristorante-bronx?osq=small+restaurants"
          }

# Data for writing into json file
BigData = []

# Traversing through every website
for website in websites:
    # Extracting data and cleaning
    data = parse(website)
    # Appending data in BigData list
    BigData.append(data)
    
# Writing to .json file 
with open('yelpdata2.json','w') as json_file:
    json.dump(BigData, json_file)
    
json_file.close()
    
    