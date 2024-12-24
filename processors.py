import pandas as pd
from typing import List, Tuple, Dict
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from pandasai.llm import OpenAI
import logging
from config import Settings
from models import Question

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TenderProcessor:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.llm = ChatOpenAI(
            api_key=settings.OPENAI_API_KEY,
            model_name=settings.MODEL_NAME,
            temperature=settings.TEMPERATURE
        )
        self.pandas_llm = OpenAI(api_token=settings.OPENAI_API_KEY)

    def is_valid_integer(self, string) -> bool:
        try:
            int(string)
            return True
        except ValueError:
            return False
    
    def extract_questions(self, df: pd.DataFrame) -> List[Question]:
        questions = []
        for i in range(len(df)):
            context = ''
            is_question = False
            is_valid = False
            question_data = {}
            
            for k, v in zip(df.iloc[i].index, df.iloc[i]):
                line = f'{k} : {v}\n'
                context += line
                
                if k == '* Type' and v == 'Question':
                    is_question = True
                elif k == 'System Id' and self.is_valid_integer(v):
                    is_valid = True
            
            if is_question and is_valid:
                question_data['context'] = context
                questions.append(Question(**question_data))
        
        return questions
    
    def process_instructions(self, df: pd.DataFrame) -> str:
        system_prompt = "Instructions for tender processing:\n"
        try:
            for _, row in df.iterrows():
                if isinstance(row[0], str) and not pd.isna(row[0]):
                    system_prompt += f"{row[0]}\n"
        except Exception as e:
            logger.error(f"Error processing instructions: {e}")
            system_prompt += "Error processing complete instructions. Using partial data."
        
        return system_prompt
    
    def generate_answers(self, questions: List[Question], system_prompt: str) -> List[str]:
        template = """
        {system_prompt}
        
        You are an AI assistant helping to fill out tender documentation.
        Please provide a professional and detailed answer to the following question:
        
        Question Context:
        {question_context}
        
        Provide a clear and concise answer that addresses all requirements.
        """
        
        prompt = ChatPromptTemplate.from_template(template)
        answers = []
        
        for question in questions:
            try:
                chain = prompt | self.llm
                response = chain.invoke({
                    "system_prompt": system_prompt,
                    "question_context": question.context
                })
                answers.append(response.content)
            except Exception as e:
                logger.error(f"Error generating answer for question: {e}")
                answers.append("Error generating answer")
        
        return answers