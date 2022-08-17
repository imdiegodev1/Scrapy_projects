import scrapy

#Xpath

##initial link i get:
#modality = '//div[@class="bikes-hero"]//h6/text()'
#xpath_subcategories = '//div[@class="col-12 cat-2-ground"]/a/h3/text()'
#subcategories_link = '//div[@class="col-12 cat-2-ground"]/a[1]/@href'
#bike_name = '//article[@class="bike-card fadein fadedin faded"]/h4/a/text()'

class BikeNameSpider (scrapy.Spider):
    name = 'bike_name'
    ##Bike's links by categories
    start_urls = [
        'https://www.bianchi.com/bikes/bikes/road/racing-road/',        #Road
        'https://www.bianchi.com/bikes/bikes/road/endurance-road/',     #Road
        'https://www.bianchi.com/bikes/bikes/road/cyclocross-road/',    #Road
        'https://www.bianchi.com/bikes/bikes/road/tt-triathlon-road/',  #Road
        'https://www.bianchi.com/bikes/bikes/mtb/cross-country-mtb/',   #MTB
        'https://www.bianchi.com/bikes/bikes/gravel-road/'              #Gravel
    ]

    custom_settings = {
        'FEED_URI': 'bike_info.json',
        'FEED_FORMAT': 'json',
        'FEED_EXPORT_ENCODING': 'utf-8'
    }

    def parse(self, response):


        ##Get link for bikes subcategories
        xpath_link_subcategories = '//div[@class="col-12 cat-2-ground"]/a[1]/@href'
        bikes_link_subcategories = response.xpath(xpath_link_subcategories).getall()

        print(bikes_link_subcategories)

        #Navigate through each link
        for overall_link in bikes_link_subcategories:
            
            yield response.follow(overall_link, callback=self.parse_link2, cb_kwargs={'url': response.urljoin(overall_link)})

            #xpath_link_product = '//div[@class="shop-now"]/a/text()'
            #link_product = response.xpath(xpath_link_product).getall()
            #print('***'*10)
            #print(link_product)

#            for link in link_product:
#                yield response.follow(link, callback=self.parse_link3, cb_kwargs={'url': response.urljoin(link)})

    def parse_link2 (self, response, **kwargs):
        link = kwargs['url']

        xpath_link_product = '//div[@class="shop-now"]/a/@href'
        link_product = response.xpath(xpath_link_product).getall()

        for link in link_product:
            yield response.follow(link, callback=self.parse_link3, cb_kwargs={'url': response.urljoin(link)})

    def parse_link3( self, response, **kwargs):

        link = kwargs['url']
        yield{
            'links': link
        }

    def parse_link(self, response, **kwargs):
        
        link = kwargs['url']

        xpath_modality = '//div[@class="third-level-hero"]/a/h6/text()'
        modality = response.xpath(xpath_modality).get()

        xpath_subcategories = '//div[@class="third-level-hero"]/h1/text()'
        subcategories = response.xpath(xpath_subcategories).get()

        xpath_bike_names = '//div[@class="col-md-6"]//h4/a/text()'
        bike_names = response.xpath(xpath_bike_names).getall()

        yield{
            'url': link,
            'modality': modality,
            'subcategories': subcategories,
            'bike_names': bike_names
        }

    #    yield {
    #        'bike_name': bike_names
    #    }


    ##'//div[@class="col-12 cat-2-ground"]/a[1]/@href'    -> importante
    ##//*[@id="main"]/div[3]/div/div[1]/a[2]/h3
    ##//*[@id="main"]/div[3]/div/div[2]/a[2]/h3
    ##/html/body/div[5]/div[3]/section/main/div[3]/div/div[1]