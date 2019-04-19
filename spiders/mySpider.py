import scrapy
import requests
from demo.items import WeightItem
from bs4 import UnicodeDammit
import json
from urllib.parse import urlencode
from bs4 import BeautifulSoup
from urllib.request import urlopen

'''class MySpider(scrapy.Spider):
    name="mySpider"
    n=1
    #source_url = 'https://www.womenshealthmag.com/weight-loss/'
    source_url='https://www.womenshealthmag.com/ajax/infiniteload/?id=c1a430f8-ff5d-433f-85a4-69ed34d4f0ec&class=CoreModels%5Csections%5CSectionModel&viewset=section&' \
               'page='+n+'&cachebuster='
    def start_requests(self):
        url = MySpider.source_url
        yield scrapy.Request(url=url, callback=self.parse)
        print("发送请求")

    def parse(self, response):
        try:

            dammit = UnicodeDammit(response.body, ["utf-8", "gbk"])
            data = dammit.unicode_markup
            selector = scrapy.Selector(text=data)
            print("收到源代码")
            links = selector.xpath("//div[position()>2][starts-with(@class,'simple-item grid-simple-item ')]/a[@class='simple-item-image item-image']")
            print("主页xpath")
            for link in links:
                newslink = link.xpath("./@href").extract_first()
                yield scrapy.Request(url=MySpider.source_url + newslink, callback=self.parse1)
        except Exception as err:
            print(err)

    def parse1(self,response):
                 dammit = UnicodeDammit(response.body, ["utf-8", "gbk"])
                 data = dammit.unicode_markup
                 selector = scrapy.Selector(text=data)
                 text = selector.xpath("//p[@class='body-text']/text()").extract()
                 text = "\n".join(text)
                 #text = selector.xpath("//p[@class='body-text']/text()")[0]
                 #text = text.xpath("string(.)")
                 pic = selector.xpath("/html/body/div[2]/div[4]/div[1]/div[1]/div/img/@data-src").extract_first()


                 header = selector.xpath("//header[@class='content-header standard-header']/div[@class='content-header-inner']")

                 title = header.xpath(".//h1/text()").extract_first()

                 subtitle = header.xpath(".//p/text()").extract_first()

                 profilephoto = header.xpath(".//img/@data-src").extract_first()

                 author = header.xpath(".//span[@class='byline-name']/text()").extract_first()
                 date = header.xpath(".//time[@class='content-info-date']/text()").extract_first()
                 video=""
                 tag="Weightloss"
                 item = WeightItem()


                 item["title"] = title.strip() if title else ""

                 item["tag"] = tag
                 item["subtitle"] = subtitle.strip() if subtitle else ""

                 item["author"] = author.strip() if author else ""

                 item["date"] = date.strip() if date else ""

                 item["profilephoto"] = profilephoto.strip() if profilephoto else ""

                 item["text"] = text.strip() if text else ""

                 item["pic"] = pic.strip() if pic else ""

                 item["video"]=video.strip()if video else ""

                 yield item
'''
class MySpider(scrapy.Spider):
    name = "mySpider"
    source_url = 'https://www.womenshealthmag.com'

    def start_requests(self):
         url_s='https://www.womenshealthmag.com/ajax/infiniteload/?id=d65ec7f5-700b-4a65-a221-3915f81271af&class=CoreModels%5Csections%5CSectionModel&viewset=section&page='
         url_e='&cachebuster='
         x=0
         while x<3:
          x+=1
          if x<19:

              USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'
              url=url_s+str(x)+url_e
              r=requests.get(url,USER_AGENT)
          if x>=19&x<38:
              USER_AGENT='Mozilla / 5.0(Macintosh;Intel Mac OS X 10_14_3) AppleWebKit / 605.1 .15(KHTML, likeGecko) Version / 12.0 .3Safari / 605.1.15'
              url = url_s + str(x) + url_e
              r = requests.get(url, USER_AGENT)


          print(r.status_code)
          selector=scrapy.Selector(text=r.text)
          links=selector.xpath("//div[starts-with(@class,'simple-item grid-simple-item ')]")
          for link in links:
            newslink = link.xpath(".//a[@class='simple-item-image item-image']/@href").extract_first()
            yield scrapy.Request(url=MySpider.source_url+newslink,callback=self.parse1)




    def parse1(self,response):
                 dammit = UnicodeDammit(response.body, ["utf-8", "gbk"])
                 data = dammit.unicode_markup
                 selector = scrapy.Selector(text=data)
                 #text = selector.xpath("//p[@class='body-text']/text()").extract()
                 #print(text)
                 #text = "\n".join(text)
                 strbodytext='<p class="body-text">'
                 gethtml = selector.xpath('//div[contains(@class,"content-lede-image-wrap aspect-ratio-1x1")]'
                                          '|//p[contains(@class,"body-text")]'
                                          '|//h2[contains(@class,"body-h2")]'
                                          '|//div[contains(@class,"product-embed-image-wrap")]'
                                          '|//div[contains(@class,"embed embed-image embed-image-center embed-image-large")]')
                 # 存储为数组list

                 jsondata = []
                 for item in gethtml:
                     jsonone = {}
                     print(str(item))
                     if (str(item).startswith('<Selector xpath=\'//div[contains(@class,"content-lede-image-wrap aspect-ratio-1x1")]|//p[contains(@class,"body-text")]|//h2[contains(@class,"body-h2")]|//div[contains(@class,"product-embed-image-wrap")]|//div[contains(@class,"embed embed-image embed-image-center embed-image-large")]\' data=\'<div class="content-lede-image-wrap aspe'))\
                             |(str(item).startswith('<Selector xpath=\'//div[contains(@class,"content-lede-image-wrap aspect-ratio-1x1")]|//p[contains(@class,"body-text")]|//h2[contains(@class,"body-h2")]|//div[contains(@class,"product-embed-image-wrap")]|//div[contains(@class,"embed embed-image embed-image-center embed-image-large")]\' data=\'<div class="product-embed-image-wrap'))\
                             |(str(item).startswith('<Selector xpath=\'//div[contains(@class,"content-lede-image-wrap aspect-ratio-1x1")]|//p[contains(@class,"body-text")]|//h2[contains(@class,"body-h2")]|//div[contains(@class,"product-embed-image-wrap")]|//div[contains(@class,"embed embed-image embed-image-center embed-image-large")]\' data=\'<div class="embed embed-image embed-image-center embed-image-large')):
                      if  item.xpath('.//img/@data-src'):
                          jsonone['img'] = item.xpath('.//img/@data-src').extract_first()

                      else:
                          jsonone['img'] = item.xpath('.//img/@src').extract_first()



                     if str(item).startswith('<Selector xpath=\'//div[contains(@class,"content-lede-image-wrap aspect-ratio-1x1")]|//p[contains(@class,"body-text")]|//h2[contains(@class,"body-h2")]|//div[contains(@class,"product-embed-image-wrap")]|//div[contains(@class,"embed embed-image embed-image-center embed-image-large")]\' data=\'<p class="body-text'):
                     #if strbodytext in str(item):
                      jsonone['p'] = item.xpath('string(.)').extract()[0]
                     if str(item).startswith('<Selector xpath=\'//div[contains(@class,"content-lede-image-wrap aspect-ratio-1x1")]|//p[contains(@class,"body-text")]|//h2[contains(@class,"body-h2")]|//div[contains(@class,"product-embed-image-wrap")]|//div[contains(@class,"embed embed-image embed-image-center embed-image-large")]\' data=\'<h2 class="body-h2'):
                      jsonone['h2']= item.xpath('string(.)').extract()[0]
                     jsondata.append(jsonone)
                     #print(jsondata)
                 # 保存为json
                 with open("./dd.json", 'w', encoding='utf-8') as json_file:
                     json.dump(jsondata, json_file)
                     #text=open("./dd.json", 'rw',encoding='utf-8')
                 #with open("./dd.json", 'r', encoding='utf-8') as json_file1:
                     #text = json.load(json_file1)
                     #print(json_file1)
                 text=open("./dd.json",encoding='utf-8').read()

                 print(text)
                 #print(type(text))
                 #text = selector.xpath("//p[@class='body-text']/text()")[0]
                 #text = text.xpath("string(.)")
                 pic = selector.xpath("/html/body/div[2]/div[4]/div[1]/div[1]/div/img/@data-src").extract_first()


                 header = selector.xpath("//header[@class='content-header standard-header']/div[@class='content-header-inner']")

                 title = header.xpath(".//h1/text()").extract_first()

                 subtitle = header.xpath(".//p/text()").extract_first()

                 profilephoto = header.xpath(".//img/@data-src").extract_first()

                 author = header.xpath(".//span[@class='byline-name']/text()").extract_first()
                 date = header.xpath(".//time[@class='content-info-date']/text()").extract_first()
                 video=""

                 tag = "Style"
                 item = WeightItem()

                 item["title"] = title.strip() if title else ""

                 item["tag"] = tag
                 item["subtitle"] = subtitle.strip() if subtitle else ""

                 item["author"] = author.strip() if author else ""

                 item["date"] = date.strip() if date else ""

                 item["profilephoto"] = profilephoto.strip() if profilephoto else ""

                 item["text"] = text if text else ""

                 item["pic"] = "" if pic else ""

                 item["video"] = "" if video else ""

                 yield item


















