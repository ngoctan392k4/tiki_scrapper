import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

# constructor contains product data
class product_info:
    def __init__(self, brand, price, title, discount, quantity, rating, prod_id):
        self.brand = brand
        self.price = price
        self.title = title
        self.rating = rating
        self.prod_id = prod_id
        self.discount = discount
        self.quantity = quantity

# constructor contains links of each product
class product_link:
    def __init__(self, image, product):
        self.image = image
        self.product = product

# got link extract from menu and number of page from main_build.py
def process_page(link):
    tuple_data = []
    # request url
    html = urlopen(link)

    # html paring
    bs = BeautifulSoup(html, 'html.parser')
    list_prod_id = bs.find_all(attrs={"data-view-id": re.compile('.*')})

    for prod in list_prod_id:
        # extracting data with pattern
        '''
        * TypeError: 'NoneType' object is not subscriptable => use try except

        data_id = prod.find("a", attrs={"data-view-id":re.compile('.*'), "href":re.compile('.*')})['data-view-id']
        data_brand = prod.attrs['style__AboveProductNameStyled-sc-m30gte-0 hjPFIz above-product-name-info']
        data_price = prod.attrs['price-discount__price']
        data_discount = prod.attrs['style__DiscountPercentStyled-sc-e9h7mj-1 StYJD price-discount__percent']
        data_title = prod.attrs['style__NameStyled-sc-139nb47-8 ibOlar']
        data_quantity = prod.attrs['quantity has-border']
        '''
        check = prod.find("a", attrs={"data-view-id": re.compile('.*'), "href": re.compile('.*')})
        if check is not None:
            data_id = check['data-view-id']
        else:
            data_id = None

        try:
            data_brand = prod.attrs['style__AboveProductNameStyled-sc-m30gte-0 hjPFIz above-product-name-info']
        except KeyError:
            data_brand = None

        try:
            data_price = prod.attrs['price-discount__price']
        except KeyError:
            data_price = None

        try:
            data_discount = prod.attrs['style__DiscountPercentStyled-sc-e9h7mj-1 StYJD price-discount__percent']
        except KeyError:
            data_discount = None

        try:
            data_title = prod.attrs['style__NameStyled-sc-139nb47-8 ibOlar']
        except KeyError:
            data_title = None

        try:
            data_quantity = prod.attrs['quantity has-border']
        except KeyError:
            data_quantity = None

        # fixing failed build if no rating data in
        try:
            data_rating = prod.find("div", attrs={"class": re.compile('__StyledStars__')})['__StyledStars__']
        except:
            data_rating = 'null'

        #store and append into tuple object
        product_data = product_info(brand=data_brand, price=data_price, title=data_title, discount = data_discount,
                                quantity = data_quantity, rating=data_rating, prod_id=data_id)

        check1 = prod.find("a", attrs={"data-view-id":re.compile('.*'), "href":re.compile('.*')})
        if check1 is not None:
            data_prod_link = check1['href']
        else:
            data_prod_link = None
        check2 = prod.find("picture", attrs={"class":"webpimg-container", "srcset":re.compile('.*')})
        if check2 is not None:
            data_image_link = check2['srcset']
        else:
            data_image_link = None

        link_data = product_link(image=data_image_link, product=data_prod_link)

        tuple_data = tuple([
            product_data.prod_id,
            product_data.brand,
            product_data.price,
            product_data.title,
            product_data.discount,
            product_data.quantity,
            product_data.rating,
            link_data.image,
            link_data.product,
            link
        ])
    print(tuple_data)

process_page('https://tiki.vn/dien-thoai-smartphone/c1795')