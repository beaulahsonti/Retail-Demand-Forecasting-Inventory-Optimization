import streamlit as st

st.set_page_config(
    page_title="Test",
    layout="wide"
)

st.title("RetailPulse Test")
st.write("Streamlit is working correctly.")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Forecast Demand", "12,450")

with col2:
    st.metric("Items", "100")

with col3:
    st.metric("Stores", "10")