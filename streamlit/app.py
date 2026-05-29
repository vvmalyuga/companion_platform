import streamlit as st, requests, pandas as pd, plotly.express as px
CUBE = "http://localhost:4000/cubejs-api/v1/load"
st.title("Companion Analytics")
dim = st.selectbox("Dimension", ["companionId", "windowStart"])
resp = requests.get(CUBE, params={"query": '{"measures":["CompanionActivity.totalEvents"],"dimensions":["CompanionActivity.'+dim+'"]}'})
df = pd.DataFrame(resp.json()["data"])
st.plotly_chart(px.bar(df, x=f"CompanionActivity.{dim}", y="CompanionActivity.totalEvents"))
if st.button("Drill-down to companions"):
    st.write("Add companion dimension dynamically")
