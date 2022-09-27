

import streamlit as st
import datetime
import math
import joblib
import requests
import plotly.express as px
import pandas as pd
import numpy as np
from streamlit_option_menu import option_menu
from streamlit_player import st_player
import streamlit.components.v1 as components

dic = {
    '01':'Jan',
    '02':'Feb',
    '03':'Mar',
    '04':'Apr',
    '05':'May',
    '06':'Jun',
    '07':'Jul',
    '08':'Aug',
    '09':'Sep',
    '10':'Oct',
    '11':'Nov',
    '12':'Dec',
    #week
    '1':'1-7',
    '2':'8-14',
    '3':'15-21',
    '4':'22-31'
}

st.set_page_config(layout="wide")
with st.sidebar:
    choose = option_menu("Welcome", ["Home", "Tech Stack","Currency Exchanger","Customised Charts","Recent Data Charts","Currency Information", "Contributors"],
                         icons=['house', 'stack', 'currency-exchange','graph-down','graph-up','info-circle-fill', 'people-fill'],
                         menu_icon="coin", default_index=0, 
                         styles={
                            "container": {"padding": "5!important", "background-color": "#1a1a1a"},
                            "icon": {"color": "White", "font-size": "25px"}, 
                            "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#4d4d4d"},
                            "nav-link-selected": {"background-color": "#4d4d4d"},
                        }
    ) 


with open("contributors.html",'r') as f:
   contributors=f.read()
def html():
    components.html(contributors,height=1400,scrolling=True)
def exchanger():
    df = pd.read_pickle("sample.pkl")
    left,middle,right = st.columns(3)
    with left:
        inp = st.number_input('AMOUNT',value=1.00,key='first_box')
        
        
    with middle:
        selectcurr1=st.selectbox(
            'FROM',('U.S. dollar (USD) ','Algerian dinar (DZD) ', 'Australian dollar (AUD) ',
       'Bahrain dinar (BHD) ', 'Bolivar Fuerte (VEF) ', 'Botswana pula (BWP) ',
       'Brazilian real (BRL) ', 'Brunei dollar (BND) ',
       'Canadian dollar (CAD) ', 'Chilean peso (CLP) ', 'Chinese yuan (CNY) ',
       'Colombian peso (COP) ', 'Czech koruna (CZK) ', 'Danish krone (DKK) ',
       'Euro (EUR) ', 'Hungarian forint (HUF) ', 'Icelandic krona (ISK) ',
       'Indian rupee (INR) ', 'Indonesian rupiah (IDR) ',
       'Iranian rial (IRR) ', 'Israeli New Shekel (ILS) ',
       'Japanese yen (JPY) ', 'Kazakhstani tenge (KZT) ', 'Korean won (KRW) ',
       'Kuwaiti dinar (KWD) ', 'Libyan dinar (LYD) ',
       'Malaysian ringgit (MYR) ', 'Mauritian rupee (MUR) ',
       'Mexican peso (MXN) ', 'Nepalese rupee (NPR) ',
       'New Zealand dollar (NZD) ', 'Norwegian krone (NOK) ',
       'Omani rial (OMR) ', 'Pakistani rupee (PKR) ', 'Peruvian sol (PEN) ',
       'Philippine peso (PHP) ', 'Polish zloty (PLN) ', 'Qatari riyal (QAR) ',
       'Russian ruble (RUB) ', 'Saudi Arabian riyal (SAR) ',
       'Singapore dollar (SGD) ', 'South African rand (ZAR) ',
       'Sri Lankan rupee (LKR) ', 'Swedish krona (SEK) ', 'Swiss franc (CHF) ',
       'Thai baht (THB) ', 'Trinidadian dollar (TTD) ',
       'Tunisian dinar (TND) ', 'U.A.E. dirham (AED) ', 'U.K. pound (GBP) ',
        'Uruguayan peso (UYU) '),key='second_box'
        )
        
    with right:
        selectcurr2=st.selectbox(
            'TO',('Algerian dinar (DZD) ', 'Australian dollar (AUD) ',
       'Bahrain dinar (BHD) ', 'Bolivar Fuerte (VEF) ', 'Botswana pula (BWP) ',
       'Brazilian real (BRL) ', 'Brunei dollar (BND) ',
       'Canadian dollar (CAD) ', 'Chilean peso (CLP) ', 'Chinese yuan (CNY) ',
       'Colombian peso (COP) ', 'Czech koruna (CZK) ', 'Danish krone (DKK) ',
       'Euro (EUR) ', 'Hungarian forint (HUF) ', 'Icelandic krona (ISK) ',
       'Indian rupee (INR) ', 'Indonesian rupiah (IDR) ',
       'Iranian rial (IRR) ', 'Israeli New Shekel (ILS) ',
       'Japanese yen (JPY) ', 'Kazakhstani tenge (KZT) ', 'Korean won (KRW) ',
       'Kuwaiti dinar (KWD) ', 'Libyan dinar (LYD) ',
       'Malaysian ringgit (MYR) ', 'Mauritian rupee (MUR) ',
       'Mexican peso (MXN) ', 'Nepalese rupee (NPR) ',
       'New Zealand dollar (NZD) ', 'Norwegian krone (NOK) ',
       'Omani rial (OMR) ', 'Pakistani rupee (PKR) ', 'Peruvian sol (PEN) ',
       'Philippine peso (PHP) ', 'Polish zloty (PLN) ', 'Qatari riyal (QAR) ',
       'Russian ruble (RUB) ', 'Saudi Arabian riyal (SAR) ',
       'Singapore dollar (SGD) ', 'South African rand (ZAR) ',
       'Sri Lankan rupee (LKR) ', 'Swedish krona (SEK) ', 'Swiss franc (CHF) ',
       'Thai baht (THB) ', 'Trinidadian dollar (TTD) ',
       'Tunisian dinar (TND) ', 'U.A.E. dirham (AED) ', 'U.K. pound (GBP) ',
       'U.S. dollar (USD) ', 'Uruguayan peso (UYU) '),key='third_box'
        )
    
    left1,middle1,right1=st.columns(3)
    with left1:
            start_date = st.date_input('Start date', datetime.datetime.now().date())
            if st.button('CONVERT'):
                date = f'{str(start_date.day).zfill(2)}-{dic[str(start_date.month).zfill(2)]}-{str(start_date.year)[2:]}'
                df1 = df[(df['Date'] == date)][[selectcurr1,selectcurr2]]
                if len(df1.index) == 0:
                    st.title('Date Not Found')
                elif math.isnan(df1[:][selectcurr1]) or math.isnan(df1[:][selectcurr2]):
                    st.title('Some Cell Is Empty')
                else:
                    # st.dataframe(df1)
                    # temp = df1.iloc[0,0]
                    temp=df1.index
                    value1 = df1.loc[temp[0],selectcurr1]
                    value2 = df1.loc[temp[0],selectcurr2]
                    st.markdown(f'1 {selectcurr1} = {(value2)/(value1)} {selectcurr2}')
                    st.markdown(f'1 {selectcurr2} = {(value1)/(value2)} {selectcurr1}')
                    st.markdown(f'Rate Of {inp} {selectcurr1} = {inp*((value2)/(value1))} {selectcurr2}')
                    # st.markdown(f'Rate Of {inp} {selectcurr2} = {inp*(float(df1[:][selectcurr1])/float(df1[:][selectcurr2]))} {selectcurr1}')
   

with open('techstack.html','r') as f:
    techstack=f.read()
    
def tech():
    components.html(techstack,height=1000,scrolling=True)


def charts():
    
    df = pd.read_pickle("fnl.pkl")
    left,right = st.columns(2)
        
    with left:
        col1 = st.selectbox(
            'BASE',('U.S. dollar (USD) ','Algerian dinar (DZD) ', 'Australian dollar (AUD) ',
       'Bahrain dinar (BHD) ', 'Bolivar Fuerte (VEF) ', 'Botswana pula (BWP) ',
       'Brazilian real (BRL) ', 'Brunei dollar (BND) ',
       'Canadian dollar (CAD) ', 'Chilean peso (CLP) ', 'Chinese yuan (CNY) ',
       'Colombian peso (COP) ', 'Czech koruna (CZK) ', 'Danish krone (DKK) ',
       'Euro (EUR) ', 'Hungarian forint (HUF) ', 'Icelandic krona (ISK) ',
       'Indian rupee (INR) ', 'Indonesian rupiah (IDR) ',
       'Iranian rial (IRR) ', 'Israeli New Shekel (ILS) ',
       'Japanese yen (JPY) ', 'Kazakhstani tenge (KZT) ', 'Korean won (KRW) ',
       'Kuwaiti dinar (KWD) ', 'Libyan dinar (LYD) ',
       'Malaysian ringgit (MYR) ', 'Mauritian rupee (MUR) ',
       'Mexican peso (MXN) ', 'Nepalese rupee (NPR) ',
       'New Zealand dollar (NZD) ', 'Norwegian krone (NOK) ',
       'Omani rial (OMR) ', 'Pakistani rupee (PKR) ', 'Peruvian sol (PEN) ',
       'Philippine peso (PHP) ', 'Polish zloty (PLN) ', 'Qatari riyal (QAR) ',
       'Russian ruble (RUB) ', 'Saudi Arabian riyal (SAR) ',
       'Singapore dollar (SGD) ', 'South African rand (ZAR) ',
       'Sri Lankan rupee (LKR) ', 'Swedish krona (SEK) ', 'Swiss franc (CHF) ',
       'Thai baht (THB) ', 'Trinidadian dollar (TTD) ',
       'Tunisian dinar (TND) ', 'U.A.E. dirham (AED) ', 'U.K. pound (GBP) ',
        'Uruguayan peso (UYU) '),key='first'
        )
        start_date = st.date_input('Start date', datetime.datetime.now().date())

        
    with right:
        col2 = st.selectbox(
            'CURRENCY 2',('Algerian dinar (DZD) ', 'Australian dollar (AUD) ',
       'Bahrain dinar (BHD) ', 'Bolivar Fuerte (VEF) ', 'Botswana pula (BWP) ',
       'Brazilian real (BRL) ', 'Brunei dollar (BND) ',
       'Canadian dollar (CAD) ', 'Chilean peso (CLP) ', 'Chinese yuan (CNY) ',
       'Colombian peso (COP) ', 'Czech koruna (CZK) ', 'Danish krone (DKK) ',
       'Euro (EUR) ', 'Hungarian forint (HUF) ', 'Icelandic krona (ISK) ',
       'Indian rupee (INR) ', 'Indonesian rupiah (IDR) ',
       'Iranian rial (IRR) ', 'Israeli New Shekel (ILS) ',
       'Japanese yen (JPY) ', 'Kazakhstani tenge (KZT) ', 'Korean won (KRW) ',
       'Kuwaiti dinar (KWD) ', 'Libyan dinar (LYD) ',
       'Malaysian ringgit (MYR) ', 'Mauritian rupee (MUR) ',
       'Mexican peso (MXN) ', 'Nepalese rupee (NPR) ',
       'New Zealand dollar (NZD) ', 'Norwegian krone (NOK) ',
       'Omani rial (OMR) ', 'Pakistani rupee (PKR) ', 'Peruvian sol (PEN) ',
       'Philippine peso (PHP) ', 'Polish zloty (PLN) ', 'Qatari riyal (QAR) ',
       'Russian ruble (RUB) ', 'Saudi Arabian riyal (SAR) ',
       'Singapore dollar (SGD) ', 'South African rand (ZAR) ',
       'Sri Lankan rupee (LKR) ', 'Swedish krona (SEK) ', 'Swiss franc (CHF) ',
       'Thai baht (THB) ', 'Trinidadian dollar (TTD) ',
       'Tunisian dinar (TND) ', 'U.A.E. dirham (AED) ', 'U.K. pound (GBP) ',
       'U.S. dollar (USD) ', 'Uruguayan peso (UYU) '),key='second'
        )
        end_date = st.date_input('End date', datetime.datetime.now().date())
    
    if st.button('PLOT'):
        


        
        col0='Date'
        st_date = f'{str(start_date.day).zfill(2)}-{dic[str(start_date.month).zfill(2)]}-{str(start_date.year)[2:]}'
        en_date = f'{str(end_date.day).zfill(2)}-{dic[str(end_date.month).zfill(2)]}-{str(end_date.year)[2:]}'

        # start_date=str(start_date).split('-')
        # start_date=str(start_date[2])+'-'+str(start_date[1])+'-'+str(start_date[0])
        # end_date=str(end_date).split('-')
        # end_date=str(end_date[2])+'-'+str(end_date[1])+'-'+str(end_date[0])
        # st.write(en_date)
        
        df1 = df[(df['Date'] >= st_date) & (df['Date'] <= en_date)][[col0,col1,col2]]
        # st.dataframe(df1)
        st.write(col1)
        maxi=df1[col1].max()
        mini=df1[col1].min()
        c1,c2=st.columns(2)
        with c1:
            st.write("HIGHEST VALUE: ",maxi)
        with c2:
            st.write("LOWEST VALUE: ",mini)
        
        
        st.write(col2)
        maxi1=df1[col2].max()
        mini1=df1[col2].min()
        c3,c4=st.columns(2)
        with c3:
            st.write("HIGHEST VALUE: ",maxi1)
        with c4:
            st.write("LOWEST VALUE: ",mini1)
        plot1 = px.line(
        df1,
        x=col0,
        y=col1,
        template='plotly_white',
        title=f'<b>{col1}</b>')
        plot1.update_layout(xaxis_showgrid=False, yaxis_showgrid=False)
        st.plotly_chart(plot1)

        plot2 = px.line(
        df1,
        x=col0,
        y=col2,
        template='plotly_white',
        title=f'<b>{col2}</b>')
        plot2.update_layout(xaxis_showgrid=False, yaxis_showgrid=False)
        st.plotly_chart(plot2)

        df1['ratio'] = df1[col1]/df[col2]
        col3 = 'ratio'
        plot3 = px.line(
        df1,
        x=col0,
        y='ratio',
        template='plotly_white',
        title=f'<b>Ratio({col1}/{col2})</b>')
        plot3.update_layout(xaxis_showgrid=False, yaxis_showgrid=False)
        st.plotly_chart(plot3)

def charts2():
    
    df = pd.read_pickle("fnl.pkl")
    left,right = st.columns(2)
        
    with left:
        col1 = st.selectbox(
            'BASE',('U.S. dollar (USD) ','Algerian dinar (DZD) ', 'Australian dollar (AUD) ',
       'Bahrain dinar (BHD) ', 'Bolivar Fuerte (VEF) ', 'Botswana pula (BWP) ',
       'Brazilian real (BRL) ', 'Brunei dollar (BND) ',
       'Canadian dollar (CAD) ', 'Chilean peso (CLP) ', 'Chinese yuan (CNY) ',
       'Colombian peso (COP) ', 'Czech koruna (CZK) ', 'Danish krone (DKK) ',
       'Euro (EUR) ', 'Hungarian forint (HUF) ', 'Icelandic krona (ISK) ',
       'Indian rupee (INR) ', 'Indonesian rupiah (IDR) ',
       'Iranian rial (IRR) ', 'Israeli New Shekel (ILS) ',
       'Japanese yen (JPY) ', 'Kazakhstani tenge (KZT) ', 'Korean won (KRW) ',
       'Kuwaiti dinar (KWD) ', 'Libyan dinar (LYD) ',
       'Malaysian ringgit (MYR) ', 'Mauritian rupee (MUR) ',
       'Mexican peso (MXN) ', 'Nepalese rupee (NPR) ',
       'New Zealand dollar (NZD) ', 'Norwegian krone (NOK) ',
       'Omani rial (OMR) ', 'Pakistani rupee (PKR) ', 'Peruvian sol (PEN) ',
       'Philippine peso (PHP) ', 'Polish zloty (PLN) ', 'Qatari riyal (QAR) ',
       'Russian ruble (RUB) ', 'Saudi Arabian riyal (SAR) ',
       'Singapore dollar (SGD) ', 'South African rand (ZAR) ',
       'Sri Lankan rupee (LKR) ', 'Swedish krona (SEK) ', 'Swiss franc (CHF) ',
       'Thai baht (THB) ', 'Trinidadian dollar (TTD) ',
       'Tunisian dinar (TND) ', 'U.A.E. dirham (AED) ', 'U.K. pound (GBP) ',
        'Uruguayan peso (UYU) '),key='first'
        )
        # start_date = st.date_input('Start date', datetime.datetime.now().date())

        
    with right:
        col2 = st.selectbox(
            'CURRENCY 2',('Algerian dinar (DZD) ', 'Australian dollar (AUD) ',
       'Bahrain dinar (BHD) ', 'Bolivar Fuerte (VEF) ', 'Botswana pula (BWP) ',
       'Brazilian real (BRL) ', 'Brunei dollar (BND) ',
       'Canadian dollar (CAD) ', 'Chilean peso (CLP) ', 'Chinese yuan (CNY) ',
       'Colombian peso (COP) ', 'Czech koruna (CZK) ', 'Danish krone (DKK) ',
       'Euro (EUR) ', 'Hungarian forint (HUF) ', 'Icelandic krona (ISK) ',
       'Indian rupee (INR) ', 'Indonesian rupiah (IDR) ',
       'Iranian rial (IRR) ', 'Israeli New Shekel (ILS) ',
       'Japanese yen (JPY) ', 'Kazakhstani tenge (KZT) ', 'Korean won (KRW) ',
       'Kuwaiti dinar (KWD) ', 'Libyan dinar (LYD) ',
       'Malaysian ringgit (MYR) ', 'Mauritian rupee (MUR) ',
       'Mexican peso (MXN) ', 'Nepalese rupee (NPR) ',
       'New Zealand dollar (NZD) ', 'Norwegian krone (NOK) ',
       'Omani rial (OMR) ', 'Pakistani rupee (PKR) ', 'Peruvian sol (PEN) ',
       'Philippine peso (PHP) ', 'Polish zloty (PLN) ', 'Qatari riyal (QAR) ',
       'Russian ruble (RUB) ', 'Saudi Arabian riyal (SAR) ',
       'Singapore dollar (SGD) ', 'South African rand (ZAR) ',
       'Sri Lankan rupee (LKR) ', 'Swedish krona (SEK) ', 'Swiss franc (CHF) ',
       'Thai baht (THB) ', 'Trinidadian dollar (TTD) ',
       'Tunisian dinar (TND) ', 'U.A.E. dirham (AED) ', 'U.K. pound (GBP) ',
       'U.S. dollar (USD) ', 'Uruguayan peso (UYU) '),key='second'
        )
    tslot=st.selectbox('TIME-SLOTS',('WEEKLY','MONTHLY','QUARTERLY','1 YEAR','2 YEAR','5 YEAR','ALL'))
    if st.button('PLOT'):
        
        if tslot=='WEEKLY':
                    
                    st_date=df.iloc[-7,0]
                    en_date=df.iloc[-1,0]
                    df1 = df[(df['Date'] >= st_date) & (df['Date'] <= en_date)][['Date',col1,col2]]
                    # st.write(df1)
                    st.write(col1)
                    maxi=df1[col1].max()
                    mini=df1[col1].min()
                    c1,c2=st.columns(2)
                    with c1:
                        st.write("HIGHEST VALUE: ",maxi)
                    with c2:
                        st.write("LOWEST VALUE: ",mini)
                    
                    
                    st.write(col2)
                    maxi1=df1[col2].max()
                    mini1=df1[col2].min()
                    c3,c4=st.columns(2)
                    with c3:
                        st.write("HIGHEST VALUE: ",maxi1)
                    with c4:
                        st.write("LOWEST VALUE: ",mini1)
                   
                    plot1 = px.line(
                    df1,
                    x='Date',
                    y=col1,
                    template='plotly_white',
                    title=f'<b>{col1}</b>')
                    plot1.update_layout(xaxis_showgrid=False, yaxis_showgrid=False)
                    st.plotly_chart(plot1)

                    plot2 = px.line(
                    df1,
                    x='Date',
                    y=col2,
                    template='plotly_white',
                    title=f'<b>{col2}</b>')
                    plot2.update_layout(xaxis_showgrid=False, yaxis_showgrid=False)
                    st.plotly_chart(plot2)

                    df1['ratio'] = df1[col1]/df[col2]
                    col3 = 'ratio'
                    plot3 = px.line(
                    df1,
                    x='Date',
                    y='ratio',
                    template='plotly_white',
                    title=f'<b>Ratio({col1}/{col2})</b>')
                    plot3.update_layout(xaxis_showgrid=False, yaxis_showgrid=False)
                    st.plotly_chart(plot3)
        elif tslot=='MONTHLY':
                    st_date=df.iloc[-30,0]
                    en_date=df.iloc[-1,0]
                    df1 = df[(df['Date'] >= st_date) & (df['Date'] <= en_date)][['Date',col1,col2]]
                    # st.dataframe(df1)
                    st.write(col1)
                    maxi=df1[col1].max()
                    mini=df1[col1].min()
                    c1,c2=st.columns(2)
                    with c1:
                        st.write("HIGHEST VALUE: ",maxi)
                    with c2:
                        st.write("LOWEST VALUE: ",mini)
                    
                    
                    st.write(col2)
                    maxi1=df1[col2].max()
                    mini1=df1[col2].min()
                    c3,c4=st.columns(2)
                    with c3:
                        st.write("HIGHEST VALUE: ",maxi1)
                    with c4:
                        st.write("LOWEST VALUE: ",mini1)

                    plot1 = px.line(
                    df1,
                    x='Date',
                    y=col1,
                    template='plotly_white',
                    title=f'<b>{col1}</b>')
                    plot1.update_layout(xaxis_showgrid=False, yaxis_showgrid=False)
                    st.plotly_chart(plot1)

                    plot2 = px.line(
                    df1,
                    x='Date',
                    y=col2,
                    template='plotly_white',
                    title=f'<b>{col2}</b>')
                    plot2.update_layout(xaxis_showgrid=False, yaxis_showgrid=False)
                    st.plotly_chart(plot2)

                    df1['ratio'] = df1[col1]/df[col2]
                    col3 = 'ratio'
                    plot3 = px.line(
                    df1,
                    x='Date',
                    y='ratio',
                    template='plotly_white',
                    title=f'<b>Ratio({col1}/{col2})</b>')
                    plot3.update_layout(xaxis_showgrid=False, yaxis_showgrid=False)
                    st.plotly_chart(plot3)
        elif tslot=='QUARTERLY':
                    st_date=df.iloc[-90,0]
                    en_date=df.iloc[-1,0]
                    df1 = df[(df['Date'] >= st_date) & (df['Date'] <= en_date)][['Date',col1,col2]]
                    # st.dataframe(df1)
                    st.write(col1)
                    maxi=df1[col1].max()
                    mini=df1[col1].min()
                    c1,c2=st.columns(2)
                    with c1:
                        st.write("HIGHEST VALUE: ",maxi)
                    with c2:
                        st.write("LOWEST VALUE: ",mini)
                    
                    
                    st.write(col2)
                    maxi1=df1[col2].max()
                    mini1=df1[col2].min()
                    c3,c4=st.columns(2)
                    with c3:
                        st.write("HIGHEST VALUE: ",maxi1)
                    with c4:
                        st.write("LOWEST VALUE: ",mini1)

                    plot1 = px.line(
                    df1,
                    x='Date',
                    y=col1,
                    template='plotly_white',
                    title=f'<b>{col1}</b>')
                    plot1.update_layout(xaxis_showgrid=False, yaxis_showgrid=False)
                    st.plotly_chart(plot1)

                    plot2 = px.line(
                    df1,
                    x='Date',
                    y=col2,
                    template='plotly_white',
                    title=f'<b>{col2}</b>')
                    plot2.update_layout(xaxis_showgrid=False, yaxis_showgrid=False)
                    st.plotly_chart(plot2)

                    df1['ratio'] = df1[col1]/df[col2]
                    col3 = 'ratio'
                    plot3 = px.line(
                    df1,
                    x='Date',
                    y='ratio',
                    template='plotly_white',
                    title=f'<b>Ratio({col1}/{col2})</b>')
                    plot3.update_layout(xaxis_showgrid=False, yaxis_showgrid=False)
                    st.plotly_chart(plot3)
        elif tslot=='1 YEAR':
                    st_date=df.iloc[-365,0]
                    en_date=df.iloc[-1,0]
                    df1 = df[(df['Date'] >= st_date) & (df['Date'] <= en_date)][['Date',col1,col2]]
                    # st.dataframe(df1)
                    st.write(col1)
                    maxi=df1[col1].max()
                    mini=df1[col1].min()
                    c1,c2=st.columns(2)
                    with c1:
                        st.write("HIGHEST VALUE: ",maxi)
                    with c2:
                        st.write("LOWEST VALUE: ",mini)
                    
                    
                    st.write(col2)
                    maxi1=df1[col2].max()
                    mini1=df1[col2].min()
                    c3,c4=st.columns(2)
                    with c3:
                        st.write("HIGHEST VALUE: ",maxi1)
                    with c4:
                        st.write("LOWEST VALUE: ",mini1)

                    plot1 = px.line(
                    df1,
                    x='Date',
                    y=col1,
                    template='plotly_white',
                    title=f'<b>{col1}</b>')
                    plot1.update_layout(xaxis_showgrid=False, yaxis_showgrid=False)
                    st.plotly_chart(plot1)

                    plot2 = px.line(
                    df1,
                    x='Date',
                    y=col2,
                    template='plotly_white',
                    title=f'<b>{col2}</b>')
                    plot2.update_layout(xaxis_showgrid=False, yaxis_showgrid=False)
                    st.plotly_chart(plot2)

                    df1['ratio'] = df1[col1]/df[col2]
                    col3 = 'ratio'
                    plot3 = px.line(
                    df1,
                    x='Date',
                    y='ratio',
                    template='plotly_white',
                    title=f'<b>Ratio({col1}/{col2})</b>')
                    plot3.update_layout(xaxis_showgrid=False, yaxis_showgrid=False)
                    st.plotly_chart(plot3)
        elif tslot=='2 YEAR':
                    st_date=df.iloc[-730,0]
                    en_date=df.iloc[-1,0]
                    df1 = df[(df['Date'] >= st_date) & (df['Date'] <= en_date)][['Date',col1,col2]]
                    # st.dataframe(df1)
                    st.write(col1)
                    maxi=df1[col1].max()
                    mini=df1[col1].min()
                    c1,c2=st.columns(2)
                    with c1:
                        st.write("HIGHEST VALUE: ",maxi)
                    with c2:
                        st.write("LOWEST VALUE: ",mini)
                    
                    
                    st.write(col2)
                    maxi1=df1[col2].max()
                    mini1=df1[col2].min()
                    c3,c4=st.columns(2)
                    with c3:
                        st.write("HIGHEST VALUE: ",maxi1)
                    with c4:
                        st.write("LOWEST VALUE: ",mini1)

                    plot1 = px.line(
                    df1,
                    x='Date',
                    y=col1,
                    template='plotly_white',
                    title=f'<b>{col1}</b>')
                    plot1.update_layout(xaxis_showgrid=False, yaxis_showgrid=False)
                    st.plotly_chart(plot1)

                    plot2 = px.line(
                    df1,
                    x='Date',
                    y=col2,
                    template='plotly_white',
                    title=f'<b>{col2}</b>')
                    plot2.update_layout(xaxis_showgrid=False, yaxis_showgrid=False)
                    st.plotly_chart(plot2)

                    df1['ratio'] = df1[col1]/df[col2]
                    col3 = 'ratio'
                    plot3 = px.line(
                    df1,
                    x='Date',
                    y='ratio',
                    template='plotly_white',
                    title=f'<b>Ratio({col1}/{col2})</b>')
                    plot3.update_layout(xaxis_showgrid=False, yaxis_showgrid=False)
                    st.plotly_chart(plot3)
        elif tslot=='5 YEAR':
                    st_date=df.iloc[-1825,0]
                    en_date=df.iloc[-1,0]
                    df1 = df[(df['Date'] >= st_date) & (df['Date'] <= en_date)][['Date',col1,col2]]
                    # st.dataframe(df1)
                    st.write(col1)
                    maxi=df1[col1].max()
                    mini=df1[col1].min()
                    c1,c2=st.columns(2)
                    with c1:
                        st.write("HIGHEST VALUE: ",maxi)
                    with c2:
                        st.write("LOWEST VALUE: ",mini)
                    
                    
                    st.write(col2)
                    maxi1=df1[col2].max()
                    mini1=df1[col2].min()
                    c3,c4=st.columns(2)
                    with c3:
                        st.write("HIGHEST VALUE: ",maxi1)
                    with c4:
                        st.write("LOWEST VALUE: ",mini1)

                    plot1 = px.line(
                    df1,
                    x='Date',
                    y=col1,
                    template='plotly_white',
                    title=f'<b>{col1}</b>')
                    plot1.update_layout(xaxis_showgrid=False, yaxis_showgrid=False)
                    st.plotly_chart(plot1)

                    plot2 = px.line(
                    df1,
                    x='Date',
                    y=col2,
                    template='plotly_white',
                    title=f'<b>{col2}</b>')
                    plot2.update_layout(xaxis_showgrid=False, yaxis_showgrid=False)
                    st.plotly_chart(plot2)

                    df1['ratio'] = df1[col1]/df[col2]
                    col3 = 'ratio'
                    plot3 = px.line(
                    df1,
                    x='Date',
                    y='ratio',
                    template='plotly_white',
                    title=f'<b>Ratio({col1}/{col2})</b>')
                    plot3.update_layout(xaxis_showgrid=False, yaxis_showgrid=False)
                    st.plotly_chart(plot3)
        elif tslot=='ALL':
                    st_date=df.iloc[0,0]
                    en_date=df.iloc[-1,0]
                    df1 = df[(df['Date'] >= st_date) & (df['Date'] <= en_date)][['Date',col1,col2]]
                    # st.dataframe(df1)
                    st.write(col1)
                    maxi=df1[col1].max()
                    mini=df1[col1].min()
                    c1,c2=st.columns(2)
                    with c1:
                        st.write("HIGHEST VALUE: ",maxi)
                    with c2:
                        st.write("LOWEST VALUE: ",mini)
                    
                    
                    st.write(col2)
                    maxi1=df1[col2].max()
                    mini1=df1[col2].min()
                    c3,c4=st.columns(2)
                    with c3:
                        st.write("HIGHEST VALUE: ",maxi1)
                    with c4:
                        st.write("LOWEST VALUE: ",mini1)

                    plot1 = px.line(
                    df1,
                    x='Date',
                    y=col1,
                    template='plotly_white',
                    title=f'<b>{col1}</b>')
                    plot1.update_layout(xaxis_showgrid=False, yaxis_showgrid=False)
                    st.plotly_chart(plot1)

                    plot2 = px.line(
                    df1,
                    x='Date',
                    y=col2,
                    template='plotly_white',
                    title=f'<b>{col2}</b>')
                    plot2.update_layout(xaxis_showgrid=False, yaxis_showgrid=False)
                    st.plotly_chart(plot2)

                    df1['ratio'] = df1[col1]/df[col2]
                    col3 = 'ratio'
                    plot3 = px.line(
                    df1,
                    x='Date',
                    y='ratio',
                    template='plotly_white',
                    title=f'<b>Ratio({col1}/{col2})</b>')
                    plot3.update_layout(xaxis_showgrid=False, yaxis_showgrid=False)
                    st.plotly_chart(plot3)
def info():
    inf=st.selectbox(
            'CURRENCY SELECTOR',('Algerian dinar (DZD) ', 'Australian dollar (AUD) ',
       'Bahrain dinar (BHD) ', 'Bolivar Fuerte (VEF) ', 'Botswana pula (BWP) ',
       'Brazilian real (BRL) ', 'Brunei dollar (BND) ',
       'Canadian dollar (CAD) ', 'Chilean peso (CLP) ', 'Chinese yuan (CNY) ',
       'Colombian peso (COP) ', 'Czech koruna (CZK) ', 'Danish krone (DKK) ',
       'Euro (EUR) ', 'Hungarian forint (HUF) ', 'Icelandic krona (ISK) ',
       'Indian rupee (INR) ', 'Indonesian rupiah (IDR) ',
       'Iranian rial (IRR) ', 'Israeli New Shekel (ILS) ',
       'Japanese yen (JPY) ', 'Kazakhstani tenge (KZT) ', 'Korean won (KRW) ',
       'Kuwaiti dinar (KWD) ', 'Libyan dinar (LYD) ',
       'Malaysian ringgit (MYR) ', 'Mauritian rupee (MUR) ',
       'Mexican peso (MXN) ', 'Nepalese rupee (NPR) ',
       'New Zealand dollar (NZD) ', 'Norwegian krone (NOK) ',
       'Omani rial (OMR) ', 'Pakistani rupee (PKR) ', 'Peruvian sol (PEN) ',
       'Philippine peso (PHP) ', 'Polish zloty (PLN) ', 'Qatari riyal (QAR) ',
       'Russian ruble (RUB) ', 'Saudi Arabian riyal (SAR) ',
       'Singapore dollar (SGD) ', 'South African rand (ZAR) ',
       'Sri Lankan rupee (LKR) ', 'Swedish krona (SEK) ', 'Swiss franc (CHF) ',
       'Thai baht (THB) ', 'Trinidadian dollar (TTD) ',
       'Tunisian dinar (TND) ', 'U.A.E. dirham (AED) ', 'U.K. pound (GBP) ',
       'U.S. dollar (USD) ', 'Uruguayan peso (UYU) '),key='third_box'
        )
    if st.button('Info'):
        infocsv=pd.read_csv('Currency Data - Sheet1.csv')

        # st.write(len(infocsv.index))
        
        for i in range(0,len(infocsv.index)):
            if inf in (infocsv.iloc[i,0]) or  (infocsv.iloc[i,0]) in inf:
                st.write(infocsv.iloc[i,1])
                break

if choose=="Currency Exchanger":
    exchanger()
elif choose=="Home":
    st.title('NORTHERN TRUST CURRENCY EXCHANGER')
    st.markdown("<p style='text-align: justify; font-size: 18px'>The objective of this project is to maintain real-time information on current market or bank exchange rates, so that the calculated result changes whenever the value of either of the component currencies does. They do so by connecting to a database of current currency exchange rates.</p>", unsafe_allow_html=True)
elif choose=="Customised Charts":
    charts()
elif choose=="Recent Data Charts":
    charts2()
elif choose=="Currency Information":
    info()
elif choose=="Tech Stack":
    tech()
elif choose=="Contributors":
    html()
