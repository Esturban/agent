"""Tools for LoRA fine-tuning example — dataset loading, tokenization, param counting, inference."""
import random


PYTHON_QA_EXAMPLES = [
    {"instruction": "How do you reverse a list in Python?", "output": "Use the `reverse()` method in-place or `reversed()` to get an iterator. For a new reversed list, use slicing: `my_list[::-1]`."},
    {"instruction": "What is a list comprehension in Python?", "output": "A concise way to create lists: `[expression for item in iterable if condition]`. Example: `[x**2 for x in range(10) if x % 2 == 0]` creates squares of even numbers."},
    {"instruction": "How do you open and read a file in Python?", "output": "Use the `with open()` context manager: `with open('file.txt', 'r') as f: content = f.read()`. The `with` block ensures the file is properly closed."},
    {"instruction": "What is a dictionary in Python and how do you use it?", "output": "A dictionary stores key-value pairs: `d = {'name': 'Alice', 'age': 30}`. Access values with `d['name']`, add with `d['key'] = value`, and iterate with `d.items()`."},
    {"instruction": "How do you handle exceptions in Python?", "output": "Use try/except blocks: `try: result = 10/0 except ZeroDivisionError: print('Cannot divide by zero') finally: print('Done')`. The `finally` block always runs."},
    {"instruction": "What is the difference between `is` and `==` in Python?", "output": "`==` checks value equality while `is` checks identity (same object in memory). `[1,2] == [1,2]` is True but `[1,2] is [1,2]` is False since they're different objects."},
    {"instruction": "How do you sort a list of dictionaries by a key?", "output": "Use `sorted()` with a key function: `sorted(people, key=lambda x: x['age'])`. For in-place sorting: `people.sort(key=lambda x: x['name'])`. Add `reverse=True` for descending."},
    {"instruction": "What are *args and **kwargs in Python?", "output": "`*args` collects extra positional arguments as a tuple; `**kwargs` collects extra keyword arguments as a dict. Example: `def f(*args, **kwargs): print(args, kwargs)` accepts any combination."},
    {"instruction": "How do you create a class in Python?", "output": "Define with `class MyClass:` and use `__init__` for initialization: `class Dog: def __init__(self, name): self.name = name`. Access attributes with `dog.name`."},
    {"instruction": "How do you use list slicing in Python?", "output": "Slice syntax is `list[start:stop:step]`. `my_list[1:4]` gets indices 1,2,3. `my_list[::2]` gets every other element. `my_list[::-1]` reverses the list."},
    {"instruction": "What is a generator in Python?", "output": "A generator is a function that yields values lazily using `yield`. Example: `def count_up(n): for i in range(n): yield i`. Memory-efficient for large sequences."},
    {"instruction": "How do you use map() and filter() in Python?", "output": "`map(func, iterable)` applies a function to each element; `filter(func, iterable)` keeps elements where func returns True. Example: `list(map(str, [1,2,3]))` returns `['1','2','3']`."},
    {"instruction": "What is a decorator in Python?", "output": "A decorator wraps a function to add behavior. Example: `@my_decorator def hello(): pass` is equivalent to `hello = my_decorator(hello)`. Common uses: logging, timing, authentication."},
    {"instruction": "How do you concatenate strings in Python?", "output": "Use `+` for simple cases: `'Hello' + ' ' + 'World'`. For many strings, `''.join(list_of_strings)` is faster. Use f-strings for formatting: `f'Hello {name}'`."},
    {"instruction": "What is the difference between a list and a tuple in Python?", "output": "Lists are mutable (can be changed), tuples are immutable. Use tuples for fixed data like coordinates `(x, y)` and lists for collections that change. Tuples are slightly faster to iterate."},
    {"instruction": "How do you check if a key exists in a dictionary?", "output": "Use the `in` operator: `if 'key' in my_dict:`. Alternatively, use `my_dict.get('key', default)` which returns None (or a default) if the key doesn't exist, avoiding KeyError."},
    {"instruction": "What is a lambda function in Python?", "output": "An anonymous single-expression function: `square = lambda x: x**2`. Useful with map/filter/sorted: `sorted(data, key=lambda x: x[1])`. For complex logic, use a regular `def` instead."},
    {"instruction": "How do you write a recursive function in Python?", "output": "A function that calls itself: `def factorial(n): return 1 if n <= 1 else n * factorial(n-1)`. Always define a base case to stop recursion. Python default recursion limit is 1000."},
    {"instruction": "What are Python's built-in data structures?", "output": "Python has four main built-ins: `list` (ordered, mutable), `tuple` (ordered, immutable), `dict` (key-value pairs), and `set` (unordered, unique elements). Each has different performance characteristics."},
    {"instruction": "How do you read command-line arguments in Python?", "output": "Use `sys.argv`: `import sys; args = sys.argv[1:]`. For structured parsing, use `argparse`: `parser = argparse.ArgumentParser(); parser.add_argument('--name'); args = parser.parse_args()`."},
    {"instruction": "What is the purpose of __init__.py in Python?", "output": "It marks a directory as a Python package, allowing imports like `from mypackage import module`. In Python 3.3+ it's optional (namespace packages), but it's still used to run initialization code or define `__all__`."},
    {"instruction": "How do you format strings in Python?", "output": "Three main ways: f-strings `f'Hello {name}'` (Python 3.6+, fastest), `.format()` method `'Hello {}'.format(name)`, and `%` operator `'Hello %s' % name`. F-strings are the modern standard."},
    {"instruction": "What is the difference between shallow and deep copy?", "output": "`copy.copy()` creates a shallow copy — new container but same inner objects. `copy.deepcopy()` recursively copies all nested objects. Use deepcopy when you need to modify nested structures independently."},
    {"instruction": "How do you use zip() in Python?", "output": "`zip(a, b)` pairs elements from two iterables: `list(zip([1,2,3], ['a','b','c']))` gives `[(1,'a'),(2,'b'),(3,'c')]`. Stops at the shortest iterable. Unzip with `zip(*pairs)`."},
    {"instruction": "What are context managers in Python?", "output": "Objects that implement `__enter__` and `__exit__` for use with `with` statements. They guarantee cleanup code runs: `with open('file') as f:` always closes the file. Create custom ones with `contextlib.contextmanager`."},
    {"instruction": "How do you use enumerate() in Python?", "output": "`enumerate(iterable)` yields `(index, value)` pairs: `for i, name in enumerate(names): print(i, name)`. Start from a different index: `enumerate(names, start=1)`. Avoids manual counter variables."},
    {"instruction": "What is the global interpreter lock (GIL) in Python?", "output": "The GIL is a mutex that prevents multiple threads from executing Python bytecode simultaneously. It simplifies memory management but limits CPU-bound multi-threading. Use `multiprocessing` for CPU-bound parallelism; threads still work well for I/O-bound tasks."},
    {"instruction": "How do you flatten a nested list in Python?", "output": "For one level deep: `[item for sublist in nested for item in sublist]`. For arbitrary depth: use `itertools.chain.from_iterable()` or a recursive function. Python 3.12+ has no built-in for deep flattening."},
    {"instruction": "What is duck typing in Python?", "output": "If an object has the required methods/attributes, it can be used regardless of its type. `len(obj)` works on any object with `__len__`. Python doesn't check types at compile time — it 'quacks like a duck, it is a duck'."},
    {"instruction": "How do you profile Python code?", "output": "Use `cProfile`: `python -m cProfile script.py`. For line-by-line: `pip install line_profiler` then `@profile` decorator. For memory: `memory_profiler`. Quick timing: `timeit` module or `%timeit` in Jupyter."},
    {"instruction": "What are Python dataclasses?", "output": "`@dataclass` auto-generates `__init__`, `__repr__`, `__eq__` from class fields: `@dataclass class Point: x: float; y: float`. Add `frozen=True` for immutability. Available since Python 3.7 via `from dataclasses import dataclass`."},
    {"instruction": "How do you work with JSON in Python?", "output": "Use the built-in `json` module: `import json`. Parse: `data = json.loads(json_string)` or `json.load(file)`. Serialize: `json.dumps(data)` or `json.dump(data, file)`. Add `indent=2` for pretty printing."},
    {"instruction": "What is the difference between range() and xrange() in Python?", "output": "In Python 3, `range()` already behaves like Python 2's `xrange()` — it's a lazy sequence that generates numbers on demand. Python 3 has no `xrange()`. `range(10**9)` uses almost no memory."},
    {"instruction": "How do you use Python's pathlib module?", "output": "`from pathlib import Path`. Create: `p = Path('/home/user/file.txt')`. Operations: `p.parent`, `p.stem`, `p.suffix`, `p.exists()`, `p.read_text()`, `p.write_text()`. Use `/` operator to join: `Path('/home') / 'user' / 'file.txt'`."},
    {"instruction": "What are Python type hints and how do you use them?", "output": "Type hints annotate function signatures: `def add(a: int, b: int) -> int: return a + b`. They're optional and not enforced at runtime but improve readability and enable static analysis with mypy. Use `from typing import List, Dict, Optional` for complex types."},
]


def load_sample_dataset(n: int = 50) -> list[dict]:
    """
    Return n {instruction, output} pairs from a built-in Python Q&A dataset.
    If n > available examples, samples cycle through with slight variation.
    """
    random.seed(42)
    if n <= len(PYTHON_QA_EXAMPLES):
        return random.sample(PYTHON_QA_EXAMPLES, n)
    # Cycle with variation if n > available
    examples = list(PYTHON_QA_EXAMPLES)
    while len(examples) < n:
        ex = random.choice(PYTHON_QA_EXAMPLES)
        examples.append({
            "instruction": ex["instruction"] + " (explain further)",
            "output": ex["output"],
        })
    return examples[:n]


def tokenize_for_training(
    examples: list[dict],
    tokenizer,
    max_length: int = 256,
):
    """
    Tokenize {instruction, output} pairs as prompt+completion sequences.
    Returns a HuggingFace Dataset ready for Trainer.
    """
    from datasets import Dataset

    texts = [
        f"### Instruction:\n{ex['instruction']}\n\n### Response:\n{ex['output']}"
        for ex in examples
    ]

    def tokenize_fn(batch):
        encoded = tokenizer(
            batch["text"],
            truncation=True,
            max_length=max_length,
            padding="max_length",
        )
        encoded["labels"] = encoded["input_ids"].copy()
        return encoded

    raw_dataset = Dataset.from_dict({"text": texts})
    return raw_dataset.map(tokenize_fn, batched=True, remove_columns=["text"])


def count_trainable_params(model) -> dict:
    """Return trainable_params, total_params, and percentage for a model."""
    trainable = sum(p.numel() for p in model.parameters() if p.requires_grad)
    total = sum(p.numel() for p in model.parameters())
    return {
        "trainable_params": trainable,
        "total_params": total,
        "percentage": 100.0 * trainable / total if total > 0 else 0.0,
    }


def generate_response(model, tokenizer, prompt: str, max_new_tokens: int = 150) -> str:
    """Run single inference and return generated text (prompt stripped)."""
    import torch
    full_prompt = f"### Instruction:\n{prompt}\n\n### Response:\n"
    device = next(model.parameters()).device
    inputs = {name: value.to(device) for name, value in tokenizer(full_prompt, return_tensors="pt").items()}
    input_ids = inputs["input_ids"]
    model.eval()
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=False,
            pad_token_id=tokenizer.eos_token_id,
        )
    generated = outputs[0][input_ids.shape[1]:]
    return tokenizer.decode(generated, skip_special_tokens=True).strip()
