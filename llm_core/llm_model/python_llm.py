from langchain_core.prompts import ChatPromptTemplate
from ..prompt_template.programing_prompt import (
    COMMENT_GENERATOR_SYS_PRT,
    CHAT_GENERATOR_SYS_PRT,
    CODE_GENERATOR_SYS_PRT,
    CODE_COMPLETOR_SYS_PRT,
)


class CommentGenerator:
    def __init__(self, llm):
        self._llm = llm

    def generate_comment(self, query):
        system = COMMENT_GENERATOR_SYS_PRT
        human = "{human_query}"
        prompt = ChatPromptTemplate.from_messages(
            [("system", system), ("human", human)]
        )
        chain = prompt | self._llm
        result = chain.invoke({"human_query": query, "language": "Python"})
        return result.content


class ChatGenerator:
    def __init__(self, llm):
        self._llm = llm

    def generate_chat(self, query):
        system = CHAT_GENERATOR_SYS_PRT
        human = "{human_query}"
        prompt = ChatPromptTemplate.from_messages(
            [("system", system), ("human", human)]
        )
        chain = prompt | self._llm
        result = chain.invoke({"human_query": query, "language": "Python"})
        return result.content


class CodeGenerator:
    def __init__(self, llm):
        self._llm = llm

    def generate_code(self, current_code, query):
        system = CODE_GENERATOR_SYS_PRT
        human = """
        The following is the current code context:
        {current_code}
        
        Based on the above code, generate only the new code that should be added according to the user's request:
        {human_query}
        """
        prompt = ChatPromptTemplate.from_messages(
            [("system", system), ("human", human)]
        )
        input_data = {
            "current_code": current_code,
            "human_query": query,
            "language": "Python",
        }
        chain = prompt | self._llm
        result = chain.invoke(input_data)
        return result.content


class CodeCompletor:
    def __init__(self, llm):
        self._llm = llm

    def complete_code(self, current_code):

        system = CODE_COMPLETOR_SYS_PRT
        human = """
        The following is the current code context:
        {current_code}
        
        Based on this code, predict the most common code that should be added next. 
        Do not repeat any of the current code.
        """
        prompt = ChatPromptTemplate.from_messages(
            [("system", system), ("human", human)]
        )
        input_data = {"current_code": current_code, "language": "Python"}
        chain = prompt | self._llm
        result = chain.invoke(input_data)
        return result.content
