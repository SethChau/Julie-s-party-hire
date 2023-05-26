import tkinter as tk
from tkinter import ttk

# Initialize an empty dictionary to store the items that are currently out
items_out = {}


# Function to add an item to the list of items that are currently out and update treeview
def add_item():
    # Get the input values from the entry fields
    customer_name = customer_name_entry.get()
    receipt_number = receipt_number_entry.get()
    item_name = item_name_entry.get()
    item_count = item_count_entry.get()

    # Check if any of the fields are empty
    if not customer_name or not receipt_number or not item_name or not item_count:
        status_label.config(text="Please fill in all fields.")
        return

    # Validate the customer name input
    customer_name = customer_name_entry.get()
    if not customer_name.replace(" ", "").isalpha():
        status_label.config(text="Invalid input. Please enter a valid customer name.")
        return

    # Validate the item name input
    item_name = item_name_entry.get()
    if not item_name.replace(" ", "").isalpha():
        status_label.config(text="Invalid input. Please enter a valid item name.")
        return

    # Validate the receipt number input
    if not receipt_number.isdigit():
        status_label.config(text="Invalid input. Receipt number should be a number.")
        return

    # Validate the item count input
    try:
        item_count = int(item_count)
    except ValueError:
        status_label.config(text="Invalid input. Please enter a number between 1 and 500 for item count.")
        return

    if not 1 <= item_count <= 500:
        status_label.config(text="Invalid input. Please enter a number between 1 and 500 for item count.")
        return

    # Convert the receipt number to an integer
    receipt_number = int(receipt_number)

    # Add the item to the items_out dictionary
    items_out[receipt_number] = {'customer_name': customer_name, 'item_name': item_name, 'item_count': item_count}

    # Update the status label
    status_label.config(
        text=f"{item_count} {item_name}(s) added to items out list for {customer_name}. Receipt number is {receipt_number}.")

    # Call the function to update the treeview with the latest data
    update_treeview()
    
    # Function to remove an item from the list of items that are currently out
def return_item():
    # Get the selected item from the combo box
    selected_item = item_combo.get()
    
        # Extract the receipt number from the selected item
    receipt_number_start_index = selected_item.rfind(":") + 2
    receipt_number = int(selected_item[receipt_number_start_index:])


    if receipt_number in items_out:
        item_name = items_out[receipt_number]['item_name']
        customer_name = items_out[receipt_number]['customer_name']
        item_count = items_out[receipt_number]['item_count']
        del items_out[receipt_number]
        status_label.config(
            text=f"{item_count} {item_name}(s) returned by {customer_name}. Receipt number {receipt_number} removed from items out list.")
        update_treeview()
    else:
        status_label.config(text="Selected item not found in item list.")
        
        # Function to update the treeview
def update_treeview():
    # Clear the treeview and combo box
    items_out_treeview.delete(*items_out_treeview.get_children())
    item_combo['values'] = ()

    # Create a list to store the combo box values
    combo_box_values = list(item_combo['values'])
       
    # Populate the treeview and combo box with the updated data
    for receipt_number, item_data in items_out.items():
        customer_name = item_data['customer_name']
        item_name = item_data['item_name']
        item_count = item_data['item_count']
        items_out_treeview.insert("", tk.END, values=(receipt_number, customer_name, item_name, item_count))
        combo_box_values.append(f"{item_name} ({item_count}) - Receipt: {receipt_number}")

    # Update the combo box values
    item_combo['values'] = tuple(combo_box_values)


# Create the GUI window
root = tk.Tk()
root.title("Julie’s Party Hire")

# Create a style for the treeview
style = ttk.Style()
style.theme_use("default")

# Create the treeview
tree_frame = tk.Frame(root)
tree_frame.pack()

tree_scroll = tk.Scrollbar(tree_frame)
tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

items_out_treeview = ttk.Treeview(tree_frame, columns=("receipt_number", "customer_name", "item_name", "item_count"),
                                  show="headings", yscrollcommand=tree_scroll.set)
items_out_treeview.heading("receipt_number", text="Receipt number")
items_out_treeview.heading("customer_name", text="Customer name")
items_out_treeview.heading("item_name", text="Item name")
items_out_treeview.heading("item_count", text="Item count")
items_out_treeview.pack()

tree_scroll.config(command=items_out_treeview.yview)

# Configure the treeview colors
style.configure("Treeview", background="white", foreground="black")  # Set background and foreground colors of the treeview

# Create labels and entry fields
label_frame = tk.Frame(root)
label_frame.pack(pady=10)

customer_name_label = tk.Label(label_frame, text="Customer Name:")
customer_name_label.grid(row=0, column=0, padx=10)
customer_name_entry = tk.Entry(label_frame)
customer_name_entry.grid(row=0, column=1)

receipt_number_label = tk.Label(label_frame, text="Receipt Number:")
receipt_number_label.grid(row=1, column=0, padx=10)
receipt_number_entry = tk.Entry(label_frame)
receipt_number_entry.grid(row=1, column=1)

item_name_label = tk.Label(label_frame, text="Item Name:")
item_name_label.grid(row=2, column=0, padx=10)
item_name_entry = tk.Entry(label_frame)
item_name_entry.grid(row=2, column=1)

item_count_label = tk.Label(label_frame, text="Item Count:")
item_count_label.grid(row=3, column=0, padx=10)
item_count_entry = tk.Entry(label_frame)
item_count_entry.grid(row=3, column=1)

# Create buttons
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

add_button = tk.Button(button_frame, text="Add Item", command=add_item)
add_button.grid(row=0, column=0, padx=10)
return_button = tk.Button(button_frame, text="Return Item", command=return_item)
return_button.grid(row=0, column=1)

# Create a combo box to display the items available for return
combo_frame = tk.Frame(root)
combo_frame.pack(pady=10)

combo_label = tk.Label(combo_frame, text="Select Item to Return:")
combo_label.grid(row=0, column=0, padx=10)
item_combo = ttk.Combobox(combo_frame, state="readonly")
item_combo.grid(row=0, column=1, padx=10)

# Create a label to display the status messages
status_label = tk.Label(root, text="")
status_label.pack(pady=10)

# Start the main event loop
root.mainloop()


