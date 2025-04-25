from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import pandas as pd
import streamlit as st


class ScraperBot:
    
    def __init__(self):
       
        print("login")
        self.k=0
        edge_options = Options()  # Use EdgeOptions instead of ChromeOptions
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.59'
        
        edge_options.add_argument(f'user-agent={user_agent}')
        #edge_options.add_argument("--headless=new")
        
        self.bot = webdriver.Edge( options=edge_options)  # Specify the path to msedgedriver

    def getLinks(self):
        bot=self.bot
        
        print("login started")
        
        bot.get('https://www.wonder.legal/in/')
        links={}
        page_source = bot.page_source
        soup = BeautifulSoup(page_source,'html.parser')
        a=soup.find_all('div',{'class':'col col50'})
        for b in a:
            c=b.find_all('a')
            for d in c:
                links[d.text]=d['href']
        
        return links
    
    def getData(self,links):
        bot=self.bot
        data={}
        
        for k,v in links.items():
            bot.get(v)
            soup = BeautifulSoup(bot.page_source,'html.parser')
            dat=soup.find('div',{'id':'description'}).text
            data[k]=dat
        return data
    
    def close(self):
        print("closed")
        self.bot.quit()



st.title("Wonder.Legal Scraper")

if st.button("Start Scraping"):
    with st.spinner("Scraping in progress..."):
        bot = ScraperBot()
        links = bot.getLinks()
        st.success(f"Found {len(links)} links.")
        
        data = bot.getData(links)
        bot.close()
        df = pd.DataFrame(list(data.items()), columns=['Title', 'Description'])
        st.write(df)
        df.to_excel('wonder_legal_data.xlsx', index=False)
        st.success("Scraping complete! Data saved to `wonder_legal_data.xlsx`.")