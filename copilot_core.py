import os
from langchain_groq import ChatGroq
from dotenv import load_dotenv
load_dotenv()
from ..llm_model.python_llm import (CommentGenerator,
                                    ChatGenerator,
                                    CodeGenerator,
                                    CodeCompletor,
                                    CodeAnalyzer)
# from ..llm_model.xtend_llm import HeaderSourceXtendGenerator

class CopilotCore:
    def __init__(self) -> None:
        self._llm = ChatGroq(
            temperature=os.environ["TEMPERATURE"],
            max_retries=os.environ["MAX_RETRIES"],
            model=os.environ["MODEL"],
            api_key=os.getenv("CHAT_GROP_KEY"),
        )

        self.init_llm()
    def init_llm(self) -> None:
        self.comment_generator_python = CommentGenerator(self._llm)
        self.chatbot_python = ChatGenerator(self._llm)
        self.code_generator_python = CodeGenerator(self._llm)
        self.code_completer_python = CodeCompletor(self._llm)
        self.code_analyzer_xtend = CodeAnalyzer(self._llm)
        ######extend
        #self.generate_xtend = HeaderSourceXtendGenerator(self._llm)
        

    def comment_code(self, query: str) -> str:
        return self.comment_generator_python.generate_comment(query)
    
    def chat_generate(self, query: str) -> str:
        return self.chatbot_python.generate_chat(query)
    
    def generate_code(self, current_code: str, query: str) -> str:
        return self.code_generator_python.generate_code(current_code, query)
    def complete_code(self, query: str) -> str:
        return self.code_completer_python.complete_code(query)
    def analyze_code(self, query: str) -> str:
        return self.code_analyzer_xtend.analyze_code(query)
    
    # ### extend items
    # def generate_header_xtend(self, standard_rule: list) -> str:
    #     return self.generate_xtend.write_header_extend(standard_rule)
    # def generate_source_xtend(self, standard_rule: list) -> str:
    #     return self.generate_xtend.write_source_extend(standard_rule)
    # def generate_generate_xtend(self) -> str:
    #     return self.generate_xtend.write_generate_extend()




