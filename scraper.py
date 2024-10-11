import requests
from bs4 import BeautifulSoup
import os
import json

class DentalScraper:
    def __init__(self, max_page, image_dir="images"):
        self.url = 'https://dentalstall.com/shop/page/'
        self.max_page = max_page
        self.product_data = []
        self.image_dir = image_dir

        # Create image directory if it doesn't exist
        if not os.path.exists(self.image_dir):
            os.makedirs(self.image_dir)

    def download_image(self, image_url, product_name):
        # Create a valid image file name
        image_name = product_name.replace(" ", "_").replace("/", "_") + ".jpg"
        image_path = os.path.join(self.image_dir, image_name)

        # Download and save the image
        img_data = requests.get(image_url).content
        with open(image_path, 'wb') as handler:
            handler.write(img_data)

        return image_path

    def scrape_page(self, page_number):
        target = self.url + f'{page_number}'
        response = requests.get(target)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            # Find all products
            products = soup.find_all('li', class_='product')

            for product in products:
                # Extract the product name
                name = product.find('h2', class_='woo-loop-product__title').text.strip()

                # Extract the product price
                price = product.find('span', class_='woocommerce-Price-amount').text.strip()

                # Extract the image URL
                noscript_tag = product.find('noscript')
                nosoup = BeautifulSoup(noscript_tag.decode_contents(), 'html.parser')
                image_url = nosoup.find('img')['src']

                # Download the image and get the local path
                image_path = self.download_image(image_url, name)

                # Store the product data
                self.product_data.append({
                    "product_title": name,
                    "product_price": price,
                    "path_to_image": image_path
                })

    def scrape_all_pages(self):
        for i in range(1, self.max_page + 1):
            self.scrape_page(i)

        # Save the data to a local JSON file
        with open('scraped_products.json', 'w') as json_file:
            json.dump(self.product_data, json_file, indent=4)

        print("Data has been saved to 'scraped_products.json'")
