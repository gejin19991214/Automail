import smtplib
import requests
from datetime import date
from email.mime.text import MIMEText
from bs4 import BeautifulSoup


class Finmail:
    def __init__(self, content):
        self.content = {}

    def crawl(self):
        # U.S. 10-year treasury rate
        ten_T_url = 'https://www.marketwatch.com/investing/bond/tmubmusd10y?countrycode=bx'
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36'}
        f2 = requests.get(ten_T_url, headers=headers)
        soup2 = BeautifulSoup(f2.content, "html.parser")
        ten_year_treasury_yield = soup2.find('h2', {'class' : 'intraday__price sup--right'}).get_text().split('\n')[2]
        self.content['ten_year_treasury_yield'] = ten_year_treasury_yield

        # five year tips rate
        url = 'https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?type=daily_treasury_real_yield_curve&field_tdr_date_value=2022'
        
        f = requests.get(url, headers=headers)
        soup = BeautifulSoup(f.content, "html.parser")
        five_year_tips_rate = soup.find('table', {'class': 'views-table views-view-table cols-16'}).find_all('td', {'class': 'views-field views-field-field-tc-5year'})[-1].get_text().strip()
        self.content['five_year_tips_rate'] = five_year_tips_rate

        # bitcoin price
        key = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"

        bitcoin_data = requests.get(key)
        bitcoin_data = bitcoin_data.json()
        bitcoin_price = str(float(bitcoin_data['price']))
        self.content['bitcoin_price'] = bitcoin_price
        print(self.content)

    def sendmail(self):
        sender = '' # sender, must be a tencent qq email address
        password = '' # password
        receiver = '' # receiver

        subject = "Daily Liquidity Report"  

        today = date.today()
        d = today.strftime("%B %d, %Y")
        ten_year_treasury_yield = 'U.S. 10 Year Treasury Note Yield: ' + str(self.content['ten_year_treasury_yield']) + ' %'
        five_year_tips_rate = 'U.S. 5 Year TIPS Rate: ' + str(self.content['five_year_tips_rate']) + ' %'
        bitcoin_price = 'Bitcoin price: $' + str(self.content['bitcoin_price'])
        content = d + '\n' + ten_year_treasury_yield + '\n' + five_year_tips_rate + '\n' + bitcoin_price + '\n'
        msg = MIMEText(content, 'plain', 'utf-8')
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = receiver
        try:
            client = smtplib.SMTP_SSL('smtp.qq.com', smtplib.SMTP_SSL_PORT)
            print("Connected to server")
        
            client.login(sender, password)
            print("Login succeeded")
        
            client.sendmail(sender, receiver, msg.as_string())
            print("Sent")
        except smtplib.SMTPException as e:
            print(str(e))
        finally:
            client.quit()

