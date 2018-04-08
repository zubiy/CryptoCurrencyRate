import notify2
import requests
import re
from bs4 import BeautifulSoup
"""
Программа считывает имя и курс криптовалюты и выводит в push-уведомлении(или в консоли)
"""
def get_coin(coin, currency):
    url = "https://www.coingecko.com/en/price_charts/"+coin+"/"+currency
    #headers = {'User-Agent': 'Mozilla/5.0'}
    crypto_file = requests.get(url)
    soup = BeautifulSoup(crypto_file.text, "html.parser")
    
    crypto_list = []

    for table in soup.find_all("table", attrs={"class" : "table"}):
        for td in table.find_all("td"):
            crypto_list.append(td.text)

    del crypto_list[3:]
    crypto_list = list(map(lambda s : s.strip(), crypto_list))
    
    #print(crypto_list)
    
    return crypto_list

def get_nameCoin():
    url = "https://www.coingecko.com/en"
    #headers = {'User-Agent': 'Mozilla/5.0'}
    crypto_file = requests.get(url)
    soup = BeautifulSoup(crypto_file.text, "html.parser")
    
    crypto_list=[]
    for table in soup.find_all("table", attrs={"class" : "table table-scrollable mb-0"}):
        for td in table.find_all("td",attrs={"class","coin-name"}):
            for span in td.find_all('span',attrs={"class","coin-content-name"}):
                crypto_list.append(span)
                
    cryptocurrencies=[]
    
    #костыль
    for name in crypto_list:
        coin =str(name).lower()
        r = re.findall('\w+',coin)
        cryptocurrencies.append(r[5])
        if len(cryptocurrencies)>10: break
        
    #Удаление повторяющихся элементов
    cryptocurrencies = list(dict(zip(cryptocurrencies,cryptocurrencies)).values())
   # print(cryptocurrencies)
   
    return cryptocurrencies
    
def notify():
    result = ""
    icon_path = "/home/zubiy/PycharmProjects/Push/logo.png" #путь к картинке 
    for coin in get_nameCoin():
        rate = get_coin(coin, "rub")
        if not rate: continue
        result+=("{} , {} - {}\n".format(rate[0], rate[1], rate[2]))
                 
    #print(result)
        
    notify2.init("Cryptocurrency rates notifier")
    n = notify2.Notification("Crypto Notifier", icon=icon_path)
    n.set_urgency(notify2.URGENCY_CRITICAL)
    n.set_timeout(1000)
    n.update("Current Rates", result)
    n.show()
    
if __name__ == "__main__":
    notify()
