from langchain_core.prompts import ChatPromptTemplate
from ..prompt_template.programing_prompt import CODE_ANALYZER_SYS_PRT
from llm_core.prompt_template.rule_to_xtend_prompt import (
    HEADER_SOURCE_SYS_PRT,
    HEADER_TEMPLATE_SYS_PRT,
    SOURCE_TEMPLATE_SYS_PRT,
    HUMAN_INPUT_SYS_PRT,
    HUMAN_INPUT_HS_PROMPT,
    GENERATOR_SYS_PRT,
    HUMAN_INPUT_G_PROMPT,
    GENERATOR_TEMPLATE_SYS_PRT,
)

from langchain_core.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)


class CodeAnalyzer:
    def __init__(self, llm) -> None:
        self._llm = llm

    def analyze_code(self, query):
        system = CODE_ANALYZER_SYS_PRT
        human = "{human_query}"
        prompt = ChatPromptTemplate.from_messages(
            [("system", system), ("human", human)]
        )
        chain = prompt | self._llm
        result = chain.invoke({"human_query": query, "language": "Xtend"})
        return result.content


class HeaderSourceXtendGenerator:
    def __init__(self, llm) -> None:
        self._llm = llm

        self.prompt_header_gen = ChatPromptTemplate.from_messages(
            [
                SystemMessagePromptTemplate.from_template(
                    template=HEADER_SOURCE_SYS_PRT,
                    partial_variables={
                        "xtend_code_template": HEADER_TEMPLATE_SYS_PRT,
                    },
                ),
                HumanMessagePromptTemplate.from_template(
                    HUMAN_INPUT_HS_PROMPT,
                    partial_variables={
                        "human_input_system_prompt": HUMAN_INPUT_SYS_PRT,
                    },
                ),
            ]
        )
        self.chain_header_gen = self.prompt_header_gen | self._llm

        self.prompt_source_gen = ChatPromptTemplate.from_messages(
            [
                SystemMessagePromptTemplate.from_template(
                    template=HEADER_SOURCE_SYS_PRT,
                    partial_variables={
                        "xtend_code_template": SOURCE_TEMPLATE_SYS_PRT,
                    },
                ),
                HumanMessagePromptTemplate.from_template(
                    HUMAN_INPUT_HS_PROMPT,
                    partial_variables={
                        "human_input_system_prompt": HUMAN_INPUT_SYS_PRT,
                    },
                ),
            ]
        )
        self.chain_source_gen = self.prompt_source_gen | self._llm

        self.prompt_generate_gen = ChatPromptTemplate.from_messages(
            [
                SystemMessagePromptTemplate.from_template(
                    template=GENERATOR_SYS_PRT,
                    partial_variables={},
                ),
                HumanMessagePromptTemplate.from_template(
                    HUMAN_INPUT_G_PROMPT,
                    partial_variables={},
                ),
            ]
        )
        self.chain_generater_gen = self.prompt_generate_gen | self._llm

    def write_header_extend(self, standard_rule: list) -> None:
        result = self.chain_header_gen.invoke({"human_input": standard_rule})
        return result.content

    def write_source_extend(self, standard_rule: list) -> None:
        result = self.chain_source_gen.invoke({"human_input": standard_rule})
        return result.content

    def write_generate_extend(self) -> str:
        # result = self.chain_generater_gen.invoke({"human_input": standard_rule})
        # return result.content
        return GENERATOR_TEMPLATE_SYS_PRT
