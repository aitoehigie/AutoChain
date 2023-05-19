from string import Template
from typing import Any, List

from pydantic import BaseModel, Extra

from minichain.memory.message import BaseMessage, HumanMessage


class JSONPromptTemplate(BaseModel):
    template: Template
    """The prompt template."""

    input_variables: List[str]
    """A list of the names of the variables the prompt template expects."""

    class Config:
        """Configuration for this pydantic object."""
        extra = Extra.forbid
        arbitrary_types_allowed = True

    def format_prompt(self, **kwargs: Any) -> List[BaseMessage]:
        variables = {v: "" for v in self.input_variables}
        variables.update(kwargs)
        prompt = self.template.substitute(**variables)
        return [HumanMessage(content=prompt)]
