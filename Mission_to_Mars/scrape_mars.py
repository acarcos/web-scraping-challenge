# MongoDB and Flask Application

# libraries
from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import time

# Converting the Jupyter Notebook into a function
# Each scraping section was separated from the main function
# which is scrape()

# == Initialize browser ==
def init_browser():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

# == Mars news ==
def mars_news():
    browser = init_browser()
    url_news = 'https://mars.nasa.gov/news/'
    browser.visit(url_news)
   
    # Time lapse to read the html
    time.sleep(2)

    html_news = browser.html
    # Parse HTML with Beautiful Soup
    soup_news = bs(html_news, 'html.parser') 
    
    # Retrieve elements like Mars news titles
    mars_news = soup_news.find_all('div', class_='list_text')
    # Iterate through each title
    news_title = []
    news_title_prg = []
    for title in mars_news:
        tag = title.find('a')
        header = tag.next
        prg = tag.next.next.text
        news_title.append(header)
        news_title_prg.append(prg) 

    # Quit browser
    browser.quit()

    news_red = {
        'news_title': news_title[0], 'news_prg': news_title_prg[0],
        'news_title2': news_title[1], 'news_prg2': news_title_prg[1]
    }
    
    return news_red

# == Mars Weather ==
def mars_weather():
    browser = init_browser()
    url_tw = 'https://twitter.com/marswxreport'
    browser.visit(url_tw)

    time.sleep(5)

    html_tw = browser.html
    soup_tw = bs(html_tw, "html.parser")
    tweets = soup_tw.find_all(class_="css-901oao r-jwli3a r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0")
    mars_weather = {}
    for i in range(len(tweets)):
        weather = tweets[i].text
        if weather[:7] == 'InSight':
            mars_weather['tweet'] = weather
            break
        else:
            continue

    browser.quit()
    
    return mars_weather

# == Mars feature image ==
def mars_img_crsty(): 
    browser = init_browser()
    url_jpl = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url_jpl)

    time.sleep(2)

    # Get HTML and parse it with BS
    html_jpl = browser.html
    soup_jpl = bs(html_jpl, "html.parser")

    # Inspect the link
    img_tag = soup_jpl.find('div', class_='img').find('img')

    browser.quit()

    # Get the latest image from Mars 
    img_source = img_tag['src']
    img_title = img_tag['title']

    # Save the link 
    feat_image = 'https://www.jpl.nasa.gov' + img_source
    feature_image_url = {'img_title': img_title, 'img_src': feat_image}

    return feature_image_url

# == Mars facts ==
def mars_facts():
    # No browser, Pandas read the html link
    url_table = 'https://space-facts.com/mars/'
    mars_table = pd.read_html(url_table)   
    mars_table_one = mars_table[0]
    mars_table_one.columns = ['Parameter', 'Value']
    mars_table_one.to_html('mars_facts/table_test.html', index=False, justify='center')

# == Mars hemispheres ==
def mars_hmp_imgs():
    browser = init_browser()
    url_hmp = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url_hmp)
    time.sleep(1)
    html_hmp = browser.html
    soup_hmp = bs(html_hmp, "html.parser")
    img_hmp = soup_hmp.find_all('a', class_='itemLink product-item')
    # Links found manually
    url_img = 'https://astropedia.astrogeology.usgs.gov/'
    img_src_cer = url_img + 'download/Mars/Viking/cerberus_enhanced.tif/full.jpg'
    img_src_sch = url_img + 'download/Mars/Viking/schiaparelli_enhanced.tif/full.jpg'
    img_src_syr = url_img + 'download/Mars/Viking/syrtis_major_enhanced.tif/full.jpg'
    img_src_val = url_img + 'download/Mars/Viking/valles_marineris_enhanced.tif/full.jpg'
    # Save title and image link
    imgs_hmp = {
        "title_hmp1": img_hmp[1].find('h3').text, "src_hmp1": img_src_cer,
        "title_hmp2": img_hmp[3].find('h3').text, "src_hmp2": img_src_sch,
        "title_hmp3": img_hmp[5].find('h3').text, "src_hmp3": img_src_syr,
        "title_hmp4": img_hmp[7].find('h3').text, "src_hmp4": img_src_val
    }
    
    browser.quit()
    
    return imgs_hmp

# == Gather all Mars information from websites ==
def scrape():
    # Call ALL functions
    # Dict to save data
    mars_data = {}
    dict_news = mars_news()
    mars_data.update(dict_news)
    dict_weather = mars_weather()
    mars_data.update(dict_weather)
    dict_img = mars_img_crsty()
    mars_data.update(dict_img)
    dict_hmps = mars_hmp_imgs()
    mars_data.update(dict_hmps)
    
    return mars_data

