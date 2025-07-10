import streamlit as st
from db_config import get_db_schema, execute_sql,list_dbs
from llm_sql_generator import generate_sql

db_list = list_dbs()

st.set_page_config(page_title="NL → SQL DB Explorer", layout="wide")
st.title(" Natural Language to SQL Query App")
selected_db = st.selectbox("Select DB:",db_list)
question = st.text_input("Ask a question about your database:")

if question:
    with st.spinner("Generating SQL..."):
        schema = get_db_schema(selected_db)
        sql_query = generate_sql(schema, question)
        st.code(sql_query, language="sql")

        try:
            if sql_query:
                results = execute_sql(sql_query,selected_db)
                st.dataframe(results)
            else :
                st.write("Enter Relavant Query!!")
        except Exception as e:
            st.error(f" Error executing SQL: {e}")
