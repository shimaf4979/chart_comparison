import scrapy
from scrapy_selenium import SeleniumRequest
from time import sleep
from selenium.webdriver.common.keys import Keys
from scrapy.selector import Selector
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class MelonChart100Spider(scrapy.Spider):
    
    name = 'melon_chart100'
    # allowed_domains = ['www.melon.com/chart/search/index.htm']
    # start_urls = ['http://www.melon.com/chart/search/index.htm/']
    def start_requests(self):
        yield SeleniumRequest(
            url="https://www.melon.com/chart/month/index.htm",
            wait_time=1,
            screenshot=False,
            callback=self.parse1
        )

    def parse1(self, response):
        driver=response.meta['driver']
        sleep(0.5)
        button_open = driver.find_element(by="xpath",value='//button[@class="button_icons etc arrow_d"]')
        button_open.click()
        sleep(0.2)
        button_to_ranking=driver.find_element(by="xpath",value='//a[@title="2023년 이전 조회 바로가기"]')
        button_to_ranking.click()
        
        yield SeleniumRequest(
            url=driver.current_url,
            wait_time=1,
            callback=self.parse2
        )
                       
    def parse2(self,response):
        sleep(0.2)
        driver=response.meta['driver']
        button_to_month=driver.find_element(by="xpath",value='//h4[@class="tab02"]')
        button_to_month.click()
        sleep(0.2)
        button_to_month=driver.find_element(by="xpath",value='//input[@id="decade_2"]/ancestor::li')
        button_to_month.click()
        sleep(0.2)
        
        #make years List[int]
        years =driver.find_elements(by="xpath",value='//input[@name="year"]/ancestor::li')
        for year in range():
            years[year].click()
            sleep(0.2)
            months=driver.find_elements(by='xpath',value='//input[@name="mon"]/ancestor::li')    
            for month in range(len(months)):
                months[month].click()
                
                sleep(0.2)
                selectors=driver.find_elements(by="xpath",value='//input[@name="classCd"]/ancestor::li')
                selectors[0].click()
                
                sleep(0.2)
                search_button=driver.find_element(by="xpath",value='//button[@title="차트 상세 검색"]')
                search_button.click()
                
                sleep(0.2)
                
                html=driver.page_source
                selector=Selector(text=html)
                
                sleep(0.2)
                
                for elem in selector.xpath('//tr[@class="lst50"]'):
                    yield{                    
                        "year":year,
                        "month":month+1,
                        "rank":elem.xpath('./td[2]/div/span[1]/text()').get(),
                        "song":elem.xpath('./td[4]//div[@class="ellipsis rank01"]//a/text()').get(),
                        "artist":elem.xpath('./td[4]//div[@class="ellipsis rank02"]/a/text()').getall(),
                        "album":elem.xpath('./td[4]//div[@class="ellipsis rank03"]//a/text()').get(),
                        "image":elem.xpath('.//a[@class="image_type15"]/img/@src').get(),
                        "chartname":"melon_all_top100"
                        }   
                next_page=driver.find_element(by="xpath",value='//a[@title="51 - 100 위 - 페이지 이동"]')
                next_page.click()
                
                sleep(0.2)
                
                for elem in selector.xpath('//tr[@class="lst100"]'):
                    yield{
                        "year":year,
                        "month":month+1,
                        "rank":elem.xpath('./td[2]/div/span[1]/text()').get(),
                        "song":elem.xpath('./td[4]//div[@class="ellipsis rank01"]//a/text()').get(),
                        "artist":elem.xpath('./td[4]//div[@class="ellipsis rank02"]/a/text()').getall(),
                        "album":elem.xpath('./td[4]//div[@class="ellipsis rank03"]//a/text()').get(),
                        "image":elem.xpath('.//a[@class="image_type15"]/img/@src').get(),
                        "chartname":"melon_all_top100"
                        }   
                
                    
                sleep(0.2)
        