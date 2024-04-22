import streamlit as st
from _03_Recomendation_model import *

# Streamlit app
st.title('Hotel Recommendation System')

package_type = st.selectbox('Select Package Type', data['Package Type'].unique())
start_city = st.selectbox('Select Start City', data['Start City'].unique())
price = st.slider('Select Maximum Price', min_value=0, max_value=100000, step=1000, value=30000)
destination = st.selectbox('Select Destination', data['Destination'].unique())

recommended_hotels = get_hotel_recommendations(package_type, start_city, price, destination)

if st.button('Get Recommendations'):
    recommended_hotels = get_hotel_recommendations(package_type, start_city, price, destination)
    if isinstance(recommended_hotels, str):
        st.error(recommended_hotels)
    else:
        st.table(recommended_hotels)
