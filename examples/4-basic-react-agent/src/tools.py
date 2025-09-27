from langchain_core.tools import tool
import pandas as pd
from pathlib import Path
_repo_root = Path(__file__).parent.parent.parent.parent

#Tool annotation identifies a function as a tool automatically
@tool
def find_sum(x:int, y:int) -> int :
    #The docstring comment describes the capabilities of the function
    #It is used by the agent to discover the function's inputs, outputs and capabilities
    """
    This function is used to add two numbers and return their sum.
    It takes two integers as inputs and returns an integer as output.
    """
    return x + y

@tool
def find_product(x:int, y:int) -> int :
    """
    This function is used to multiply two numbers and return their product.
    It takes two integers as inputs and returns an integer as ouput.
    """
    return x * y

#Load the laptop product pricing CSV into a Pandas dataframe.
product_pricing_df = pd.read_csv(f"{_repo_root}/data/product/Laptop pricing.csv")
#print(product_pricing_df)

@tool
def get_laptop_price(laptop_name:str) -> int :
    """
    This function returns the price of a laptop, given its name as input.
    It performs a substring match between the input name and the laptop name.
    If a match is found, it returns the pricxe of the laptop.
    If there is NO match found, it returns -1
    """

    #Filter Dataframe for matching names
    match_records_df = product_pricing_df[
                        product_pricing_df["Name"].str.contains(
                                                "^" + laptop_name, case=False)
                        ]
    #Check if a record was found, if not return -1
    if len(match_records_df) == 0 :
        return -1
    else:
        return match_records_df["Price"].iloc[0]