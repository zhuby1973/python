import os
import tushare as ts
def ReadTxtName(rootdir):
    lines = []
    with open(rootdir, 'r') as file_to_read:
        while True:
            line = file_to_read.readline()
            if not line:
                break
            line = line.strip('\n')
            lines.append(line)
    return lines
stockList = ReadTxtName('20200218A.txt')
print(stockList,sep=',')
#ts.set_token('xxxxxx')
for stock in stockList:
    df = ts.get_hist_data(stock)
    try:
        df.to_csv(stock+'.csv')
    except AttributeError:
        continue;
    print('====================')
print('get data end!!!')

# create 20200218A.txt in same folder as below:
# 600519
# 600000
# 600004
# or you can get a list from http://quote.stockstar.com/stock/stock_index.htm
