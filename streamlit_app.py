# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title(":cup_with_straw: Customize your smoothie :cup_with_straw:")
st.write(
    f"""Choose the fruits you want in your custom smoothie!
    """
)

name_on_order = st.text_input("Name on Smoothie :")
st.write("The name on your Smoothie will be : " , name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("SMOOTHIES.PUBLIC.FRUIT_OPTIONS").select(col('FRUIT_NAME'),col('SEARCH_ON'))
st.dataframe(data=my_dataframe, use_container_width=True)
st.stop()

ingredients_list = st.multiselect(
    "choose upto 5 ingredients:"
    ,my_dataframe
    ,max_selections = 5
)

if ingredients_list:
    INGREDIENTS_STRING = ''
    
    for fruit_chosen in ingredients_list:
         INGREDIENTS_STRING += fruit_chosen + ' '
         st.subheader(fruit_chosen + ' Nutrition Information')
         smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + fruit_chosen)
         sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width= True)

    
    #st.write (INGREDIENTS_STRING)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients)
            values ('""" + INGREDIENTS_STRING + """')"""

    #st.write(my_insert_stmt)
    time_to_insert = st.button('Submit Order ')
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(f'Your Smoothie is ordered {name_on_order} ! '  , icon="✅")







