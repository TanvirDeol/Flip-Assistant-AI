import streamlit as st
from PIL import Image
import listing_scraper as ls
import results_scraper
import model 
import pandas as pd
import matplotlib.pyplot as plt

col1, col2, col3 = st.beta_columns([1,6,1])
header = st.beta_container()
buy,sell = st.beta_columns([1,1])
market_price = st.beta_container()
hiw = st.beta_container()


phone_model =''
condition = ''
color=''
capacity =''
final_price = 0
links =[]
ls_str = ''
link_data=[]
disp_data = pd.DataFrame()
progress = ''


with col1:
    st.write("")
with col2:
    
    logo = Image.open('banner.png')
    st.image(logo)
with col3:
    st.write("")

with header:
    st.header("Select your specifications:")
    phone_model = st.selectbox('Select Model',
    ('iPhone 3G','iPhone 3GS','iPhone 4','iPhone 4S','iPhone 5C','iPhone 5','iPhone 5S','iPhone 6',
    'iPhone SE 1st Gen','iPhone 6 Plus','iPhone 7','iPhone 7 Plus','iPhone 8','iPhone SE 2nd Gen','iPhone 8 Plus','iPhone XR',
    'iPhone X','iPhone XS','iPhone XS Max','iPhone 11','iPhone 11 Pro','iPhone 11 Pro Max','iPhone 12','iPhone 12 Pro','iPhone 12 Pro Max'))
    
    condition = st.selectbox('Select Condition',('For parts or not working','Used','Seller refurbished','Open box','New'))

    color = st.selectbox('Select Color',('Space Gray','Black','Rose Gold','Product Red','Gold'))
    
    capacity = st.selectbox('Select Capacity',('8 GB','16 GB','32 GB','64 GB','128 GB','256 GB','512 GB'))
    st.write("Note: Wait approx 60s for the real-time data collection.")

def prep_data(type):
    query = ''
    word_list = []
    for w in phone_model.split():
        word_list.append(w)
    for w in condition.split():
        word_list.append(w)
    for w in capacity.split():
        word_list.append(w)
    for i in range(len(word_list)):
        query+=word_list[i].lower()
        if i<len(word_list)-1:
            query+='+'
    progress = 'Loading Data...'
    st.write(progress)
    #st.write(query)
    results_scraper.start(query)
    features = [0,0,0,ls.conv_condition(condition),1,ls.conv_model(phone_model),ls.conv_capacity(capacity)]
    #st.write(features)
    return model.execute(features,type)
    

with buy:
    if st.button('Buy'):
        disp_data,final_price,link_data = prep_data('Buy')
        progress = 'Complete!'
        ls_str = 'Listings Below Market Price:'
        

with sell:
    if st.button('Sell'):
        disp_data,final_price,link_data = prep_data('Sell')
        progress = 'Complete!'
        ls_str = 'Similar Listings'


with market_price:
    st.write(progress)
    st.header('Realtime Market Price:')
    st.subheader('$'+str(final_price)+' CAD')
    st.subheader(ls_str)
    for link in link_data:
        st.write('[Listing]('+link+')')
    st.subheader('Collected Data:')
    st.write(disp_data.head(10))
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    ax.set_xlabel('Condition')
    ax.set_ylabel('Model')
    ax.set_xlabel('Capacity')
    for idx,row in disp_data.iterrows():
        ax.scatter(row['condition'],row['model'],row['capacity'])
    st.subheader("Data Visualization")
    st.pyplot(fig)

with hiw:
    st.title("How it Works:")
    st.markdown('* The program collects user input from site')
    st.markdown('* Gathers listings from eBay in realtime')
    st.markdown('* Trains clustering model (K-means) using collected data')
    st.markdown('* Calculates cluster closest to user\'s input')
    st.markdown('* Does weighted calculations to find market price of user\'s phone')
    st.markdown('* If user wants to buy, it shows listings below market price')
    st.markdown('* If user wants to sell, it shows the statistically most similar listings')
    st.text('Made By: Tanvir Deol and Navjot Singh')