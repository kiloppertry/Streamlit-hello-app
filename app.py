import tushare as ts
import pandas as pd
import matplotlib.pylab as plt
import numpy as np
from scipy.stats import norm
import scipy.stats as scs
import time
import math
import plotly.graph_objects as go
import streamlit as st
from pylab import *
from plotly.subplots import make_subplots
#在文件夹位置运行  streamlit run NETLER一体化stream.py
six=pd.read_excel(r'd:\data\llfx101.xls')
six.columns=['date','tens','sixs']
six=six.fillna(axis=0,method='ffill')
df=ts.get_k_data('sh',start='2007-12-14',end=time.strftime('%Y-%m-%d', time.localtime()))
gf=df.iloc[:,[0,2]]
gf.reset_index(drop=True)
six['cha']=-(six.tens-six.sixs)/six.tens
lc=six.loc[:,['date','cha']]
lc.date=lc.date.astype('datetime64[D]')
gf.date=gf.date.astype('datetime64[D]')
qq=pd.merge(lc,gf,how='left')
qq=qq.iloc[580:,:]

st.title('R模型')
fig = make_subplots(specs=[[{"secondary_y": True}]])
fig.add_trace(
    go.Scatter(x=qq.date, y=qq.cha, line=dict(color='orange', width=1)),
    secondary_y=True,
)

fig.add_trace(
    go.Scatter(x=qq.date, y=qq.close, line=dict(color='green', width=1)),
    secondary_y=False,
)

fig.update_xaxes(title_text="时间")
fig.update_yaxes(title_text="<b>上证指数收盘价</b> ", secondary_y=False)
fig.update_yaxes(title_text="<b>R值</b> ", secondary_y=True)
st.plotly_chart(fig,width=1200, height=800, use_container_width=True)
#E模型
gz=pd.read_excel(r'd:\data\llfx101.xls')
gz=gz.iloc[:,[0,1]]
gz.columns=['date','close']
pe=pd.read_excel(r'd:\data\pe.xlsx')
pe.columns=['date','ttm']
gz['r']=gz.close/100
pe['ep']=1/pe.ttm
gz=gz[['date','r']]
pe=pe[['date','ep']]
nep = pd.merge(gz, pe, how='left')

szzs=ts.get_k_data('sh',start='2007-12-14',end=time.strftime('%Y-%m-%d', time.localtime()))
err=nep.loc[:,:]
err['zhi']=1/(err.ep-err.r)
nep.date=nep.date.astype('datetime64[D]')
szzs.date=szzs.date.astype('datetime64[D]')
hh=pd.merge(nep,szzs,on='date')
hh=hh.iloc[580:,:]

st.title('E模型')

fig2 = make_subplots(specs=[[{"secondary_y": True}]])

fig2.add_trace(
    go.Scatter(x=hh.date, y=hh.zhi, line=dict(color='orange', width=1)),
    secondary_y=True,
)

fig2.add_trace(
    go.Scatter(x=hh.date, y=hh.close, line=dict(color='green', width=1)),
    secondary_y=False,
)

fig2.update_xaxes(title_text="时间")
fig2.update_yaxes(title_text="<b>上证指数收盘价</b> ", secondary_y=False)
fig2.update_yaxes(title_text="<b>E值</b> ", secondary_y=True)
st.plotly_chart(fig2,width=1200, height=800, use_container_width=True)
