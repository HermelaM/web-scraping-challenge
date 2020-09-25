from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import datetime as dt
import time

#executable_path = {'executable_path':"C:\\Users\\Hermela\\Documents\\bootcamp\\web-scraping-challenge\\app\\chromedriver.exe"}
#browser = Browser("chrome", **executable_path, headless=False)

def mars_news(browser):
    executable_path = {'executable_path':"C:\\Users\\Hermela\\Documents\\bootcamp\\web-scraping-challenge\\app\\chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)
    mars = {}

    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    mars["news_title"] = soup.find("a", class_="content_title").get_text()
    mars["news_paragraph"] = soup.find('a', class_="article_teaser_body").get_text()

    return mars

def featured_image(browser):
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    #Find the click button and click
    full_image = browser.find_by_id("full_image")
    full_image.click()

    #Find more info button and click
    browser.is_element_present_by_text('more info', wait_time=1)
    more_info = browser.find_link_by_partial_text('more info')
    more_info.click()

    html = browser.html
    img_soup = BeautifulSoup(html, 'html.parser')

    img_url_rel = img_soup.select_one('figure.lede a img').get("src")
   
    try: 
        img_url = img_url_rel.get("src")
    except AttributeError:
        return None
    
    img_url_rel = f"https://www.jpl.nasa.gov{img_url_rel}"
    return img_url

# Mars Facts Web Scraper
def mars_facts():
    # Visit the Mars Facts Site Using Pandas to Read
    try:
        df = pd.read_html("https://space-facts.com/mars/")[0]
    except BaseException:
        return None
    df.columns=["Description", "Value"]
    df.set_index("Description", inplace=True)

    return df.to_html(classes="table table-striped")

# Mars Hemispheres
def hemisphere(browser):

    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    hemisphere_image_urls = []

    # List of all the hemispheres
    links = browser.find_by_css("a.product-item h3")

# loop through hemispheres 
    for item in range(len(links)):
        hemisphere = {}
        
        # Find Element on Each Loop to Avoid a Stale Element Exception
        browser.find_by_css("a.product-item h3")[item].click()
        
        # Find Sample Image Anchor Tag & Extract <href>
        sample_element = browser.find_link_by_text("Sample").first
        hemisphere["img_url"] = sample_element["href"]
        
        # Get hemisphere title
        hemisphere["title"] = browser.find_by_css("h2.title").text
        
        # Append hemisphere Object to List
        hemisphere_image_urls.append(hemisphere)
        
        # Navigate backwards
        browser.back()
    return hemisphere_image_urls

def scrape_hemisphere(html_text):
    hemisphere_soup = BeautifulSoup(html_text, "html.parser")
    try: 
        title_element = hemisphere_soup.find("h2", class_="title").get_text()
        sample_element = hemisphere_soup.find("a", text="Sample").get("href")
    except AttributeError:
        title_element = None
        sample_element = None 
    hemisphere = {
        "title": title_element,
        "img_url": sample_element
    }
    return hemisphere


def scrape_all():

    # Initiate headless driver for deployment
    browser = Browser("chrome", executable_path="chromedriver", headless=True)
    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store in dictionary.
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "hemispheres": hemispheres(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now()
    }
     # Stop webdriver and return data
    browser.quit()
    return data
   

if __name__ == "__main__":
    print(scrape_all())