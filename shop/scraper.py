import os, requests, re, urllib
from bs4 import BeautifulSoup
from .models import Category, Item, Image, StyleGroup, Style


def scrapeEtsy():
    URL = 'https://www.etsy.com/shop/amicajewels/?etsrc=sdt'
    overview_url = requests.get(URL)
    overview_page = BeautifulSoup(overview_url.content, 'html.parser')

    category_page_links = overview_page.find_all('button', class_='wt-tab__item wt-ml-md-0 wt-mr-md-0 wt-justify-content-space-between')

    for category_page_link in category_page_links:
        category_page_url_id = category_page_link['data-section-id']
        category_page_url =requests.get(f"{URL}&section_id={category_page_url_id}")
        category_title = category_page_link.findChildren('span', recursive=False)[0].find(text=True).strip()

        if Category.objects.filter(title=category_title).exists():
            category = Category.objects.get(title=category_title)
        else:
            category = Category.objects.create(title=category_title)
            category.save()
        print(category)

        category_page = BeautifulSoup(category_page_url.content, 'html.parser')

        items = category_page.find_all('a', class_='listing-link')
        for item in items:
            item_dict = {}
            item_url = requests.get(item['href'])
            item_page = BeautifulSoup(item_url.content, 'html.parser')
            item_title = item_page.find('h1').decode_contents()

            if Item.objects.filter(title=item_title).exists():
                item = Item.objects.get(title=item_title)
                item.categories.add(category)

            else:
                item = Item.objects.create(title=item_title)

            try:
                # item_price_str = item_page.find('span', text = re.compile('Price:(.*)', re.DOTALL)
                # , attrs={'class': 'wt-screen-reader-only'}).findNext('span').decode_contents()
                item_price_str = item_page.find('p', {'class': 'wt-text-title-03 wt-mr-xs-1'}).decode_contents()
            except:
                print(item['href'])
                item_price_str = item_page.find('p', {'class': 'wt-text-title-03 wt-mr-xs-2'}).decode_contents()
            item_price = float(re.sub('[^\d\.]', '', item_price_str))
            item.price = item_price

            try:
                # item_old_price_str = item_page.find('span', text = re.compile('Original Price:(.*)', re.DOTALL)
                # , attrs={'class': 'wt-screen-reader-only'}).find_parent('p').decode_contents()
                item_old_price_str = item_page.find('p', {'class': 'wt-text-strikethrough wt-text-caption wt-text-gray wt-mr-xs-1'}).decode_contents()
            except:
                print(item_url)
                item_old_price_str = '0'
            item_old_price = float(re.sub('[^\d\.]', '', item_old_price_str))
            item.old_price = item_old_price
            item.save()

            item_images = item_page.find_all('img', {'class': 'wt-max-width-full wt-horizontal-center wt-vertical-center carousel-image wt-rounded'})
            print(item_images)

            for item_image in item_images:
                if not item.image_set.filter(image=f"/item_images/{item_image['alt']}.jpg").exists():
                    try:
                        if item_image.has_attr('src'):
                            item_image_src = item_image.get('src')
                        else:
                            item_image_src = item_image.get('data-src')
                        print(item_image_src)
                        with open(f"media/item_images/{item_image['alt']}.jpg", "wb") as f:
                            f.write(requests.get(item_image_src).content)
                            image = Image.objects.create()
                            image.image = f"/item_images/{item_image['alt']}.jpg"
                            image.item = item
                            image.save()

                    except:
                        print('Issue at: ' + item_image_src)

            item_style_groups = []
            item_style_groups_elements = item_page.find_all(lambda tag:tag.name=="option" and "Select a" in tag.text)
            for i in range(len(item_style_groups_elements)):
                item_style_group = {}
                item_style_group['type'] = item_page.find_all('label', {'class': 'wt-label wt-display-block wt-text-caption'})[i].find(text=True).strip()
                if not item.stylegroup_set.filter(type=item_style_group['type']).exists():
                    style_group = StyleGroup.objects.create(type=item_style_group['type'])
                    style_group.item = item
                else:
                    style_group = item.stylegroup_set.get(type=item_style_group['type'])

                style_group.save()
                item_style_group['styles'] = []
                for style in item_style_groups_elements[i].findParent().findChildren():
                    if not 'Select a' in style.find(text=True):
                        item_style = {}
                        item_style['title'] = style.find(text=True).split('(')[0].strip()
                        if not style_group.style_set.filter(title=item_style['title']).exists():
                            style = Style.objects.create(title=item_style['title'])
                            style.style_group = style_group
                        else:
                            style = style_group.style_set.get(title=item['title'])
                        try:
                            item_style['price'] = float(re.sub('[^\d\.]', '', style.find(text=True).split('(')[1]))
                            style.price = item_style['price']
                        except:
                            pass
                        item_style_group['styles'].append(item_style)
                        style.save()

                print(item_style_group)

            print(f"{item_title}: Price-{item_price} Old Price-{item_old_price}")
