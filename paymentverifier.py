```python
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests, time, sqlite3, os

conn = sqlite3.connect('transactions.db')
cursor = conn.cursor()
cursor.execute(
    '''
        CREATE TABLE IF NOT EXISTS Transactions(
            invoice VARCHAR(50) PRIMARY KEY,
            bank_name VARCHAR(50),
            name VARCHAR(50),
            date DATE
        )
    '''
)

print('--------------- PAYMENT VERIFIER ---------------')
Method = int(input('1. Telebirr \n2. Abyssinia\n3. Database\nChoose your payment method => '))
IN = input('Invoice / Transaction reference number => ')


def Telebirr():
    web = requests.get(f'https://transactioninfo.ethiotelecom.et/receipt/{IN}')
    soup = BeautifulSoup(web.content, 'html.parser')

    invoice = soup.find_all('td', class_="receipttableTd")[3].text.strip()
    payer = soup.find_all('td', attrs={'style':'text-align: left'})[0].text.strip()
    reciver = soup.find_all('td', attrs={'style':'text-align: left'})[6].text.strip()
    pn = soup.find_all('td', attrs={'style':'text-align: left'})[7].text.strip()
    status = soup.find_all('td', attrs={'style':'text-align: left'})[8].text.strip()
    date = soup.find_all('td', class_='receipttableTd')[4].text.strip()
    amount = soup.find_all('td', class_='receipttableTd')[5].text.strip()

    cursor.execute('SELECT invoice FROM Transactions WHERE invoice == ?', (invoice,))
    data = cursor.fetchall()

    if not data:
        if reciver == os.getenv('TELEBIRR_RECEIVER', 'EXAMPLE_RECEIVER'):
            if pn == os.getenv('TELEBIRR_PHONE', 'EXAMPLE_PHONE'):
                if status == 'Completed':
                    if amount == os.getenv('TELEBIRR_AMOUNT', '800.00 Birr'):
                        cursor.execute(
                            'INSERT INTO Transactions VALUES (?, ?, ?, ?)',
                            (invoice, 'Telebirr', payer, date)
                        )
                        conn.commit()
                        print('Payment Verified!')
                    else:
                        print('amount is incorrect!')
                else:
                    print('status is not completed!')
            else:
                print('phone number is incorrect!')
        else:
            print('Reciver name is incorrect!')
    else:
        print('This invoice number had already been used!')


def Abyssinia():
    options = Options()
    options.add_argument('--headless')

    driver = webdriver.Chrome(options=options)
    driver.get(f'https://cs.bankofabyssinia.com/slip/?trx={IN}')
    time.sleep(3)

    attr = 'border-bottom: 1px solid black; border-left: none; border-right: none; text-align: right;'
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    invoice = soup.find_all('td', attrs={'style': attr})[5].text.strip()
    account = soup.find_all('td', attrs={'style': attr})[0].text.strip()
    name = soup.find_all('td', attrs={'style': attr})[1].text.strip()
    amount = soup.find_all('td', attrs={'style': attr})[2].text.strip()
    date = soup.find_all('td', attrs={'style': attr})[4].text.strip()

    cursor.execute('SELECT invoice FROM Transactions WHERE invoice == ?', (invoice,))
    data = cursor.fetchall()

    if not data:
        if account == os.getenv('ABYSSINIA_ACCOUNT', 'EXAMPLE_ACCOUNT'):
            if name == os.getenv('ABYSSINIA_NAME', 'EXAMPLE_NAME'):
                if amount == os.getenv('ABYSSINIA_AMOUNT', 'ETB 200.00'):
                    cursor.execute(
                        'INSERT INTO Transactions VALUES (?, ?, ?, ?)',
                        (invoice, 'Abyssinia', 'Verified Customer', date)
                    )
                    conn.commit()
                    print('payment verified!')
                else:
                    print('amount is incorrect')
            else:
                print('name doesn\'t match')
        else:
            print('account doesn\'t match')
    else:
        print('This invoice number had already been used!')

    driver.quit()


def DBViewer():
    cursor.execute(
        '''
            SELECT * FROM Transactions
        '''
    )
    data = cursor.fetchall()

    for datas in data:
        print(datas)


if Method == 1:
    Telebirr()
elif Method == 2:
    Abyssinia()
elif Method == 3:
    DBViewer()
else:
    print('Enter from the list above!')

conn.close()
```
