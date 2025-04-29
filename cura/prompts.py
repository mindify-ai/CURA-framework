# Prompt templates for various pipeline stages
TASK_UNDERSTAND_PROMPT = '''\
Identity: You are an expert AI assistant specializing in programmatic reasoning.
Task: {task}
Return JSON: {{"task_understanding":"<analysis>"}}
'''

TEST_CASE_PROMPT = '''\
Identity: You are an expert AI assistant generating unittest code.
Task: {task}
Understanding: {task_understanding}
Return JSON: {{"test_code":"<code>"}}
'''

CODE_SOLVER_PROMPT = '''\
Identity: You are an expert AI assistant that writes Python functions passing given tests.
Task: {task}
Understanding: {task_understanding}
Tests: {test_code}
Return JSON: {{"generated_code":"<code>"}}
'''