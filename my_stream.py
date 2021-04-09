# !pip install streamlit
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.font_manager import FontProperties
matplotlib.rc('font', family='SimHei')
import pathlib, os
import yfinance as yf # https://pypi.org/project/yfinance/
from ta.volatility import BollingerBands
from ta.trend import MACD
from ta.momentum import RSIIndicator
import streamlit.components.v1 as components
import mplfinance as mpf
from pandas_datareader import data


# components.iframe("http://www.greatchinarenaissance.com/")

# components.html(
#     """
#     <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
#     <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
#     <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
#     <div id="accordion">
#       <div class="card">
#         <div class="card-header" id="headingOne">
#           <h5 class="mb-0">
#             <button class="btn btn-link" data-toggle="collapse" data-target="#collapseOne" aria-expanded="true" aria-controls="collapseOne">
#             Collapsible Group Item #1
#             </button>
#           </h5>
#         </div>
#         <div id="collapseOne" class="collapse show" aria-labelledby="headingOne" data-parent="#accordion">
#           <div class="card-body">
#             Collapsible Group Item #1 content
#           </div>
#         </div>
#       </div>
#       <div class="card">
#         <div class="card-header" id="headingTwo">
#           <h5 class="mb-0">
#             <button class="btn btn-link collapsed" data-toggle="collapse" data-target="#collapseTwo" aria-expanded="false" aria-controls="collapseTwo">
#             Collapsible Group Item #2
#             </button>
#           </h5>
#         </div>
#         <div id="collapseTwo" class="collapse" aria-labelledby="headingTwo" data-parent="#accordion">
#           <div class="card-body">
#             Collapsible Group Item #2 content
#           </div>
#         </div>
#       </div>
#     </div>
#     """,
#     height=200,
# )

##################
# Set up sidebar #
##################

# Add in location to select image.

#option = st.sidebar.selectbox('请输入股票代码', ( '000651.sz','AAPL', 'MSFT',"SPY",'WMT'))

##
BASE_DIR = pathlib.Path(__file__).parent
st.sidebar.write("股票分析网站")
st.sidebar.write("开发者：东海宽客")
stock_ticker = st.sidebar.text_input("点击下方输入股票代码")
st.sidebar.button("提交")
ticker_name = pd.read_pickle(os.path.join(BASE_DIR, "ticker_name_k"))
if stock_ticker in ticker_name['ticker'].tolist():
    name = ticker_name.loc[ticker_name['ticker']==stock_ticker, 'name'].values[0]
    # st.write(name)
    st.markdown(f'{name}', unsafe_allow_html=True,)
    if stock_ticker[0] == '6':
        x = stock_ticker + '.ss'
    else:
        x = stock_ticker + '.sz'
elif stock_ticker in ticker_name['name'].tolist():
    name = stock_ticker
    y = ticker_name.loc[ticker_name['name']==stock_ticker, 'ticker'].values[0]
    if y[0] == '6':
        x = y + '.ss'
    else:
        x = y + '.sz'
    #st.write(stock_ticker)
    st.markdown(f'{name}', unsafe_allow_html=True,)
else:
    st.sidebar.write("尚未输入或输入有误，请重新输入")
    x = "600309.ss"
#option = st.sidebar.selectbox('请输入股票代码', ('AAPL', 'MSFT',"SPY",'WMT'))
##


import datetime

today = datetime.date.today()
before = today - datetime.timedelta(days=700)
start_date = st.sidebar.date_input('起始日', before)
end_date = st.sidebar.date_input('截止日', today)
if start_date < end_date:
    st.sidebar.success('起始日: `%s`\n\n截止日:`%s`' % (start_date, end_date))
else:
    st.sidebar.error('错误: 截止日期需要晚于起始日期')


# @st.cache(allow_output_mutation=True)
# def get_data():
#     return []

# user_id = st.text_input("User ID")
# foo = st.slider("foo", 0, 100)
# bar = st.slider("bar", 0, 100)

# if st.button("Add row"):
#     get_data().append({"UserID": user_id, "foo": foo, "bar": bar})

# st.write(pd.DataFrame(get_data()))

##############
# Stock data #
##############

# https://technical-analysis-library-in-python.readthedocs.io/en/latest/ta.html#momentum-indicators

df = yf.download(x,start= start_date,end= end_date, progress=False)
ds = data.DataReader(x,'yahoo', start_date,end_date)
st.set_option('deprecation.showPyplotGlobalUse', False)


mc = mpf.make_marketcolors(up='r',down='g',
                           edge='i',
                           wick={'up':'blue','down':'orange'},
                           volume={'up':'red','down':'green'},
                           ohlc='black')
s  = mpf.make_mpf_style(marketcolors=mc, rc={'font.family':'sans-serif','font.sans-serif':'SimHei'})

dlm = mpf.plot(ds, type='candle', ylabel='价格', title="K线图", volume=True, mav=(10,30), style=s)
st.pyplot(dlm)

# indicator_bb = BollingerBands(df['Close'])

# bb = df
# bb['bb_h'] = indicator_bb.bollinger_hband()
# bb['bb_l'] = indicator_bb.bollinger_lband()
# bb = bb[['Close','bb_h','bb_l']]

macd = MACD(df['Close']).macd()

rsi = RSIIndicator(df['Close']).rsi()


###################
# Set up main app #
###################

# st.write('Stock Bollinger Bands')

# st.line_chart(bb)

# progress_bar = st.progress(0)

# https://share.streamlit.io/daniellewisdl/streamlit-cheat-sheet/app.py

st.write('指数平滑移动平均线 (MACD)')
st.area_chart(macd)

st.write('强弱指数 RSI ')
st.line_chart(rsi)


# st.write('Recent data ')
# st.dataframe(df.tail(10))
