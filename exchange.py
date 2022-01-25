import requests
from datetime import datetime
# from xml.etree import ElementTree
import xmltodict




def getCurrencyData():
    day = datetime.today().strftime('%d.%m.%Y')
    resp = requests.get(f'https://www.cbar.az/currencies/{day}.xml')
    result = xmltodict.parse(resp.content)
    print(result)
    
getCurrencyData()

