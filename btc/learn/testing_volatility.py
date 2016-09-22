def test_data():
    dates = []
    prices = []
    volumes = []
    try:
        source = open('/home/keyan/fun/algotrading/btc/btceUSD.csv','r').read()
        split_source = source.split('\n')
        for line in split_source[-num:]:
            split_line = line.split(',')
            dates.append(float(split_line[0]))
            prices.append(float(split_line[1]))
            volumes.append(float(split_line[2]))
    except Exception as e:
        print('failed to open data file', str(e))

    print dates[0]

test_data()
