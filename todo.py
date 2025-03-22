import streamlit as st
import json
import os

# File to store tasks
task_file = "tasks.json"

def load_tasks():
    if os.path.exists(task_file):
        with open(task_file, "r") as f:
            return json.load(f)
    return []

def save_tasks(tasks):
    with open(task_file, "w") as f:
        json.dump(tasks, f)

def main():
    st.set_page_config(page_title="Advanced To-Do List", layout="centered")
    
    if "tasks" not in st.session_state:
        st.session_state.tasks = load_tasks()
    
    if "theme" not in st.session_state:
        st.session_state.theme = "light"
    
    # Dark/Light Mode Toggle
    st.sidebar.title("Settings")
    theme_option = st.sidebar.radio("Choose Theme", ["Light", "Dark"], index=0 if st.session_state.theme == "light" else 1)
    st.session_state.theme = "light" if theme_option == "Light" else "dark"
    
    # Apply Theme
    if st.session_state.theme == "dark":
        dark_css = """
        <style>
        body { background-color: #1e1e1e; color: white; }
        .stApp { background-color: #1e1e1e; }
        </style>
        """
        st.markdown(dark_css, unsafe_allow_html=True)
    
    st.sidebar.markdown("---")
    st.sidebar.write(f"Current Theme: {st.session_state.theme.capitalize()}")
    
    st.title("📝 Advanced To-Do List")
    
    # Input new task
    new_task = st.text_input("Add a new task:")
    if st.button("➕ Add Task"):
        if new_task:
            st.session_state.tasks.append({"task": new_task, "done": False})
            save_tasks(st.session_state.tasks)
            st.rerun()
    
    st.markdown("### Tasks")
    
    for i, task in enumerate(st.session_state.tasks):
        col1, col2, col3, col4 = st.columns([0.6, 0.1, 0.1, 0.1])
        with col1:
            st.write("✅" if task["done"] else "🔲", task["task"])
        
        with col2:
            if st.button("✔️", key=f"done_{i}"):
                st.session_state.tasks[i]["done"] = True
                save_tasks(st.session_state.tasks)
                st.rerun()
        
        with col3:
            if not task["done"]:
                new_text = st.text_input("Edit task", value=task["task"], key=f"edit_input_{i}")
                if st.button("Save", key=f"save_{i}"):
                    st.session_state.tasks[i]["task"] = new_text
                    save_tasks(st.session_state.tasks)
                    st.rerun()
        
        with col4:
            if st.button("❌", key=f"delete_{i}"):
                st.session_state.tasks.pop(i)
                save_tasks(st.session_state.tasks)
                st.rerun()
    
    # Filtering tasks
    st.markdown("---")
    filter_option = st.radio("Filter tasks", ["All", "Completed", "Pending"])
    
    filtered_tasks = [
        task for task in st.session_state.tasks 
        if (filter_option == "All") or (filter_option == "Completed" and task["done"]) or (filter_option == "Pending" and not task["done"])
    ]
    
    st.markdown(f"### Showing {filter_option} Tasks")
    for task in filtered_tasks:
        st.write("✅" if task["done"] else "🔲", task["task"])
    
if __name__ == "__main__":
    main()
