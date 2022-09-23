from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt

 


def scrape():
    executable_path = {'executable_path' : ChromeDriverManager().install()}
    browser = Browser('chrome',**executable_path, headless = False)
    final_data = {}
    output = marsNews(browser)
    final_data['mars_news'] = output[0]
    final_data['mars_paragraph'] = output[1]
    final_data['mars_image']=marsImage(browser)
    final_data['mars_facts']=marsFacts(browser)
    final_data['mars_hemisphere'] = marsHem(browser)
    browser.quit()
    return final_data

def marsNews(browser):
    news_url = 'https://mars.nasa.gov/news/'
    browser.visit(news_url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    article = soup.find("div", class_='list_text')
    news_title = article.find('div', class_='content_title').text
    news_p = article.find("div", class_="article_teaser_body").text
    output = [news_title, news_p]
    return output

def marsImage(browser):
    image_url = "https://spaceimages-mars.com"
    browser.visit(image_url)
    html = browser.html
    soup = BeautifulSoup(html,"html.parser")
    image = soup.find('img', class_='headerimage')['src']
    featured_image_url = 'https://www.spaceimages-mars.com/' + image
    return featured_image_url

def marsFacts(browser):
    facts_url = 'https://space-facts.com/mars/'
    browser.visit(facts_url)
    mars_data = pd.read_html(facts_url)
    mars_data = pd.DataFrame(mars_data[0])
    mars_data.columns = ["Description", 'Value']
    mars_data = mars_data.set_index("Description")
    mars_facts = mars_data.to_html(index = True, header = True)
    return mars_facts

def marsHem(browser):
    import time 
    hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemispheres_url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    hemispheres = soup.find_all('div', class_='item')
    hemisphere_image_url = []
    
    main_url = 'https://astrogeology.usgs.gov/'
    for x in hemispheres:
        hemisphere = {}
        title = x.find('h3').text
        link_ref = x.find('a',class_='itemLink product-item')['href']
        browser.visit(main_url + link_ref)
        image_html = browser.html
        image_soup = BeautifulSoup(image_html, 'html.parser')
        download = image_soup.find('div', class_='downloads')
        img_url = download.find('a')['href']
        hemisphere['img_url'] = img_url
        hemisphere['title'] = title
        hemisphere_image_url.append(hemisphere)
        browser.back()
    return hemisphere_image_url

scrape()