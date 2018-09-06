import requests
from bs4 import BeautifulSoup
import re

domain = 'https://www.avito.ru'
city = '/omsk'
category = '/nastolnye_kompyutery'

main_url = domain + city + category

request = requests.get(main_url)
html = request.content

soup = BeautifulSoup(html, "html.parser")
links = soup.select('.item .item-description-title-link')
# urls = [domain + link['href'] for link in links]


def parse_phone():
    return 'empty'


# parsing advert
def parse_url(advert_url):
    r = requests.get(advert_url)
    advert_page = BeautifulSoup(r.content, "html.parser")

    advert_header = advert_page.find(class_='item-view-header')
    advert_content = advert_page.find(class_='item-view-content')

    pub_date_dirty = advert_header.find(class_='title-info-metadata-item').text
    pub_date = re.split(r'размещено', pub_date_dirty)

    advert_info = {
        'title': advert_header.find(class_='title-info-title-text').text,
        'price': advert_header.find(class_='js-item-price')['content'],
        'pub_date': pub_date[1].strip(),
        # 'description': advert_content.find(class_='item-description-text').text
    }

    seller_block = advert_content.find(class_='item-view-seller-info')

    seller_info = {
        'name': seller_block.find(class_='seller-info-name').text.strip(),
        'phone': parse_phone(),
        # 'company': seller_block.find(class_='seller-info-col').find('div', {'class': None}).text,
        # 'experience_on_avito': seller_block.find(class_='seller-info-col').find_all(class_='seller-info-value')[-1].find_all('div')[0].text.strip(),
        # 'finished_adverts': seller_block.find(class_='seller-info-col').find_all(class_='seller-info-value')[-1].find_all('div')[1].text.strip(),
        # 'active_adverts': advert_content.find(class_='seller-info-items-link').text.strip(),
        # 'profile_link': domain + seller_block.a['href'],
        'address': seller_block.find_all(class_='seller-info-prop')[-1].find(class_='seller-info-value').text.strip()
    }

    return {'advert': advert_info, 'seller': seller_info}


for link in links:
    print(parse_url(domain + link['href']))


ad_url = 'https://www.avito.ru/omsk/nastolnye_kompyutery/igrovoy_pk_core_i5_8gb_r9_290_963427366'
print(parse_url(ad_url))


