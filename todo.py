import streamlit as st
import json
import time

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

def main():
    st.set_page_config(page_title="📝 To-Do List", layout="centered")
    st.title("📝 To-Do List")
    st.markdown("<style>body { background-color: #E6E6FA; }</style>", unsafe_allow_html=True)

    tasks = load_tasks()

    new_task = st.text_input("Add a new task:")
    if st.button("Add Task"):
        if new_task.strip():
            tasks.append({"task": new_task.strip(), "completed": False})
            save_tasks(tasks)
            st.experimental_rerun()

    for idx, task in enumerate(tasks):
        col1, col2, col3 = st.columns([0.7, 0.15, 0.15])
        with col1:
            st.write(f"{'✅' if task['completed'] else '❌'} {task['task']}")
        with col2:
            if st.button("✔", key=f"complete_{idx}"):
                tasks[idx]["completed"] = not tasks[idx]["completed"]
                save_tasks(tasks)
                st.experimental_rerun()
        with col3:
            if st.button("🗑", key=f"delete_{idx}"):
                tasks.pop(idx)
                save_tasks(tasks)
                st.experimental_rerun()

    st.write("---")
    st.write(f"Current Time: {time.strftime('%I:%M:%S %p')}")

if __name__ == "__main__":
    main()
