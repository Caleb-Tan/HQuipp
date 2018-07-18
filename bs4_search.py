import urllib
from bs4 import BeautifulSoup
import requests
import webbrowser
import time


url = 'https://google.com/search?q='
headers = {'User-Agent': 'Chrome/67.0.3396.99'}
soup = ""

def question(query):
    start = time.time()

    response = requests.get(url + query, headers=headers)
    # with open('output1.html', 'wb') as f:
    #    f.write(response.content)
    # webbrowser.open('output2.html')

    soup = BeautifulSoup(response.text, 'lxml')
    results = soup.findAll('div', class_='g')
    placeholder_tag = soup.new_tag("p")
    result = clean(results[0], placeholder_tag)

    if not result:
        result = clean(results[1], placeholder_tag)
    end = round(time.time()-start, 3)
    return {"result": result, "time": end}
    
def clean(html, placeholder_tag):
    if html.find("cite"):
        html.cite.replace_with(placeholder_tag)
    while html.find("a"):
        html.a.replace_with(placeholder_tag)
    while html.find("b"):
        bold_text = html.b.text
        placeholder_tag.string = "**" + bold_text + "**"
        html.b.replace_with(placeholder_tag)
    return html.text    

