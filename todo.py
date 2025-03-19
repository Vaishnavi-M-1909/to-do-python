import streamlit as st
import json
import time
import pytz
from datetime import datetime

# File to save tasks persistently
TASKS_FILE = "tasks.json"

def load_tasks():
    try:
        with open(TASKS_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_tasks(tasks):
    with open(TASKS_FILE, "w") as file:
        json.dump(tasks, file)

def get_ist_time():
    ist = pytz.timezone('Asia/Kolkata')
    return datetime.now(ist).strftime('%I:%M:%S %p')

def main():
    st.set_page_config(page_title="📝 To-Do List", layout="centered")
    
    # Dark Mode Toggle
    if "dark_mode" not in st.session_state:
        st.session_state.dark_mode = False
    
    st.sidebar.title("Settings")
    if st.sidebar.button("🌙 Toggle Dark Mode" if not st.session_state.dark_mode else "☀ Toggle Light Mode"):
        st.session_state.dark_mode = not st.session_state.dark_mode

    # Background color
    bg_color = "#2E3B4E" if st.session_state.dark_mode else "#E6E6FA"
    text_color = "white" if st.session_state.dark_mode else "black"
    st.markdown(f"""
        <style>
            body {{ background-color: {bg_color}; color: {text_color}; }}
        </style>
    """, unsafe_allow_html=True)

    st.title("📝 To-Do List")

    tasks = load_tasks()

    new_task = st.text_input("Add a new task:")
    if st.button("Add Task"):
        if new_task.strip():
            tasks.append({"task": new_task.strip(), "completed": False})
            save_tasks(tasks)
            st.rerun()

    for idx, task in enumerate(tasks):
        col1, col2, col3, col4 = st.columns([0.6, 0.15, 0.15, 0.1])
        with col1:
            if task['completed']:
                st.write(f"✅ {task['task']}")
            else:
                edited_task = st.text_input("", value=task['task'], key=f"edit_{idx}")
                if edited_task != task['task']:
                    tasks[idx]['task'] = edited_task
                    save_tasks(tasks)
                    st.rerun()
        with col2:
            if st.button("✔", key=f"complete_{idx}"):
                tasks[idx]["completed"] = True
                save_tasks(tasks)
                st.rerun()
        with col3:
            if st.button("🗑", key=f"delete_{idx}"):
                tasks.pop(idx)
                save_tasks(tasks)
                st.rerun()
    
    st.write("---")
    st.write(f"Current Time (IST): {get_ist_time()}")

if __name__ == "__main__":
    main()
