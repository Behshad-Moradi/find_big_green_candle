import requests
import smtplib, ssl
from email.message import EmailMessage
from threading import Thread
import datetime
from time import sleep

def sendEmail(tokenName, message):
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = "behshad.moradi.net@gmail.com"
    receiver_email = "behshad.moradi.net@protonmail.com"
    password = "erjehkzrbwmazhvt"

    msg = EmailMessage()
    msg.set_content(message)
    msg['Subject'] = tokenName
    msg['From'] = sender_email
    msg['To'] = receiver_email

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.send_message(msg, from_addr=sender_email, to_addrs=receiver_email)

def getAllTickers():
    baseUrl = "https://api.kucoin.com"
    endPoint = "/api/v1/market/allTickers"
    result = requests.get(baseUrl + endPoint)
    return result.json()

def sortTickers(data, numbers):
    stableTokens = ['PYUSD-USDT', 'AUSD-USDT', 'USDJ-USDT', 'USDD-USDT', 'USDP-USDT', 'USDE-USDT', 'TUSD-USDT', 'OUSD-USDT']
    counter = 0
    tickers = data['data']['ticker']
    symbols = {}
    for ticker in tickers:
        if ('-USDT' in ticker['symbol'] and '3S' not in ticker['symbol'] and '2S' not in ticker['symbol'] and 'DOWN-USDT' not in ticker['symbol'] and 'UP-USDT' not in ticker['symbol']
            and '2L' not in ticker['symbol'] and '3L' not in ticker['symbol'] and ticker['symbol'] not in stableTokens):
            symbols[ticker['symbol']] = int(float(ticker['volValue']))
        else:
            pass
    #Sort ticker low to high
    sortedSymbol = dict(sorted(symbols.items(), key=lambda item: item[1]))
    return list(sortedSymbol.items())[70: numbers]

def getKlines(timeFrame, token):
    baseUrl = "https://api.kucoin.com"
    endPoint = "/api/v1/market/candles?type={}&symbol={}-USDT".format(timeFrame, token)
    result = requests.get(baseUrl + endPoint)
    return result.json()

def precent(a, b):
    return (float(b) - float(a)) / float(a) * 100

def checkTimerToStart():
    while True:
        _time = datetime.datetime.now().time()
        #print(_time)
        if ((_time.second == 1) and (_time.minute % 15 == 0)):
            break
        sleep(0.2)
    #print("START:", _time)


numbers = 620



"""
[
  [
    "1545904980", //Start time of the candle cycle 0
    "0.058", //opening price 1
    "0.049", //closing price 2
    "0.058", //highest price 3
    "0.049", //lowest price 4
    "0.018", //Transaction volume 5
    "0.000945" //Transaction amount 6
  ]
]
"""
checkTimerToStart()

while True:

    try:
        tickersData = getAllTickers()
        firstTickers = dict(sortTickers(tickersData, numbers))
    except:
        continue


    for x in firstTickers:
        token = x[0:x.rfind("-")]
        try:
            #kliens = getKlines("15min", token)['data']
            kliens = getKlines("15min", token)['data']

        except:
            continue
        
        #کندل حال حاضر
        lastCandle = kliens[0]
        lastCandlePrecent = precent(lastCandle[1], lastCandle[2])
        upperShadow = lastCandle[3] - lastCandle[2]
        smallUpperShadow = upperShadow <= (lastCandle[2] / 100) * 2
        if ((lastCandlePrecent > 6.1) and ((lastCandle[2] == lastCandle[3]) or smallUpperShadow)):
            sendEmail(token, "TEST")
        sleep(0.2)
        '''
        #يکي مانده به کندل حال حاضر
        oneToTheLastCandle = kliens[1]

        #آخرين کندل-صدمين کندل
        firstCandle = kliens[-1]

        betweenPrecent = precent(firstCandle[3], oneToTheLastCandle[4])
        sleep(0.3)
        if ((lastCandlePrecent > 5) and (lastCandlePrecent > betweenPrecent * 2)):
            sendEmail(token, "TEST")
        '''
    sleep(180)
