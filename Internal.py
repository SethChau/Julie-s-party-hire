import tkinter as tk
from tkinter import ttk

# Initialize an empty dictionary to store the items that are currently out
items_out = {}


# Function to add an item to the list of items that are currently out and update treeview
def add_item():
    customer_name = customer_name_entry.get()
    receipt_number = receipt_number_entry.get()
    item_name = item_name_entry.get()
    item_count = item_count_entry.get()

    if not customer_name or not receipt_number or not item_name or not item_count:
        status_label.config(text="Please fill in all fields.")
        return

    customer_name = customer_name_entry.get()
    if not customer_name.isalpha():
        status_label.config(text="Invalid input. Please enter a valid customer name.")
        return

    item_name = item_name_entry.get()
    if not item_name.isalpha():
        status_label.config(text="Invalid input. Please enter a valid item name.")
        return

    if not receipt_number.isdigit():
        status_label.config(text="Invalid input. Receipt number should be an number.")
        return

    try:
        item_count = int(item_count)
    except ValueError:
        status_label.config(text="Invalid input. Please enter a number between 1 and 500 for item count.")
        return

    if not 1 <= item_count <= 500:
        status_label.config(text="Invalid input. Please enter a number between 1 and 500 for item count.")
        return

    receipt_number = int(receipt_number)
    items_out[receipt_number] = {'customer_name': customer_name, 'item_name': item_name, 'item_count': item_count}
    status_label.config(
        text=f"{item_count} {item_name}(s) added to items out list for {customer_name}. Receipt number is {receipt_number}.")
    update_treeviews()
