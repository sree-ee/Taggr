import requests
from urllib.parse import quote
from bs4 import BeautifulSoup

def search_redbubble(keyword):
    encoded_keyword = quote(keyword)
    url = f"https://www.redbubble.com/shop/?query={encoded_keyword}&ref=search_box"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text
    else:
        return None

def get_top_product_tags(top_product_link):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
    response = requests.get(top_product_link, headers=headers)
    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        tags_divs = soup.find_all('span', class_='styles_box__54ba70e3 styles_text__5c7a80ef styles_body2__5c7a80ef styles_muted__5c7a80ef')
        tag_list = []
        for div in tags_divs:
            tag_a = div.find('a', class_='styles_link__2ab672d8')
            if tag_a:
                tag_list.append(tag_a.text.strip())
                if len(tag_list) == 17:  # Limit to 17 tags
                    break
        return tag_list
    return None

#keyword = input("Enter a keyword: ")
keyword='barbie'
html = search_redbubble(keyword)
if html:
    print("Search successful!")
    soup = BeautifulSoup(html, 'html.parser')
    top_product_link_element = soup.find('a', class_='styles__link--3QJ5N')
    if top_product_link_element:
        top_product_link = top_product_link_element.get('href')
        print("Top product link:", top_product_link)
        
        product_tags = get_top_product_tags(top_product_link)
        if product_tags:
            print("Product tags:", product_tags)
        else:
            print("Failed to retrieve product tags.")
    else:
        print("Failed to find top product link.")
else:
    print("Failed to retrieve search results.")
