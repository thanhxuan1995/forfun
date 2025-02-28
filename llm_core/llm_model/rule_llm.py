from typing import List
from langchain_core.messages import BaseMessage
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from ..prompt_template.standard_rule_prompt import STANDARD_RULE_SYS_PRT


class InMemoryHistory(BaseChatMessageHistory, BaseModel):
    """In memory implementation of chat message history."""

    messages: List[BaseMessage] = Field(default_factory=list)

    def add_messages(self, messages: List[BaseMessage]) -> None:
        """Add a list of messages to the store"""
        self.messages.extend(messages)

    def clear(self) -> None:
        self.messages = []


class ParseRule:
    def __init__(self, llm):
        self.llm = llm
        self.store_gen_excel = {}
        self.prompt_gen_excel = ChatPromptTemplate.from_messages(
            [
                ("system", STANDARD_RULE_SYS_PRT),
                MessagesPlaceholder(variable_name="history"),
                ("human", "{question}"),
            ]
        )

        self.chain_gen_excel = self.prompt_gen_excel | self.llm
        self.chain_gen_excel_with_history = RunnableWithMessageHistory(
            self.chain_gen_excel,
            self.get_standard_rule_by_session_id,
            input_messages_key="question",
            history_messages_key="history",
        )

    def get_standard_rule_by_session_id(
        self, session_id: str
    ) -> BaseChatMessageHistory:
        if session_id not in self.store_gen_excel:
            self.store_gen_excel[session_id] = InMemoryHistory()
        return self.store_gen_excel[session_id]

    def standard_rule(self, input: str):
        self.chain_gen_excel_with_history.invoke(
            {"question": input},
            config={"configurable": {"session_id": "standard_rule"}},
        )
        return self.store_gen_excel["standard_rule"].messages[-1].content
