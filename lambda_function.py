from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import json
import csv
import boto3


def lambda_handler(event, context):
    options = Options()
    options.add_argument('--headless')  # Comment out to view UI
    book_data = []
    website = ('https://www.audible.com/search')
    driver = webdriver.Firefox(options=options)
    driver.get(website)

    while True:
        books = driver.find_elements(by='xpath', value=r"//li[contains(@class, 'productListItem')]")
        for book in books:
            title = book.find_element(by='xpath', value=".//h3[contains(@class, 'bc-heading')]").text
            author = book.find_element(by='xpath', value=".// li[contains( @class , 'authorLabel')]").text
            run_time = book.find_element(by='xpath', value=".// li[contains( @class , 'runtimeLabel')]").text
            book_data.append([title, author[4:], run_time[8:]])

        try:
            driver.find_element(by='xpath',
                                value="//a[contains(@class, 'bc-button-text') and contains(@href, 'pageNext')]").click()
        except Exception as e:
            print('No more pages to scrape')
            break

    with open('books.csv', 'w', newline='',encoding='UTF-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Title', 'Author', 'Runtime'])
        writer.writerows(book_data)

    return {
        'statusCode': 200,
        'body': json.dumps('completed!')
    }


lambda_handler(None, None)
