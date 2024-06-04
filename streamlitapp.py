import os
import json
import traceback
import pandas as pd
from dotenv import load_dotenv
from file_functionality import read_file,get_table_data
import streamlit as st
from langchain.callbacks import get_openai_callback
from app import generate_evaluate_chain


with open(r"C:/Users/DHRUVIL/OneDrive/Desktop/MCQGenerator/responce.json", 'r') as file:
    RESPONCE_JSON = json.load(file)

st.title("MCQ generator using langchain")

with st.form("user_inputs"):
    uploaded_file = st.file_uploader("upload a pdf or text file")

    mcq_count = st.number_input("No. of MCQs", min_value=3,max_value=50)

    subject = st.text_input("insert Subject", max_chars=20)

    tone = st.text_input("complexity level of question", max_chars=20, placeholder='simple')

    button = st.form_submit_button("Generate MCQs")


    if button and uploaded_file is not None and mcq_count and subject and tone:
        with st.spinner("loading..."):
            try:
                text = read_file(uploaded_file)
                with get_openai_callback() as cb:
                    responce = generate_evaluate_chain(
                        {
                            "text": text,
                            "number": mcq_count,
                            "subject": subject,
                            "tone": tone,
                            "responce_json": json.dumps(RESPONCE_JSON)
                                }
                    )

            except Exception as e:
                traceback.print_exception(type(e),e,e.__traceback__)
                st.error("error")

            else:

                if isinstance(responce, dict):
                    quiz = responce.get("quiz",None)
                    if quiz is not None:
                        table_data = get_table_data(quiz)
                        if table_data is not None:
                            df = pd.DataFrame(table_data)
                            df.index = df.index+1
                            st.table(df)

                            st.text_area(label='Review', value=responce['review'])
                    
                    else:
                        st.error("error in the table data")
                
                else:
                    st.write(responce)
