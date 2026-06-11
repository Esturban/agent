from langchain_community.tools import DuckDuckGoSearchResults
from langchain_core.documents import Document

SAMPLE_DOCS = [
    Document(
        page_content="Python lists are ordered, mutable sequences. Create with: my_list = [1, 2, 3]. Access by index: my_list[0] returns 1. Negative indexing: my_list[-1] returns the last item.",
        metadata={"source": "python-basics"},
    ),
    Document(
        page_content="List methods: append(x) adds to end, extend(iterable) merges lists, pop(i) removes by index, sort() sorts in-place, reverse() flips order, len(list) returns count.",
        metadata={"source": "python-basics"},
    ),
    Document(
        page_content="List comprehensions: squares = [x**2 for x in range(10)]. Filtered: evens = [x for x in range(10) if x % 2 == 0]. Nested: [[i*j for j in range(3)] for i in range(3)].",
        metadata={"source": "python-basics"},
    ),
    Document(
        page_content="Slicing lists: my_list[1:3] returns items at index 1 and 2. my_list[:2] takes the first two. my_list[::2] takes every other item. Slicing always returns a new list.",
        metadata={"source": "python-basics"},
    ),
    Document(
        page_content="Python tuples are immutable sequences: t = (1, 2, 3). Tuple unpacking: a, b, c = (1, 2, 3). Use tuples for fixed data; use lists when mutation is needed.",
        metadata={"source": "python-basics"},
    ),
]

web_search = DuckDuckGoSearchResults(output_format="list", max_results=3)
