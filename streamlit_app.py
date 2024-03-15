# Import python packages
import streamlit as st
##from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
import requests


# Write directly to the app
st.title(":cup_with_straw: Smoothie Order App :cup_with_straw:")
st.write(
    """Replace this example with your own code!
    **And if you're new to Streamlit,** check
    out our easy-to-follow guides at
    [docs.streamlit.io](https://docs.streamlit.io).
    """
)

title = st.text_input('The name of the Smoothie:', 'The name')
st.write('The name of the Smoothie will be', title)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect('Choose up to 5 ingredients:', my_dataframe, max_selections = 5)
if ingredients_list: 
  
  ingredients_string = ''
  for fruit_chosen in ingredients_list:
    ingredients_string += fruit_chosen + ' '
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
    fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width=True)
      
  st.write(ingredients_string)


  my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """', '""" + title + """')"""
  st.write(my_insert_stmt)

  #st.stop()

    
  time_to_insert = st.button('Submit Order')

  #st.write(my_insert_stmt)
  if time_to_insert:
    session.sql(my_insert_stmt).collect()
    st.success('Your Smoothie is ordered!', icon="✅")


fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width=True)
