from bigcodebench.eval import untrusted_check

def remove_wrappers(text: str) -> str:
    if "```" in text:
        parts = text.split("```python") if "```python" in text else text.split("```")
        return parts[-1].split("```", 1)[0].strip()
    return text.strip()

def test(code: str, test_code: str):
    clean_code = remove_wrappers(code)
    clean_test = remove_wrappers(test_code)
    return untrusted_check(
        code=clean_code,
        test_code=clean_test,
        entry_point="",
        max_as_limit=30*1024,
        max_data_limit=30*1024,
        max_stack_limit=10
    )
