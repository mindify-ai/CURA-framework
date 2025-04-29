import json
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from tqdm import tqdm
from bigcodebench.data import get_bigcodebench
from bigcodebench import evaluate
from .pipeline import Pipeline

def solve_problem(task_id: str, problem: dict, split: str = "complete") -> dict:
    agent = Pipeline()
    prompt = problem.get("complete_prompt") if split == "complete" else problem.get("instruct_prompt", "")
    sol = agent.generate(prompt)
    return {"task_id": task_id, "solution": sol}

def dataset_generation(subset: str = "hard", split: str = "complete", num_workers: int = 8, output_file: str = None):
    problems = get_bigcodebench(subset=subset)
    if not output_file:
        output_file = f"dataset_{subset}_{split}_{int(time.time())}.jsonl"
    with open(output_file, "w") as f, ProcessPoolExecutor(max_workers=num_workers) as pool:
        futures = [pool.submit(solve_problem, tid, prob, split) for tid, prob in problems.items()]
        for fb in tqdm(as_completed(futures), total=len(futures)):
            f.write(json.dumps(fb.result()) + "\n")
    print(f"Saved to {output_file}")

def evaluate_dataset(subset: str = "hard", split: str = "complete"):
    generation_file = f"generation_{int(time.time())}.jsonl"
    dataset_generation(subset, split, output_file=generation_file)
    evaluate(split=split, subset=subset, samples=generation_file, pass_k="1", parallel=64)
