import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException

from langchain_core.prompts import PromptTemplate

class Chain:
    def __init__(self):
        self.llm = ChatGroq(temperature=0, groq_api_key="your_api_key", model_name="llama-3.1-70b-versatile")

    def summarize_text(self, full_text):
    # Create a prompt template for summarization
        prompt_summarize = PromptTemplate.from_template(
        """
        ### FULL TEXT:
        {document_text}
        ### INSTRUCTION:
        Summarize the text provided above. Provide a concise summary capturing the main points.
        """
        )
    
    # Chain the prompt with the language model
        chain_summarize = prompt_summarize | self.llm
    
    # Invoke the chain with the provided text
        res = chain_summarize.invoke(input={"document_text": full_text})
    
    # Handle the output
        try:
        # Assuming the response from the language model is directly usable
            summary = res.content.strip()  # Stripping any extra whitespace
        except Exception as e:
        # You might want to handle specific exceptions based on your environment
             raise Exception("Failed to summarize the text: {}".format(str(e)))
    
        return summary
    
    def answer_question(self, document_text, user_question):
        prompt_qa = PromptTemplate.from_template(
        """
        ### DOCUMENT TEXT:
        {document_text}
        ### QUESTION:
        {user_question}
        ### ANSWER:
        """
        )

        chain_qa = prompt_qa | self.llm

        res = chain_qa.invoke(input={"document_text": document_text, "user_question": user_question})

        try:
            answer = res.content.strip()
        except Exception as e:
            raise Exception("Failed to answer the question: {}".format(str(e)))
        
        return answer
    

    def translate_text(self, input_text, target_language):
        prompt_translate = PromptTemplate.from_template(
        """
        {input_text}
        ### TRANSLATE TO {target_language}:
        """
    )
        chain_translate = prompt_translate | self.llm
        res = chain_translate.invoke(input={
        "input_text": input_text,
        "target_language": target_language
    })
        try:
        # Assuming the response from the language model is directly usable
            translated_text = res.content.strip()
        except Exception as e:
            raise Exception("Failed to translate text: {}".format(str(e)))
        
        return translated_text

    def classify_document(self, document_text):
        prompt_classify = PromptTemplate.from_template(
        """
        ### DOCUMENT TEXT:
        {document_text}
        ### INSTRUCTION:
        Determine the type of the document from the following categories: Legal, Financial, Medical, Technical.
        ### CATEGORY:
        """
    )
        chain_classify = prompt_classify | self.llm
        res = chain_classify.invoke(input={"document_text": document_text})
        try:
            document_type = res.content.strip()
        except Exception as e:
            raise Exception("Failed to classify the document: {}".format(str(e)))
        
        return document_type
    
    def detect_anomalies(self,document_text):
        prompt_anomaly = PromptTemplate.from_template(
            """
        ### DOCUMENT TEXT:
        {document_text}
        ### INSTRUCTION:
        Identify any anomalies or inconsistencies in the document text. Describe any found issues.
        ### ANOMALIES FOUND:
        """
        )

        chain_anomaly = prompt_anomaly | self.llm
    
        res = chain_anomaly.invoke(input={"document_text": document_text})
        try:
            anomalies = res.content.strip()
        except Exception as e:
            raise Exception("Failed to detect anomalies in the document: {}".format(str(e)))
        
        return anomalies
    
if __name__ == "__main__":
    print("your_api_key")
