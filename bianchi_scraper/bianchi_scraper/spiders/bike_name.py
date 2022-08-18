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
            
            yield response.follow(overall_link, callback=self.parse_link, cb_kwargs={'url': response.urljoin(overall_link)})


    def parse_link(self, response, **kwargs):
        link = kwargs['url']

        xpath_link_product = '//div[@class="shop-now"]/a/@href'
        link_product = response.xpath(xpath_link_product).getall()

        for link in link_product:
            yield response.follow(link, callback=self.parse_link_products, cb_kwargs={'url': response.urljoin(link)})

    def parse_link_products(self, response, **kwargs):

        #link = kwargs['url']

        bike_name_xpath = '//h1[@class="page-title"]/span[2]/text()'
        bike_name = response.xpath(bike_name_xpath).get()

        bike_reference_xpath ='//span[@class="page-subtitle"]/span/text()'
        bike_reference = response.xpath(bike_reference_xpath).get()

        bike_modality_xpath = '//div[@class="breadcrumbs-product"]//li/a/text()'
        bike_paths = response.xpath(bike_modality_xpath).getall()

        if len(bike_paths) == 5:
            bike_modality = bike_paths[2]
            bike_type = bike_paths[3]
        else:
            bike_modality = bike_paths[1]
            bike_type = bike_paths[2]

        ##Frame information
        frame_xpath = '//ul[@class="contailer-additional-attributes"]//li[1]/ol/li[1]/span/text()'
        frame = response.xpath(frame_xpath).get()

        fork_xpath = '//ul[@class="contailer-additional-attributes"]//li[1]/ol/li[2]/span/text()'
        fork = response.xpath(fork_xpath).get()

        headset_xpath = '//ul[@class="contailer-additional-attributes"]//li[1]/ol/li[3]/span/text()'
        headset = response.xpath(headset_xpath).get()

        ##Drivetrain information
        shifter_xpath = '//ul[@class="contailer-additional-attributes"]//li[2]/ol/li[1]/span/text()'
        shifter = response.xpath(shifter_xpath).get()

        rear_derailleur_xpath = '//ul[@class="contailer-additional-attributes"]//li[2]/ol/li[2]/span/text()'
        rear_derailleur =  response.xpath(rear_derailleur_xpath).get()

        ##Brakes information
        brakers_xpath = '//ul[@class="contailer-additional-attributes"]//li[3]/ol/li[1]/span/text()'
        brakers = response.xpath(brakers_xpath).get()

        ##Rotor logic
        brakes_information_xpath = '//ul[@class="contailer-additional-attributes"]//li[3]/ol/li'
        brakes_information = response.xpath(brakes_information_xpath).getall()

        if len(brakes_information) == 3:
            rotors_xpath = '//ul[@class="contailer-additional-attributes"]//li[3]/ol/li[3]/span/text()'
            rotors = response.xpath(rotors_xpath).get()
        else:
            rotors_xpath = '//ul[@class="contailer-additional-attributes"]//li[3]/ol/li[2]/span/text()'
            rotors = response.xpath(rotors_xpath).get()

        yield{
            bike_name: {'link': kwargs['url'],
                        'modality': bike_modality,
                        'type': bike_type,
                        'bike_reference': bike_reference,
                        'frame': frame,
                        'fork': fork,
                        'headset': headset,
                        'drivetrain': {
                                        'shifter': shifter,
                                        'rear': rear_derailleur,
                                        },
                        'brakes': {
                                    'brakes': brakers,
                                    'rotor': rotors, 
                        }
                        }
        }

