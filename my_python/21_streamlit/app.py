import streamlit as st

st.title("my first streamlit app created by Kartik soni")

st.write("wELCOME! this app caluculates the squares of number")

st.header("Select a Number")
number = st.slider("Pick a number", 0, 0, 5)

st.subheader("Result")
squared_number = number * number
st.write(f"The square of **{number}** is **{squared_number}**.")


# import streamlit as st: this line import the Streamlit libarary, which is the only dependency you
