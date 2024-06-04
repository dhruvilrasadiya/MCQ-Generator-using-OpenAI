import os
import json
import traceback
import pandas as pd
from dotenv import load_dotenv
from file_functionality import read_file,get_table_data
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain 


load_dotenv()
key = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(openai_api_key=key, model_name="gpt-3.5-turbo", temperature=0.6)

template1 = """

    Text = {text}
    you are an expert MCQ maker, given the above text, it is your job to create a quiz of {number} multiple choice questions fro {subject} students in {tone} tone. make sure that the questions are not repeated and check all the questions to be confirming the text as well. make sure to formate your responce like RESPONCE_JSON below and use it as a guide.
    Ensure to make {number} MCQs.

    
    {responce_json}


"""

quiz_generation_prompt = PromptTemplate(
    input_variables=["text", "number", "subject", "tone", "responce_json"],
    template=template1
)

quiz_chain = LLMChain(llm=llm, prompt=quiz_generation_prompt, output_key="quiz", verbose=True)


template2 = """

    you are an expert english gramerian and writer. given a multiple choice quiz for {subject} student. you need to evaluate the complexity of the question and give a complate analysis of the quiz. only use at maximum 50 words for the question. if the quiz is not at per cognotive and analytical abilities of the student, update the quiz question which needs to be changed and change the tone such that it perfectly fits the student abilities.
    Quiz_MCQ:
    {quiz}

    checkfrom an expert English writer of the above quiz:

"""

quiz_evaluation_prompt = PromptTemplate(
    input_variables=["subject", "quiz"],
    template=template2
)

review_chain = LLMChain(llm=llm, prompt=quiz_evaluation_prompt, output_key = "review", verbose=True)


generate_evaluate_chain = SequentialChain(chains=[quiz_chain,review_chain],input_variables=["text","number","subject","tone","responce_json"],output_variables=["quiz","review"], verbose=True)
