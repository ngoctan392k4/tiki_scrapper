#Set-ExecutionPolicy Unrestricted -Scope Process: use this in powershell to activate venv
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

def process_page(link):
    tuple_data = []
    tuple_data_page = []

    html = urlopen(link)

    bs = BeautifulSoup(html, 'html.parser')
    list_prod_id = bs.find_all('span',attrs={"class": re.compile('StyledItem')})

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

        """ data_id = None
        data_discount = None
        data_brand = None
        data_image_link = None
        data_price = None
        data_prod_link = None
        data_rating = None
        data_title = None
        data_quantity = None """

        #1 Get ID => DONE
        data_id = prod.previous['data-view-content'][15:45]
        for i in range(len(data_id)):
            if data_id[i] == ':':
                data_id = data_id[i+1:]
                break

        for i in range(len(data_id)):
            if data_id[i] == ',':
                data_id = data_id[:i]
                break
        #check = prod.find("a", attrs={"data-view-content"}) # edit
        """ if check is not None:
            data_id = check['data-view-id']
        else:
            data_id = None """

        #2 Get brand => tạm bỏ qua
        try:
            data_brand = prod.find('div', attrs={'span'})
            #check= prod.find('div', class_ = 'above-product-name-info')
            #data_brand = check.find('span').text
           # data_brand = prod.find('div', attrs={'span'}).text
        except KeyError:
            data_brand = None
        """ try:
            data_brand = prod.attrs['style__AboveProductNameStyled-sc-m30gte-0 hjPFIz above-product-name-info'].text
        except KeyError:
            data_brand = None """


        #3 Get price - DONE
        try:
            data_price = prod.find("div", attrs={"class": re.compile('price-discount__price')}).text[:-1]
            for i in range(len(data_price)-2):
                if data_price[i] == '.':
                    data_price = data_price[:i]+data_price[i+1:]
            data_price = int(data_price)
        except KeyError:
            data_price = None


        #4 Get title - DONE
        try:
            data_title = prod.find('h3').text
        except KeyError:
            data_title = None


        #5 Get discount
        data_discount = prod.find("div", attrs={"class": re.compile('price-discount__discount')})
        if data_discount:
            data_discount = data_discount.text
        else:
            data_discount = '0'
            #data_discount = prod.find(class_ = 'price-discount__discount').text.split()[-1]
            #data_discount = prod.attrs['style__DiscountPercentStyled-sc-e9h7mj-1 StYJD price-discount__percent']

        #6 Get quantity - lỗi none
            #trường hợp quantity
        data_quantity = prod.find('span', class_ = 'quantity has-border')
        if data_quantity:
            data_quantity = data_quantity.text
        else:
            data_quantity = prod.find('span', class_ = 'quantity ')
            if data_quantity:
                data_quantity = data_quantity.text
            else:
                data_quantity = 'Đã bán 0'

        #7 Rating - incorrect output
        try:
            all_stars = prod.find_all('g')
            data_rating = len(all_stars)
            #data_rating = prod.find('div', style_='margin-right: 4px; font-size: 14px; line-height: 150%; font-weight: 500;').text
        except:
            data_rating = 'null'

        # print()
        #store and append into tuple object
        product_data = product_info(brand=data_brand, price=data_price, title=data_title, discount = data_discount,
                                quantity = data_quantity, rating=data_rating, prod_id=data_id)


        data_prod_link = "https://tiki.vn"+prod.previous['href']
        #8 done
        check2 = prod.find('source')
        if check2 is not None:
            data_image_link = check2['srcset']
        else:
            data_image_link = None

        link_data = product_link(image=data_image_link, product=data_prod_link)

        tuple_data = tuple([
            product_data.prod_id,
            product_data.brand, # not yet
            product_data.price,
            product_data.title,
            product_data.discount,
            product_data.quantity,
            product_data.rating, # count incorrectly
            link_data.image,
            link_data.product,
            link
        ])
        tuple_data_page.append(tuple_data)
        #return tuple_data_page
        print(tuple_data)
        #print()

process_page('https://tiki.vn/dien-thoai-smartphone/c1795')
