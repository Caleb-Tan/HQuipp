import urllib
from bs4 import BeautifulSoup
import requests
import webbrowser
from timeit import default_timer as timer


url = 'https://google.com/search?q='

def question(query):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    response = requests.get(url + query, headers=headers)
    # with open('output2.html', 'wb') as f:
    #    f.write(response.content)
    # webbrowser.open('output2.html')

    soup = BeautifulSoup(response.text, 'lxml')
    first_result = soup.find('div', class_='g')
    
    if first_result.find("cite"):
        placeholder_tag = soup.new_tag("p")
        first_result.cite.replace_with(placeholder_tag)
    while first_result.find("a"):
        placeholder_tag = soup.new_tag("p")
        first_result.a.replace_with(placeholder_tag)
    while first_result.find("b"):
        bold_text = first_result.b.text
        placeholder_tag = soup.new_tag("p")
        placeholder_tag.string = "**" + bold_text + "**"
        first_result.b.replace_with(placeholder_tag)

    return first_result.text