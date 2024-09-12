import random
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import threading

# Define the success rates for each enhancement level
success_rates = {
    1: 0.76,
    2: 0.50,
    3: 0.40,
    4: 0.30,
    5: 0.12,
    # Add more levels as needed
}

# Fixed downgrade rate for all levels
downgrade_rate = 0.4

# Cron costs for each enhancement level
cron_costs = {
    1: 10,
    2: 20,
    3: 30,
    4: 50,
    5: 100,
    # Add more levels as needed
}

# Default base cost
DEFAULT_BASE_COST = 1000000  # Set your desired default base cost here

def format_cost(cost):
    return "{:,.0f}".format(cost)

def simulate_enhancements(target_level, num_simulations, base_cost, use_crons, results):
    total_cost = 0
    for _ in range(num_simulations):
        current_level = 0
        cost = 0
        while current_level < target_level:
            enhancement_success_rate = success_rates.get(current_level + 1, 0)
            cost += base_cost  # Base cost for enhancing
            
            if random.random() < enhancement_success_rate:
                current_level += 1
            else:
                if use_crons and random.random() >= downgrade_rate:
                    # Check if enough crons are available
                    cron_cost = cron_costs.get(current_level + 1, 0)
                    if cron_cost > 0:
                        cost += cron_cost  # Add cron cost
                else:
                    cost += base_cost  # Add base cost for rebuilding
                    current_level = 0  # Reset to base level upon failure
        
        total_cost += cost
    
    average_cost = total_cost / num_simulations
    results.append(average_cost)

def calculate_average_cost():
    try:
        target_level = int(target_level_entry.get())
        if target_level < 1:
            raise ValueError("Enhancement level must be greater than or equal to 1.")
        
        base_cost = float(base_cost_entry.get() or DEFAULT_BASE_COST)  # Use default if entry is empty
        use_crons = use_crons_checkbox_var.get()
        num_simulations = 100000
        
        # Number of threads to use
        num_threads = 4  # You can adjust this based on your system's capabilities
        
        # Create a list to store the results from each thread
        results = []
        threads = []
        
        # Create and start threads
        for _ in range(num_threads):
            thread = threading.Thread(target=simulate_enhancements, args=(target_level, num_simulations // num_threads, base_cost, use_crons, results))
            thread.start()
            threads.append(thread)
        
        # Wait for all threads to finish
        for thread in threads:
            thread.join()
        
        # Calculate the average cost from the results
        average_cost = sum(results) / num_threads
        
        formatted_cost = format_cost(int(average_cost))
        result_label.config(text=f"Average cost: {formatted_cost} silver")
    except ValueError as e:
        messagebox.showerror("Error", str(e))

def edit_success_rates():
    # Create a dialog to edit success rates
    edit_window = tk.Toplevel(root)
    edit_window.title("Edit Success Rates")

    # Create and pack widgets in the edit window
    edit_label = ttk.Label(edit_window, text="Edit Success Rates:")
    edit_label.pack(padx=10, pady=5)

    # Create an entry for each enhancement level
    entry_labels = []
    for level, rate in success_rates.items():
        label = ttk.Label(edit_window, text=f"Level {level}:")
        label.pack(padx=10, pady=5)
        entry = ttk.Entry(edit_window)
        entry.insert(0, str(rate))
        entry.pack(padx=10, pady=5)
        entry_labels.append((level, entry))

    # Function to update success rates
    def update_success_rates():
        try:
            for level, entry in entry_labels:
                new_rate = float(entry.get())
                if new_rate < 0 or new_rate > 1:
                    raise ValueError("Success rate must be between 0 and 1.")
                success_rates[level] = new_rate
            edit_window.destroy()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    update_button = ttk.Button(edit_window, text="Update", command=update_success_rates)
    update_button.pack(padx=10, pady=10)

def edit_cron_costs():
    # Create a dialog to edit cron costs
    edit_window = tk.Toplevel(root)
    edit_window.title("Edit Cron Costs")

    # Create and pack widgets in the edit window
    edit_label = ttk.Label(edit_window, text="Edit Cron Costs:")
    edit_label.pack(padx=10, pady=5)

    # Create an entry for each enhancement level
    entry_labels = []
    for level, cost in cron_costs.items():
        label = ttk.Label(edit_window, text=f"Level {level}:")
        label.pack(padx=10, pady=5)
        entry = ttk.Entry(edit_window)
        entry.insert(0, str(cost))
        entry.pack(padx=10, pady=5)
        entry_labels.append((level, entry))

    # Function to update cron costs
    def update_cron_costs():
        try:
            for level, entry in entry_labels:
                new_cost = int(entry.get())
                if new_cost < 0:
                    raise ValueError("Cron cost must be a non-negative integer.")
                cron_costs[level] = new_cost
            edit_window.destroy()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    update_button = ttk.Button(edit_window, text="Update", command=update_cron_costs)
    update_button.pack(padx=10, pady=10)

# Create the main window
root = tk.Tk()
root.title("BDO Enhancement Calculator")

# Create and pack widgets
base_cost_label = ttk.Label(root, text="Base Cost:")
base_cost_label.pack(padx=10, pady=5)

base_cost_entry = ttk.Entry(root)
base_cost_entry.insert(0, str(DEFAULT_BASE_COST))  # Set default value
base_cost_entry.pack(padx=10, pady=5)

target_level_label = ttk.Label(root, text="Target Enhancement Level:")
target_level_label.pack(padx=10, pady=5)

target_level_entry = ttk.Entry(root)
target_level_entry.pack(padx=10, pady=5)

use_crons_checkbox_var = tk.BooleanVar()
use_crons_checkbox = ttk.Checkbutton(root, text="Use crons to prevent loss (may affect cost)", variable=use_crons_checkbox_var)
use_crons_checkbox.pack(padx=10, pady=5)

calculate_button = ttk.Button(root, text="Calculate", command=calculate_average_cost)
calculate_button.pack(padx=10, pady=10)

edit_rates_button = ttk.Button(root, text="Edit Success Rates", command=edit_success_rates)
edit_rates_button.pack(padx=10, pady=10)

edit_cron_costs_button = ttk.Button(root, text="Edit Cron Costs", command=edit_cron_costs)
edit_cron_costs_button.pack(padx=10, pady=10)

result_label = ttk.Label(root, text="")
result_label.pack(padx=10, pady=5)

root.mainloop()







