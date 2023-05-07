import time
from bs4 import BeautifulSoup
#from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from splinter import Browser


#def init_browser():
   # executable_path = {'executable_path': ChromeDriverManager().install()}
    #return Browser('chrome', **executable_path, headless=False)
   # return browser

def scrape_info():
    
    browser = Browser('chrome')
    mars = {}
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    time.sleep(1)

    #HTML object
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    #collect the latest News Title and Paragraph Text
    news_title = soup.find_all("div", class_="content_title")[1].text
    news_p = soup.find("div", class_="article_teaser_body").text
    print(news_title)
    print(news_p)
    mars["news_title"]= news_title
    mars["news_p"]= news_p


    #-------------------------------------JPL Mars Space Images- Featured Image--------------------------------------------------#


    jpl_image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(jpl_image_url)

    

    main_url = "https://www.jpl.nasa.gov"
    jpl_image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(jpl_image_url)
    time.sleep(5)
    browser.find_by_id("full_image").click()
    time.sleep(5)
    browser.find_link_by_partial_text("more info").click()
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    featured_image_url = soup.find("figure", class_="lede").a.img["src"]
    featured_image_url = main_url + featured_image_url
    mars["featured_image"]= featured_image_url

    fact_url = "https://space-facts.com/mars/"
    table = pd.read_html(fact_url)
    table

    mars_df = table[0]
    mars_df.columns = ["description","values"]
    mars_df.set_index("description", inplace =True)
    mars_df

    mars_fact_html = mars_df.to_html()
    mars_fact_html  

    mars_fact_html.replace('\n', '')
    mars["facts"]= mars_fact_html
    print (mars_fact_html)

#-----------------------------------Mars Hemispheres------------------------------------------------------------------#
    hem_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hem_url)

    hem_image_url = []

    for i in range(4):
        hem ={}
        browser.find_by_css("a.product-item h3")[i].click()
        hem_html =  browser.html
        hem_soup = BeautifulSoup(hem_html, 'html.parser')
        
        try:
            title = hem_soup.find("h2", class_="title").text
            sample_element =hem_soup.find("a", text="Sample").get("href")
        
        except:
            title= None
            sample_element =None
        hem ={"title":title, 
            "img_url": sample_element
            }
        hem_image_url.append(hem)
        browser.back()

    hem_image_url


    mars["hem"] =hem_image_url
    mars

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars

if __name__ == "__main__":
    print(scrape_info())    