from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
import bs4
import os
import sys

class Bot:
    def __init__(self):
        self.option = Options()

        self.option.add_argument("--disable-infobars")
        self.option.add_argument("--disable-extensions")
        self.option.add_experimental_option("prefs", {"profile.default_content_setting_values.notifications": 1})

        self.driver = webdriver.Chrome(chrome_options=self.option)

    def search(self, query):
        url = 'https://www.tokopedia.com/search?st=product&q='
        self.query = query
        query.replace(' ','%20')
        self.driver.get(url+self.query)


    def scrape(self):
        soup = bs4.BeautifulSoup(self.driver.page_source, 'lxml')
        items = soup.find_all('span', {'class':'css-1tu1s3r'})
        prices = soup.find_all('span',{'class':'css-o5uqvq'})
        urls = soup.find_all('a', {'class':'css-89jnbj'}, href=True)
        file_name = self.query.replace(' ', '_')
        with open('results_'+file_name+'.txt', 'a') as f:
            for i in range(len(items)):
                f.write('[+]'+items[i].text+": \n")
                f.write('[price]'+prices[i].text+'\n')
                f.write('[link]'+urls[i]['href']+'\n')
                f.write('\n')

    def next(self):
        try:
            self.driver.find_element_by_xpath('//*[@id="zeus-root"]/div/div[2]/div/div[2]/div[4]/i[2]').click()
        except Exception:
            self.driver.find_element_by_xpath('//*[@id="zeus-root"]/div/div[2]/div/div[2]/div[5]/i[2]').click()
            pass

    def stop(self):
        self.driver.quit()

def program():
    print('Loading data')
    for i in range(3):
        print('*')
        sleep(1)
    bot.scrape()
    bot.next()

def mainloop():
    for i in range(5):
        program()
        print('Page '+str(i+1)+' done.')
    bot.stop()

def promptUser():
    prompt = input('Search for '+query+'?[Y/n]')

    if prompt.lower() == 'y':
        print("\nDO NOT CLOSE BROWSER WHILE BOT IS RUNNING. PLS DUDE.")
        global bot
        bot = Bot()
        bot.search(query)
        print('Slurping results for "'+query+'"')
        sleep(1)
        mainloop()

    elif prompt.lower() == 'n':
        print('Ok bye now. Weirdo...')

    else:
        promptUser()


try:
    arg = sys.argv[1]
    if arg == '-h' or arg == '--help':
        print('\nFormatting command:')
        print('tokped [option/search]\n')
        print('-----\n')
        print('example 1(with -h option): python3 tokped.py -h (displays guide/help page)')
        print('example 2(with search): python3 tokped.py topi bundar (collects results for "topi bundar")\n')
        print('-----\n')
        print('option list:')
        print('-h or --help: display guide/help page.')
        print('-v or --version: display current version program.')

    elif arg == '-v' or arg == '--version':
        print('v0.0.1(narasaka)')

    else:
        try:
            arg = sys.argv[1:]
        except Exception:
            print("hi")
        query = ' '.join(arg)
        file_name = query.replace(' ', '_')
        path = './results_'+file_name+'.txt'
        if os.path.exists(path):
            print('You searched this already. Try something else!')
        else:
            promptUser()
except Exception:
    print('Error. Command empty.')
