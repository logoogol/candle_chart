# !pip install streamlit
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
# from matplotlib import font_manager
# from matplotlib.font_manager import FontProperties
# matplotlib.rc('font', family='SimHei')
import pathlib, os
import yfinance as yf # https://pypi.org/project/yfinance/
from ta.volatility import BollingerBands
from ta.trend import MACD
from ta.momentum import RSIIndicator
import streamlit.components.v1 as components
import mplfinance as mpf
from PIL import Image


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

#option = st.sidebar.selectbox('?????????????????????', ( '000651.sz','AAPL', 'MSFT',"SPY",'WMT'))

##
st.markdown(
    """
<style>
.big-font {
    font-size:30px !important;
    bold;
}
.small-font {
    font-size:13px !important;
    color:blue
}
.sidebar .sidebar-content {
    background-image: linear-gradient(#2e7bcf,#2e7bcf);
    color: white;
}
</style>
""",
    unsafe_allow_html=True,
)
BASE_DIR = pathlib.Path(__file__).parent
img = Image.open(os.path.join(BASE_DIR, "ticker_name", "??????logo.jpg"))
st.sidebar.image(img, caption='')
# st.sidebar.markdown('<p class="big-font">???????????????</p>', unsafe_allow_html=True)
# st.sidebar.markdown('<p class="small-font">????????????????????????</p>', unsafe_allow_html=True)
# st.sidebar.write("????????????????????????")
stock_ticker = st.sidebar.text_input("?????????????????????????????????????????????", '000001')
st.sidebar.button("??????",)
ticker_name = pd.read_pickle(os.path.join(BASE_DIR, "ticker_name","ticker_name_k"))
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
    # st.sidebar.write("(?????????????????????????????????????????????)")
    #st.sidebar.markdown('<p class="small-font">(?????????????????????????????????????????????)</p>', unsafe_allow_html=True)
    x = " "
#option = st.sidebar.selectbox('?????????????????????', ('AAPL', 'MSFT',"SPY",'WMT'))
##


import datetime

today = datetime.date.today()
before = today - datetime.timedelta(days=200)
start_date = st.sidebar.date_input('???????????????', before)
end_date = st.sidebar.date_input('???????????????', today)
if start_date < end_date:
    st.sidebar.success('?????????: `%s`\n\n?????????:`%s`' % (start_date, end_date))
else:
    st.sidebar.error('??????: ????????????????????????????????????')


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

try:
    df = yf.download(x,start= start_date,end= end_date, progress=False)

    st.set_option('deprecation.showPyplotGlobalUse', False)


    mc = mpf.make_marketcolors(up='r',down='g',
                            edge='i',
                            wick={'up':'blue','down':'orange'},
                            volume={'up':'red','down':'green'},
                            ohlc='black')
    s  = mpf.make_mpf_style(marketcolors=mc)
    # s  = mpf.make_mpf_style(marketcolors=mc, rc={'font.family':'sans-serif','font.sans-serif':'SimHei'})

    dlm = mpf.plot(df, type='candle', ylabel='', title="", volume=True, mav=(10,30), style=s)
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

    st.write('??????????????????????????? (MACD)')
    st.bar_chart(macd)

    st.write('???????????? RSI ')
    st.line_chart(rsi)

except:
    st.write("?????????????????????????????????????????????")
# st.write('Recent data ')
# st.dataframe(df.tail(10))
