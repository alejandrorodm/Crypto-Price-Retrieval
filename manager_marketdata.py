import marketdata as mkd

temporalities = {
        '1min': 1500 * 60,
        '5min': 1500 * 60 * 5,
        '15min': 1500 * 60 * 15,
        '1hour': 1500 * 60 * 60,
        '4hour': 1500 * 60 * 60 * 4,
        '8hour': 1500 * 60 * 60 * 8,
        '1day': 1500 * 60 * 60 * 24,
        '1week': 1500 * 60 * 60 * 24 * 7,
        '1month': 1500 * 60 * 60 * 24 * 30
    }

def getNowArrayDate():
    """
        Get the current date and time.

    Returns:
        date (array): the current date and time
    """
    now = mkd.getNowDate()
    now_array = [now.year, now. 
                 month, now.day, now.hour, now.minute, now.second]
    return now_array

NOW = getNowArrayDate()

def obtainData (coin, temporality, startDate, endDate, writeOnExcel=True, mav=[]):
    """
        Obtain data in the temporality that you want.

    Args:
        coin (string): the name of the coin (ex: BTC-USDT)
        temporality (string): the desired temporality (1min, 5min, 15min, 1hour, 4hour, 8hour, 1day, 1week, 1month)
        startDate (array int): the start date, must have this format: int(year, month, day, hour, minute, second). Example [2022, 1, 1, 1, 0, 0]
        endDate (array int): the end date, must have this format: int(year, month, day, hour, minute, second). Example [2022, 1, 1, 1, 0, 0]
    
    Returns:
        data (array): the data of the coin in the desired temporality
        excelFile (string): the name of the excel file where the data is stored
    """
    # I use * to iterate over the array
    start_timestamp = mkd.getDatetime_to_timestamp(mkd.getDatetime(*startDate))
    end_timestamp = mkd.getDatetime_to_timestamp(mkd.getDatetime(*endDate))

    if start_timestamp > end_timestamp:
        print("Error, the startDate must be lower than the endDate")
        exit(-1)

    if temporalities.get(temporality):
        if writeOnExcel == True:
            data, excelFile = mkd.multi_threading(start_timestamp, end_timestamp, temporality, coin, writeOnExcel=True)
        else:
            data, excelFile = mkd.multi_threading(start_timestamp, end_timestamp, temporality, coin, writeOnExcel=False)
    else:
        print("Error, please select a correct temporality.")
        exit(-1)

    if len(mav) > 0:
        mkd.addEMAs(mav, excelFile)

    print(f"Done!")

    return data, excelFile
