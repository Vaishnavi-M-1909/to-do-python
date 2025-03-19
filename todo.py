
import streamlit as st
import json
import time
import threading

# File to save tasks persistently
TASKS_FILE = "tasks.json"

dark_mode = False  # Initialize dark mode variable

# Load saved tasks
def load_tasks():
    try:
        with open(TASKS_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

# Save tasks to file
def save_tasks():
    tasks = [(task_list.get(idx), task_list.itemcget(idx, "fg")) for idx in range(task_list.size())]
    with open(TASKS_FILE, "w") as file:
        json.dump(tasks, file)

# Add a new task
def add_task():
    task = task_input.get().strip()
    if task:
        task_list.insert(tk.END, task)
        save_tasks()
        task_input.delete(0, tk.END)
    else:
        messagebox.showwarning("Warning", "Task cannot be empty!")

# Mark task as complete
def complete_task():
    selected = task_list.curselection()
    if selected:
        idx = selected[0]
        task_list.itemconfig(idx, {'fg': 'gray'})
        save_tasks()

# Edit an existing task
def edit_task():
    selected = task_list.curselection()
    if selected:
        idx = selected[0]
        old_task = task_list.get(idx)
        new_task = simpledialog.askstring("Edit Task", "Modify task:", initialvalue=old_task)
        if new_task:
            task_list.delete(idx)
            task_list.insert(idx, new_task)
            save_tasks()

# Delete a task
def delete_task():
    selected = task_list.curselection()
    if selected:
        task_list.delete(selected[0])
        save_tasks()

# Move task up
def move_up():
    selected = task_list.curselection()
    if selected and selected[0] > 0:
        idx = selected[0]
        task = task_list.get(idx)
        task_list.delete(idx)
        task_list.insert(idx - 1, task)
        task_list.selection_set(idx - 1)
        save_tasks()

# Move task down
def move_down():
    selected = task_list.curselection()
    if selected and selected[0] < task_list.size() - 1:
        idx = selected[0]
        task = task_list.get(idx)
        task_list.delete(idx)
        task_list.insert(idx + 1, task)
        task_list.selection_set(idx + 1)
        save_tasks()

# Toggle light/dark mode
def toggle_theme():
    global dark_mode
    dark_mode = not dark_mode
    bg_color = "#E6E6FA" if not dark_mode else "#2E3B4E"
    text_color = "black" if not dark_mode else "white"
    root.configure(bg=bg_color)
    task_list.configure(bg=bg_color, fg=text_color)
    task_input.configure(bg=bg_color, fg=text_color)
    theme_button.configure(text="☀" if dark_mode else "🌙")

# Live clock updater
def update_clock():
    while True:
        current_time.set(time.strftime('%I:%M:%S %p'))
        time.sleep(1)

# Initialize main window
root.title("📝 To-Do List")
root.geometry("400x500")
root.configure(bg="#E6E6FA")

# Task Input
task_input = tk.Entry(root, width=40, bg="#E6E6FA", fg="black")
task_input.pack(pady=10)

# Buttons
button_frame = tk.Frame(root, bg="#E6E6FA")
button_frame.pack()

tk.Button(button_frame, text="Add", command=add_task).pack(side=tk.LEFT)
tk.Button(button_frame, text="Edit", command=edit_task).pack(side=tk.LEFT)
tk.Button(button_frame, text="Delete", command=delete_task).pack(side=tk.LEFT)
tk.Button(button_frame, text="Complete", command=complete_task).pack(side=tk.LEFT)

task_list = tk.Listbox(root, width=50, height=15, selectmode=tk.SINGLE, bg="#E6E6FA", fg="black")
task_list.pack(pady=10)

tk.Button(root, text="Up", command=move_up).pack(side=tk.LEFT, padx=5)
tk.Button(root, text="Down", command=move_down).pack(side=tk.LEFT, padx=5)

theme_button = tk.Button(root, text="🌙", command=toggle_theme)
theme_button.pack()

# Clock
current_time = tk.StringVar()
tk.Label(root, textvariable=current_time, font=("Arial", 14), bg="#E6E6FA").pack()
clock_thread = threading.Thread(target=update_clock, daemon=True)
clock_thread.start()

# Load tasks
for task, color in load_tasks():
    idx = task_list.size()
    task_list.insert(tk.END, task)
    task_list.itemconfig(idx, {'fg': color})

# Run the application
root.mainloop()
