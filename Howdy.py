from flask import Flask, request, jsonify
from urllib.request import urlopen, Request
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import sys
app = Flask(__name__)

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--blink-settings=imagesEnabled-false')
chrome_options.add_argument('--disable-extensions')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3')

driver = webdriver.Chrome(options=chrome_options)

page_index = 1
page_items = {}

@app.route('/getproduct', methods=['GET'])
def respond():

    product = request.args.get("product", None)
    
    global page_index

    page_number = '&PageNumber=' + str(page_index)

    url = 'https://www.woolworths.com.au/shop/search/products?searchTerm=' + product + page_number

    driver.get(url)

    # driver.set_page_load_timeout(50)

    WebDriverWait(driver, 2).until(
        EC.presence_of_element_located((By.CLASS_NAME, "product-tile-title"))
    )

    buildItemList()
    
    # Retrieve the name from the url parameter ?name=
    # 

    # # For debugging
    # print(f"Received: {product}")

    # response = {}

    # # Check if the user sent a name at all
    # if not product:
    #     response["ERROR"] = "No name found. Please send a name."
    # # Check if the user entered a number
    # elif str(product).isdigit():
    #     response["ERROR"] = "The name can't be numeric. Please send a string."
    # else:
    #     response["MESSAGE"] = f"Welcome {product} to our awesome API!"

    # # Return the response in json format
    # return jsonify(response)

@app.route('/post/', methods=['POST'])
def post_something():
    param = request.form.get('product')
    print(param)
    # You can add the test cases you made in the previous function, but in our case here you are just testing the POST functionality
    if param:
        return jsonify({
            "Message": f"Welcome {param} to our awesome APIS!",
            # Add this option to distinct the POST request
            "METHOD": "POST"
        })
    else:
        return jsonify({
            "ERROR": "No name found. Please send a name."
        })

@app.route('/')
def index():
    # A welcome message to test our server
    return "<h1>Welcome to our medium-greeting-api!</h1>"

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)
