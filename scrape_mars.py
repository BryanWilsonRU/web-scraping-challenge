import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup

def init_browser(): 
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    return Browser("chrome", **executable_path, headless=False)

# Create dictionary for mars info
mars_info = {}

def scrape_mars_news():
    try:
        browser = init_browser()
        url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"

        browser.visit(url)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')

        news_title = soup.find



        # Need to extract the following: content_title AND article_teaser_body
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')

        news_titles = soup.find_all('div', class_='content_title')
        news_title = news_titles[1].text.strip()

        news_p = soup.find('div', class_='article_teaser_body')



        # Append dictionary entry from Mars News Source
        mars_info['news_title'] = news_title
        mars_info['news_paragraph'] = news_p

        return mars_info

    finally:

        browser.quit()


def scrape_mars_image():
    try:

        # Initialize browser 
        browser = init_browser()

        # MARS DATA SCRAPE- JPL WEBSITE FEATURED IMAGE

        jpl_image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
        featured_image_url_start = 'https://jpl.nasa.gov'
        browser.visit(jpl_image_url)



        jpl_image = browser.html
        soup = BeautifulSoup(jpl_image, 'html.parser')



        # Need to extract the following: carousel item- data-fancybox-href
        home_images = soup.find('article', class_='carousel_item')
        footer = home_images.find('footer')
        link_url = footer.find('a')["data-fancybox-href"]
        featured_image_url = featured_image_url_start + link_url
        featured_image_url

        # Dictionary entry from FEATURED IMAGE
        mars_info['featured_image_url'] = featured_image_url 
            
        return mars_info
        
    finally:

        browser.quit()

# Scrape Mars Facts
def scrape_mars_facts():
    try:
        browser = init_browser()

        # MARS DATA SCRAPE- TABLE FROM SPACE-FACTS.COM

        sf_url = "https://space-facts.com/mars/"
        browser.visit(sf_url)

        tables = pd.read_html(sf_url)
        tables

        df = tables[0]
        df.columns = ['Description', 'Value']
        df.head()

        df = df.iloc[1:]
        df.set_index('Description', inplace=True)
        df.head()

        marsTable = df.to_html()

        mars_info['mars_facts'] = marsTable

        return mars_info
    finally:
        browser.quit()

def scrape_mars_hemispheres():
    try: 

        # Initialize browser 
        browser = init_browser()

        hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(hemispheres_url)



        hemisphere_images = browser.html
        soup = BeautifulSoup(hemisphere_images, 'html.parser')



        # Create list for image URLs
        image_urls = []
        image_url_start = 'https://astrogeology.usgs.gov'

        # Retreive all items that contain Mars Hemispheres data
        items = soup.find_all('div', class_='item')

        for i in items: 
            title = i.find('h3').text
            image_url_end = i.find('a', class_='itemLink product-item')['href']
            browser.visit(image_url_start + image_url_end)
            image_html = browser.html
            soup = BeautifulSoup(image_html, 'html.parser')
            image_url = image_url_start + soup.find('img', class_='wide-image')['src']
            image_urls.append({"title" : title, "image_url" : image_url})

        mars_info['hemisphere_image_urls'] = image_urls
            

        # Display image_urls
        image_urls
        return mars_info

    finally:
         browser.quit()
