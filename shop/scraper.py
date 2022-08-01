import requests, re
from bs4 import BeautifulSoup
from .models import Category, Item, Image, StyleGroup, Style


def scrapeEtsy():
    URL = 'https://www.etsy.com/shop/amicajewels/?etsrc=sdt'
    overview_url = requests.get(URL)
    overview_page = BeautifulSoup(overview_url.content, 'html.parser')

    category_page_links = overview_page.find_all('button', class_='wt-tab__item wt-ml-md-0 wt-mr-md-0 wt-justify-content-space-between')

    for category_page_link in category_page_links:
        category_page_url = category_page_link['data-section-id']
        category_title = category_page_link.findChildren('span', recursive=False)[0].find(text=True).strip()
        category = Category.objects.create(title=category_title)
        category.save()
        print(category)

    items = overview_page.find_all('a', class_='listing-link')
    for item in items:
        item_dict = {}
        item_url = requests.get(item['href'])
        item_page = BeautifulSoup(item_url.content, 'html.parser')
        item_title = item_page.find('h1').decode_contents()
        try:
            # item_price_str = item_page.find('span', text = re.compile('Price:(.*)', re.DOTALL)
            # , attrs={'class': 'wt-screen-reader-only'}).findNext('span').decode_contents()
            item_price_str = item_page.find('p', {'class': 'wt-text-title-03 wt-mr-xs-1'}).decode_contents()
        except:
            print(item['href'])
            item_price_str = item_page.find('p', {'class': 'wt-text-title-03 wt-mr-xs-2'}).decode_contents()
        item_price = float(re.sub('[^\d\.]', '', item_price_str))

        try:
            # item_old_price_str = item_page.find('span', text = re.compile('Original Price:(.*)', re.DOTALL)
            # , attrs={'class': 'wt-screen-reader-only'}).find_parent('p').decode_contents()
            item_old_price_str = item_page.find('p', {'class': 'wt-text-strikethrough wt-text-caption wt-text-gray wt-mr-xs-1'}).decode_contents()
        except:
            print(item_url)
            item_old_price_str = '0'
        item_old_price = float(re.sub('[^\d\.]', '', item_old_price_str))

        item_style_groups = []
        item_style_groups_elements = item_page.find_all(lambda tag:tag.name=="option" and "Select a" in tag.text)
        for i in range(len(item_style_groups_elements)):
            item_style_group = {}
            item_style_group['type'] = item_page.find_all('label', {'class': 'wt-label wt-display-block wt-text-caption'})[i].find(text=True).strip()
            item_style_group['styles'] = []
            for style in item_style_groups_elements[i].findParent().findChildren():
                if not 'Select a' in style.find(text=True):
                    item_style = {}
                    item_style['title'] = style.find(text=True).split('(')[0].strip()
                    try:
                        item_style['price'] = float(re.sub('[^\d\.]', '', style.find(text=True).split('(')[1]))
                    except:
                        pass
                    item_style_group['styles'].append(item_style)

            print(item_style_group)


            item_style_groups.append({})

        print(f"{item_title}: Price-{item_price} Old Price-{item_old_price}")
