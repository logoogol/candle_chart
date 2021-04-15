import pandas as pd
import numpy as np
import pickle, os, re, sys, schedule, time
import datetime as dt
from datetime import date
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import mplfinance as mpf
import matplotlib.dates as mdates

## 个股K线图， 创建于2021-01-11
df_history_data = pd.read_pickle('/Users/zhangxiaodong/Desktop/data_from_163/4171只股票价格20161220_'+str(date.today()).replace('-',''))
# df_history_data = pd.read_pickle('/Users/zhangxiaodong/Desktop/data_from_163/4171只股票价格20161220_20210129')
def make_candle_chart_new_way():
    #ticker_name = pd.read_pickle('/Users/zhangxiaodong/Desktop/data_from_163/IPO_date')
    ticker_name = pd.read_pickle('/Users/zhangxiaodong/Desktop/data_from_163/上市公司代码20210105')
    ticker_name = pd.DataFrame(ticker_name)
    ticker_name.columns = ['name']
    initial_input = input('请输入股票代码或名称：')
    date_input = input('请输入日期')
    if date_input == " ":
        end_date = str(date.today())
        start_date = str(date.today() -dt.timedelta(days = 100))
    else: 
        start_date = input('请输入起始日期：')
        end_date = input('请输入截止日期：')
#     end_date = str(date.today())
    if initial_input in ['000016', '000300','000905']:
        df_index = pd.read_pickle('/Users/zhangxiaodong/Desktop/data_from_163/指数/'+initial_input)
        dy = df_index.loc[:,['开盘价','最高价','最低价','收盘价','成交金额(元)']][::-1]
        dy = dy[(dy.index>=start_date)&(dy.index<=end_date)]
        dy.columns =  ['open','high','low','close','volume']
        df_return = "{:0.2%}".format((dy['close'][-1]-dy['close'][0])/dy['close'][0])
        title = initial_input + '\n'+ str(df_return)
    else:
        if initial_input in list(ticker_name.index):
            df_input = initial_input
        else:
            df_input = str(ticker_name[ticker_name['name']==initial_input].index[0])
        stock_name = ticker_name[ticker_name.index==df_input]['name'][0]
#         title = '\n' + df_input + '\n' +stock_name
        if list(df_input)[0] in ['6', '0', '3']:
            ticker = df_input
        else:
            ticker = list(ticker_name[ticker_name.name==df_input].index)[0]

        dw = df_history_data[ticker].iloc[:,[0,3,4,2,1,5]]
        dy = dw[(dw.index>=start_date)&(dw.index<=end_date)]
        dy = dy.astype(float)
        dy = dy[dy['成交金额(万元)'] != 0]
        dy = dy[(dy.T != 0).any()]
        dy.columns =  ['open','low','high','close','volume','pct']
        #df_return = "{:0.2%}".format((dy['close'][-1]-dy['close'][0])/dy['close'][0])
        df_return = "{:0.2%}".format((dy['pct']+1).prod()-1)
#         df_return = "{:0.2%}".format((dy['close'][0]-dy['close'][-1])/dy['close'][-1])
        title = '\n' + df_input + '\n' +stock_name+'\n'+df_return
#     matplotlib.rcParams['font.family'] = ['sans-serif']
#     matplotlib.rcParams['font.sans-serif'] = ['SimHei']
    mc = mpf.make_marketcolors(up='r',down='g',
                           edge='i',
                           wick={'up':'blue','down':'orange'},
                           volume={'up':'red','down':'green'},
                           ohlc='black')
    s  = mpf.make_mpf_style(marketcolors=mc, rc={'font.family':'sans-serif','font.sans-serif':'SimHei'})
    kwargs = dict(type='candle',mav=(5,10,20),volume=True,figratio=(11,8),figscale=1.85, title=title)
    mpf.plot(dy,**kwargs, show_nontrading = True, style=s)
    plt.show()
    
    return(dy)
make_candle_chart_new_way()