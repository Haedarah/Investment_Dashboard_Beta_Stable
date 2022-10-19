import numpy as np
import pandas as pd
import pandas_ta as ta
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import yfinance as yf
from datetime import datetime
from datetime import date
from datetime import time
from datetime import timedelta
import time
import altair as alt
from statsmodels.tsa.arima.model import ARIMA
from pmdarima.arima import auto_arima
from statsmodels.tsa.statespace.exponential_smoothing import ExponentialSmoothing

mapping={
"Dollar":"INR=X",
"Euro":"EURINR=X", 
"Bitcoin":"BTC-INR",
"Ethereum":"ETH-INR", 
"Infosys":"INFY.NS",
"TATA Steel":"TATASTEEL.NS",
"ICICI Bank":"ICICIBANK.NS",
"State Bank of India":"SBIN.NS",
"Reliance Industries limited":"RELIANCE.NS"
}

mapping2={
"Dollar":"INR=X",
"Euro":"EURINR=X",  
"Infosys":"INFY.NS",
"TATA Steel":"TATASTEEL.NS",
"ICICI Bank":"ICICIBANK.NS",
"State Bank of India":"SBIN.NS",
"Reliance Industries limited":"RELIANCE.NS"
}

times={
"3 Months":90,
"6 Months":180,
"1 Year":365
}

risk={
"Dollar":-1,
"Euro":-1, 
"Bitcoin":-1,
"Ethereum":-1, 
"Infosys":0,
"TATA Steel":1,
"ICICI Bank":0,
"State Bank of India":0,
"Reliance Industries limited":-1
}

periods={
"1 Day":"1d",
"5 Days":"5d",
"1 Month":"1mo",
"3 Months":"3mo",
"6 Months":"6mo",
"1 Year":"1y",
"2 Years":"2y",
"5 Years":"5y",
"10 Years":"10y",
"Max":"max"
}

intervals={
"1 Minute":"1m",
"2 Minutes":"2m",
"5 Minutes":"5m",
"15 Minutes":"15m",
"30 Minutes":"30m",
"60 Minutes":"60m",
"90 Minutes":"90m",
"1 Day":"1d",
"5 Days":"5d",
"1 Week":"1wk",
"1 Month":"1mo",
"3 Months":"3mo"
}

st.set_page_config(
	page_icon="chart_with_upwards_trend",
    page_title="Investment Dashboard",
    layout="wide",
)

header=st.container()
st.write("""---""")
UpperBlock=st.container()
st.write("""---""")
MiddleBlock=st.container()
LowerBlock=st.container()
st.write("""---""")
footer=st.container()





with header:
	col1,col2=st.columns([1,4],gap="large")

	with col1:
		st.image("Objects/LOGO1.png",use_column_width=True)

	with col2:
		st.title("Indian Investment Dashboard - Beta Version")
		st.write("Prototype of an Indian Investment Dashboard.")





with UpperBlock:

	col1, col2=st.columns([8,3],gap="large")
	with col1:
		st.header("5-Year Historical performance of a stock")
		display1=st.selectbox("Select a stock to plot:",mapping.keys())
		data1=yf.download(tickers=mapping[display1], period="5y")	
		data1=data1.reset_index()	

		plotting1=px.line(data1,x="Date",y="Close",height=800).update_layout(xaxis_title="Date", yaxis_title="Close/₹")
		plotting1.update_traces(line_color="blue", line_width=3)
		st.plotly_chart(plotting1,use_container_width=True)


	with col2:
		st.subheader("Global Indicators/₹")
		
		end=datetime.now()
		start=end-timedelta(hours=end.hour,minutes=end.minute,seconds=end.second)

		try:
			sub_data_1=yf.download(tickers="INR=X", start=start, end=end, interval = "1m")
			dol_close=sub_data_1['Close'][-1]
			dol_diff=dol_close-sub_data_1['Open'][0]
			st.metric("United States Dollar",str('1$ = '+'{:.2f}'.format(dol_close)+' ₹'),str('{:.5f}'.format(dol_diff)+' ₹'))
		except:
			sub_data_11 = yf.download(tickers="INR=X",period="5d",interval="1h")
			st.metric("United States Dollar",str('1$ = '+'{:.2f}'.format(sub_data_11['Close'][-1])+' ₹'),str("showing the last close value"))


		try:	
			sub_data_2=yf.download(tickers="EURINR=X", start=start, end=end, interval = "1m")
			eur_close=sub_data_2['Close'][-1]
			eur_diff=eur_close-sub_data_2['Open'][0]	
			st.metric("EURO",str('1€ = '+'{:.2f}'.format(eur_close)+' ₹'),str('{:.5f}'.format(eur_diff))+' ₹')
		except:
			sub_data_22 = yf.download(tickers="EURINR=X",period="5d",interval="1h")
			st.metric("EURO",str('1€ = '+'{:.2f}'.format(sub_data_22['Close'][-1])+' ₹'),str("showing the last close value"))


		try:
			sub_data_3=yf.download(tickers="BTC-INR", start=start, end=end, interval = "1m")
			btc_close=sub_data_3['Close'][-1]
			btc_diff=btc_close-sub_data_3['Open'][0]
			st.metric("Bitcoin",str('1₿ = '+'{:.2f}'.format(btc_close)+' ₹'),str('{:.5f}'.format(btc_diff))+' ₹')

		except:
			sub_data_33 = yf.download(tickers="BTC-INR",period="5d",interval="1h")
			st.metric("Bitcoin",str('1₿ = '+'{:.2f}'.format(sub_data_33['Close'][-1])+' ₹'),str("showing the last close value"))


		try:
			sub_data_4=yf.download(tickers="ETH-INR", start=start, end=end, interval = "1m")
			eth_close=sub_data_4['Close'][-1]
			eth_diff=eth_close-sub_data_4['Open'][0]
			st.metric("Ethereum",str('1Ξ = '+'{:.2f}'.format(eth_close)+' ₹'),str('{:.5f}'.format(eth_diff))+' ₹')
		except:
			sub_data_44 = yf.download(tickers="ETH-INR",period="5d",interval="1h")
			st.metric("Ethereum",str('1Ξ = '+'{:.2f}'.format(sub_data_44['Close'][-1])+' ₹'),str("showing the last close value"))

		st.write("""---""")
		st.button("Update")



with MiddleBlock:
	st.header("Analysis")
	st.subheader("# Forecasted Performance of a Stock for 5 Days")
	col1,col2,col3=st.columns([1,1,1],gap="large")
	
	with col1:
		stock=st.selectbox("Select a stock for prediction:",mapping2.keys())


	prediction_data=yf.download(tickers=mapping[stock],period="5y",interval="1d")
	prediction_data=prediction_data['Close']

	fixed_index=pd.date_range(prediction_data.index[0],periods=5000,freq='D')
	prediction_data=prediction_data.reindex(fixed_index,method='bfill')
	prediction_data=prediction_data.dropna()
	
	div=int(len(prediction_data)*0.9999)
	train=prediction_data[:div]
	test=prediction_data[div:]
	
	model_auto=auto_arima(train,start_p=2,start_q=2,test="adf",m=1,max_p=6,max_q=6,trace=True,suppress_warnings=True)

	model=ARIMA(train,order=model_auto.get_params().get("order"))
	model=model.fit()

	st.write("p, d, and q of the used ARIMA model are: "+str(model_auto.get_params().get("order")))
	st.write("Displaying the forcasted closing values range for the next 5 days:")

	s=div
	e=len(train)+len(test)-1

	smoothing=ExponentialSmoothing(endog=train)
	smoothing=smoothing.fit()
	preds=smoothing.get_forecast(steps=len(test)+5)
	predictions=preds.summary_frame(alpha=0.03)
	
	test=test.reset_index()
	train=train.reset_index()
	prediction_data=prediction_data.reset_index()
	current_date=test['index'][len(test)-1]

	for i in range(5):
		current_date=current_date+timedelta(days=1)
		new_row={'Date':current_date,'Close':np.nan}
		new_row=pd.DataFrame(new_row,index=[len(test)])
		test=pd.concat([test,new_row])

	predictions=predictions.reset_index()
	predictions['Date']=test['Date']
	
	mnn=predictions['mean_ci_lower'][len(predictions)-1]-0.3
	mxx=predictions['mean_ci_upper'][len(predictions)-1]+0.3


	plotting2=go.Figure()
	plotting2.add_trace(go.Scatter(x=prediction_data['index'][-100:],y=prediction_data['Close'][-100:],mode='lines',line=dict(color="blue",width=4),name="Historical chart"))
	plotting2.add_trace(go.Scatter(x=prediction_data['index'][-100:],y=prediction_data['Close'][-100:],mode='markers',marker=dict(color="blue",size=8),name="Historical values"))
	plotting2.add_trace(go.Scatter(x=predictions['Date'],y=predictions['mean_ci_upper'],mode='lines',line=dict(color="green",width=4),name="Prediction upper bound"))
	plotting2.add_trace(go.Scatter(x=predictions['Date'],y=predictions['mean_ci_lower'],mode='lines',line=dict(color="red",width=4),name="Prediction lower bound"))
	plotting2.add_trace(go.Scatter(x=predictions['Date'],y=predictions['mean'],mode='lines',line=dict(color='gray',width=4),name="Prediction"))


	plotting2.update_layout(xaxis_title="Date", yaxis_title="Close/₹",height=800)
	st.plotly_chart(plotting2,use_container_width=True)


	# plotting2=px.line(prediction_data[-100:],x='Date',y='Close')
	# #plotting2.add_line(predictions,y='mean_ci_upper')
	# plotting2.add_scatter(x=predictions['Date'], y=predictions['mean'],mode='lines',line_color='green')
	# plotting2.add_scatter(x=predictions['Date'], y=predictions['mean_ci_upper'],mode='lines',line_color='yellow')
	# plotting2.add_scatter(x=predictions['Date'], y=predictions['mean_ci_lower'],mode='lines',line_color='yellow',fill='tonexty')
	# st.plotly_chart(plotting2,use_container_width=True)

	# cc1=alt.Chart(predictions).mark_line(color='yellow').encode(x='Date',y='mean_ci_upper')
	# cc2=alt.Chart(predictions).mark_line(color='yellow').encode(x='Date',y='mean_ci_lower')
	# cc3=alt.Chart(prediction_data[-1000:]).mark_line(color='cyan').encode(x='Date',y=alt.Y('Close',title='Close/₹',scale=alt.Scale(domain=[mnn,mxx])))
	# cc4=alt.Chart(predictions).mark_area(color='grey').encode(x='Date',y='mean_ci_upper',y2='mean_ci_lower')
	# st.altair_chart((cc4+cc1+cc2+cc3).properties(height=500).interactive(),use_container_width=True)





with LowerBlock:
	st.subheader("# Candlestick Chart")

	col1,col2,col3,col4=st.columns([1,1,1,1],gap="large")
	
	with col1:
		signal=st.selectbox("Select the stock:",mapping.keys(),index=4)
		
		if risk[signal]==1 :
			st.markdown("<p style='color:Red;'>High risk stock !!</p>",unsafe_allow_html=True)
		elif risk[signal]==0:
			st.markdown("<p style='color:Green;'>Low risk stock</p>",unsafe_allow_html=True)
		else:
			st.markdown("<p style='color:Gray;'>Can't determine risk of the stock.</p>",unsafe_allow_html=True)

	with col2:
		per=st.selectbox("Select the period:",periods.keys(),index=6)

	with col3:
		inter=st.selectbox("Select the intervals:",intervals.keys(),index=7)

	

	data3=yf.download(tickers=mapping[signal],period=periods[per],interval=intervals[inter])
	data3.index.name='Date'
	data3=data3.reset_index()

	st.write("The size of the dataset is: "+str(len(data3)))

	try:
		if len(data3)==0:
			x=1/0
		plotting3=go.Figure(data=[go.Candlestick(x=data3['Date'],open=data3['Open'],high=data3['High'],low=data3['Low'],close=data3['Close'])])
		plotting3.update_layout(xaxis_title="Date", yaxis_title="Close/₹",height=1000)
		st.plotly_chart(plotting3,use_container_width=True)

	except:
		st.write("Please adjust the parameters in order to plot the data properly.")
		st.write("If the size of the dataset is 0, consider increasing the interval value.")
	

	



with footer:
	st.write("AMBILIO Technology")

