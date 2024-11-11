import streamlit as st

#Tiger testing mysql connection11/2 
conn = st.connection('mysql', type='sql') 

df = conn.query('show tables', ttl=6) 
st.write(df)

df = conn.query('select * from broadbcover_by_city limit 5', ttl=6) 
st.write(df)

df = conn.query('select * from population_cover limit 5', ttl=6)
st.write(df)

df = conn.query('select * from use_pc_internet_by_county limit 5', ttl=6)
st.write(df)

df = conn.query('select * from readiness_by_dimensions', ttl=6)
st.write(df)

df = conn.query('select * from Campaign_fund limit 5', ttl=6)
st.write(df)
