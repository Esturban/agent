MAX_ITERATIONS = 3

SAMPLE_CSV = """\
product,category,price,units_sold,region
Laptop Pro,Electronics,1299.99,450,North
Wireless Mouse,Electronics,29.99,2100,North
Office Chair,Furniture,349.99,820,South
Standing Desk,Furniture,599.99,340,South
Notebook,Stationery,4.99,5500,East
Pen Pack,Stationery,9.99,3200,East
Coffee Maker,Appliances,89.99,670,West
Blender Pro,Appliances,149.99,290,West
Monitor 27in,Electronics,399.99,610,North
Desk Lamp,Furniture,49.99,1450,South
"""

SAMPLE_QUESTIONS = [
    "Which product has the highest total revenue (price * units_sold)?",
    "What is the average price of Electronics products?",
    "How many units were sold in the North region in total?",
]

QUERY_PROMPT = """\
You have a pandas DataFrame named `df` with these columns: {columns}
Sample rows:
{sample}

Write a single Python expression (no print, no assignment) that answers:
{question}

The expression must evaluate to a scalar value or a short string.
Return only the expression, nothing else.\
"""
