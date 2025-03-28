#!/usr/bin/env python

"""
  script to download premiumIndexKlines.
  set the absoluate path destination folder for STORE_DIRECTORY, and run

  e.g. STORE_DIRECTORY=/data/ ./download-kline.py

"""
import sys
from datetime import *

import pandas as pd

from enums import MAX_DAYS, START_DATE, END_DATE, DAILY_INTERVALS, FIRST_DAILY_DATE, PERIOD_START_DATE
from utility import download_file, get_all_symbols, get_parser, convert_to_date_object, \
    get_path


def download_monthly_premiumIndexKlines(trading_type, symbols, num_symbols, intervals, years, months, start_date,
                                      end_date, folder, checksum):
    current = 0
    date_range = None

    if start_date and end_date:
        date_range = start_date + " " + end_date

    if not start_date:
        start_date = START_DATE
    else:
        start_date = convert_to_date_object(start_date)

    if not end_date:
        end_date = END_DATE
    else:
        end_date = convert_to_date_object(end_date)

    print("Found {} symbols".format(num_symbols))

    for symbol in symbols:
        print("[{}/{}] - start download monthly {} premiumIndexKlines ".format(current + 1, num_symbols, symbol))
        for interval in intervals:
            for year in years:
                for month in months:
                    current_date = convert_to_date_object('{}-{}-01'.format(year, month))
                    if start_date <= current_date <= end_date:
                        path = get_path(trading_type, "premiumIndexKlines", "monthly", symbol, interval)
                        file_name = "{}-{}-{}-{}.zip".format(symbol.upper(), interval, year, '{:02d}'.format(month))
                        download_file(path, file_name, date_range, folder)

                        if checksum == 1:
                            checksum_path = get_path(trading_type, "premiumIndexKlines", "monthly", symbol, interval)
                            checksum_file_name = "{}-{}-{}-{}.zip.CHECKSUM".format(symbol.upper(), interval, year,
                                                                                   '{:02d}'.format(month))
                            download_file(checksum_path, checksum_file_name, date_range, folder)

        current += 1


def download_daily_premiumIndexKlines(trading_type, symbols, num_symbols, intervals, dates, start_date, end_date, folder,
                                    checksum):
    current = 0
    date_range = None

    if start_date and end_date:
        date_range = start_date + " " + end_date

    if not start_date:
        start_date = START_DATE
    else:
        start_date = convert_to_date_object(start_date)

    if not end_date:
        end_date = END_DATE
    else:
        end_date = convert_to_date_object(end_date)

    # Get valid intervals for daily
    intervals = list(set(intervals) & set(DAILY_INTERVALS))
    print("Found {} symbols".format(num_symbols))

    for symbol in symbols:
        print("[{}/{}] - start download daily {} premiumIndexKlines ".format(current + 1, num_symbols, symbol))
        for interval in intervals:
            for date in dates:
                current_date = convert_to_date_object(date)
                if start_date <= current_date <= end_date:
                    path = get_path(trading_type, "premiumIndexKlines", "daily", symbol, interval)
                    file_name = "{}-{}-{}.zip".format(symbol.upper(), interval, date)
                    download_file(path, file_name, date_range, folder)

                    if checksum == 1:
                        checksum_path = get_path(trading_type, "premiumIndexKlines", "daily", symbol, interval)
                        checksum_file_name = "{}-{}-{}.zip.CHECKSUM".format(symbol.upper(), interval, date)
                        download_file(checksum_path, checksum_file_name, date_range, folder)

        current += 1


if __name__ == "__main__":
    parser = get_parser('klines')
    args = parser.parse_args(sys.argv[1:])

    if not args.symbols:
        print("fetching all symbols from exchange")
        symbols = get_all_symbols(args.type)
        num_symbols = len(symbols)
    else:
        symbols = args.symbols
        num_symbols = len(symbols)

    if args.dates:
        dates = args.dates
    else:
        period = convert_to_date_object(datetime.today().strftime('%Y-%m-%d')) - convert_to_date_object(
            PERIOD_START_DATE)
        dates = pd.date_range(end=datetime.today(), periods=period.days + 1).to_pydatetime().tolist()
        dates = [date.strftime("%Y-%m-%d") for date in dates]
        download_monthly_premiumIndexKlines(args.type, symbols, num_symbols, args.intervals, args.years, args.months,
                                          args.startDate, args.endDate, args.folder, args.checksum)
    download_daily_premiumIndexKlines(args.type, symbols, num_symbols, args.intervals, dates, args.startDate,
                                    args.endDate, args.folder, args.checksum)
