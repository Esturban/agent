import pandas as pd
from pathlib import Path
_repo_root = Path(__file__).parent.parent.parent.parent

from langchain_core.tools import tool

#Load the laptop product pricing CSV into a Pandas dataframe.
product_pricing_df = pd.read_csv(f"{_repo_root}/data/product/Laptop pricing.csv")
product_orders_df = pd.read_csv(f"{_repo_root}/data/product/Laptop Orders.csv")
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

@tool
def get_order_details(order_id:str) -> str :
    """
    This function returns details about a laptop order, given an order ID
    It performs an exact match between the input order id and available order ids
    If a match is found, it returns products (laptops) ordered, quantity ordered and delivery date.
    If there is NO match found, it returns -1
    """
    #Filter Dataframe for order ID
    match_order_df = product_orders_df[
                        product_orders_df["Order ID"] == order_id ]

    #Check if a record was found, if not return -1
    if len(match_order_df) == 0 :
        return -1
    else:
        return match_order_df.iloc[0].to_dict()

#Test the tool. Before running the test, comment the @tool annotation
#print(get_order_details("ORD-6948"))
#print(get_order_details("ORD-9999"))

@tool
def update_quantity(order_id:str, new_quantity:int) -> bool :
    """
    This function updates the quantity of products ( laptops ) ordered for a given order Id.
    It there are no matching orders, it returns False.
    """
    #Find if matching record exists
    match_order_df = product_orders_df[
                        product_orders_df["Order ID"] == order_id ]

    #Check if a record was found, if not return -1
    if len(match_order_df) == 0 :
        return -1
    else:
        product_orders_df.loc[
            product_orders_df["Order ID"] == order_id, 
                "Quantity Ordered"] = new_quantity
        return True
        