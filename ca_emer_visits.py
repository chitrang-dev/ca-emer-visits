import streamlit as st
import pandas as pd
import numpy as np
from st_files_connection import FilesConnection

st.title('CA Emergency Dept Visit Trends')
st.subheader('Takeways:')
st.caption('1. More than 10 million visits to the Emergency Department (ED) across California in 2021')
st.caption('2. Total ED visits still below pre-COVID19 levels')
st.caption('3. Number of Uninsured patients visting the ED dropped starting in 2014 (Obamacare) and corresponding expansion in Medi-Cal patients')

DATA_URL= ('https://st-emer-data.s3.us-west-1.amazonaws.com/output.tbl')


@st.cache_data
def load_data():
    conn = st.experimental_connection('s3', type=FilesConnection)
    data = conn.read("st-emer-data/output.tbl", input_format="csv", ttl=600, delimiter='|')
    return data

#data_load_state = st.text('Loading data...')
data = load_data()
#data_load_state.text("Done! (using st.cache_data)")

data_grouped = data[["year","medicare","medi_cal","private_coverage","uninsured"]].groupby(by="year").sum()
st.bar_chart(data_grouped)

st.subheader('Check your local Emergency Department:')

hosp_list = data.sort_values(by="facility").facility.unique()
#st.write(hosp_list)

hosp_to_filter = st.selectbox('Select a Hospital:', hosp_list)
filtered_data = data[data.facility.eq(hosp_to_filter)]

st.line_chart(data=filtered_data, x="year", y=["medicare", "medi_cal", "private_coverage", "uninsured"])


if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(filtered_data)
