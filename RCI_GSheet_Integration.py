import logging
import configparser
import argparse
from concurrent.futures import ThreadPoolExecutor
from google.oauth2.service_account import Credentials
from pandas_datareader import data as pdr
import yfinance as yf
import gspread
import datetime
import pandas as pd
import numpy as np
from retrying import retry
from tqdm import tqdm
import smtplib
from email.mime.text import MIMEText

# Load configuration
config = configparser.ConfigParser()
config.read('config.ini')

scopes = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

credentials = Credentials.from_service_account_file(
    config['DEFAULT']['CredentialsFile'],
    scopes=scopes
)

gc = gspread.authorize(credentials)
sheet = gc.open_by_key(config['DEFAULT']['SheetID'])

logging.basicConfig(level=logging.INFO)

def send_email(subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = config['EMAIL']['From']
    msg['To'] = config['EMAIL']['To']

    with smtplib.SMTP(config['EMAIL']['SMTPServer'], config['EMAIL']['SMTPPort']) as server:
        server.login(config['EMAIL']['Username'], config['EMAIL']['Password'])
        server.send_message(msg)

def getRci(close_prices, period):
    rci_values = [None] * (period - 1)
    for end in range(period - 1, len(close_prices)):
        start = end - period + 1
        period_prices = close_prices[start:end + 1]
        sorted_prices = sorted(period_prices, reverse=True)
        rank_difference_sum = 0
        for i, price in enumerate(period_prices):
            time_rank = period - i
            price_rank = sorted_prices.index(price) + 1
            rank_difference_sum += (time_rank - price_rank) ** 2
        rci = (1 - 6 * rank_difference_sum / (period * (period ** 2 - 1))) * 100
        rci_values.append(round(rci, 2))
    return rci_values

@retry(stop_max_attempt_number=3, wait_fixed=2000)
def fetch_stock_data(ticker, start_date, end_date):
    data = pdr.get_data_yahoo(ticker, start=start_date, end=end_date)
    return data['Close']

def update_sheet_with_rci(worksheet, tickers, period, start_date, end_date):
    def process_ticker(ticker):
        close_prices = fetch_stock_data(ticker, start_date, end_date)
        if close_prices is not None:
            rci_values = getRci(close_prices.tolist(), period)
            return ticker, rci_values
        return ticker, None

    with ThreadPoolExecutor(max_workers=5) as executor:
        results = list(tqdm(executor.map(process_ticker, tickers), total=len(tickers)))

    for ticker, rci_values in results:
        if rci_values is not None:
            cell_range = f'A1:A{len(rci_values)}'
            worksheet.update(cell_range, [[val] for val in rci_values])
            logging.info(f"Updated RCI values for {ticker}")

def main():
    parser = argparse.ArgumentParser(description='RCI GSheet Integration')
    parser.add_argument('--start_date', type=str, required=True, help='Start date in YYYY-MM-DD format')
    parser.add_argument('--end_date', type=str, required=True, help='End date in YYYY-MM-DD format')
    parser.add_argument('--period', type=int, default=14, help='RCI calculation period')
    args = parser.parse_args()

    yf.pdr_override()
    worksheet = sheet.worksheet("NSE")
    tickers = [row[0] for row in worksheet.get_all_values()]
    start_date = datetime.datetime.strptime(args.start_date, '%Y-%m-%d')
    end_date = datetime.datetime.strptime(args.end_date, '%Y-%m-%d')
    period = args.period

    try:
        update_sheet_with_rci(worksheet, tickers, period, start_date, end_date)
        send_email('RCI Update Success', 'The RCI values have been successfully updated.')
    except Exception as e:
        logging.error(f"Error updating RCI values: {e}")
        send_email('RCI Update Failure', f'There was an error updating the RCI values: {e}')

if __name__ == '__main__':
    main()