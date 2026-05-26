# Import python packages
import streamlit as st
# from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

cnx = st.connection("snowflake")
session = cnx.session()  

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))


# Write directly to the app
st.title(f"🥤Custom Smoothies Order🥤")
st.write(
  """
  Choose the fruits you want in your custom smoothies!
  """
)

cust_name = st.text_input("Name on Smoothie")
st.write("the name on the smoothie will be: " + cust_name)

ingredient_list = st.multiselect(
    'Choose up to 5 ingredients:'
    , my_dataframe
    , max_selections=6
)

if ingredient_list:

    ingredient_string = ''

    for fruit_choosen in ingredient_list:
        ingredient_string += fruit_choosen+' '

    my_insert_string = """insert into smoothies.public.orders(ingredients, NAME_ON_ORDER)
    values('""" + ingredient_string +"""','""" + cust_name+"""')"""

    # st.write(my_insert_string)

    submit_button = st.button("Submit order")

    if submit_button:
        session.sql(my_insert_string).collect()
        st.success('Your Smoothie is ordered!', icon="✅")


import requests  
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")  
st.text(smoothiefroot_response)
st.text(smoothiefroot_response.json())

sf_df = st.dataframe(data= smoothiefroot_response.json(), use_container_width=true)
