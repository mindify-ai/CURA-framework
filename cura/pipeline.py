from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from pydantic import BaseModel
from .agent import Agent
from .base_agent import BaseAgent
from .prompts import TASK_UNDERSTAND_PROMPT, TEST_CASE_PROMPT, CODE_SOLVER_PROMPT
from .utils import test

class Pipeline(BaseAgent):
    class State(TypedDict):
        task: str
        task_understanding: str
        test_code: str
        generated_code: str
        test_result: str

    def __init__(self, model="openrouter/gpt-4o-mini"):
        self.solver = Agent(
            name="CURA-Solver", description="Generates tests and code", tools=[], model=model
        )
        builder = StateGraph(Pipeline.State)

        def understand(s: Pipeline.State):
            prompt = TASK_UNDERSTAND_PROMPT.format(task=s["task"])
            out = self.solver.run(prompt)
            s["task_understanding"] = BaseModel.parse_raw(out).task_understanding
            return s

        def gen_tests(s: Pipeline.State):
            prompt = TEST_CASE_PROMPT.format(
                task=s["task"], task_understanding=s["task_understanding"]
            )
            out = self.solver.run(prompt)
            s["test_code"] = BaseModel.parse_raw(out).test_code
            return s

        def solve(s: Pipeline.State):
            prompt = CODE_SOLVER_PROMPT.format(
                task=s["task"], task_understanding=s["task_understanding"], test_code=s["test_code"]
            )
            out = self.solver.run(prompt)
            s["generated_code"] = BaseModel.parse_raw(out).generated_code
            stat, _ = test(s["generated_code"], s["test_code"])
            s["test_result"] = stat
            return s

        builder.add_node(understand)
        builder.add_node(gen_tests)
        builder.add_node(solve)
        builder.add_edge(START, "understand")
        builder.add_edge("understand", "gen_tests")
        builder.add_edge("gen_tests", "solve")
        builder.add_edge("solve", END)

        self.graph = builder.compile()

    def generate(self, task: str) -> str:
        state = {"task": task, "task_understanding": "", "test_code": "", "generated_code": "", "test_result": ""}
        result = self.graph.invoke(state)
        return result["generated_code"]
