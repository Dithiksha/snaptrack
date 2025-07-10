import streamlit as st
import json
from datetime import date

FILENAME = "skills.json"

def load_data():
    try:
        with open(FILENAME, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_data(data):
    with open(FILENAME, "w") as f:
        json.dump(data, f, indent=4)

def add_entry(skills, note):
    today = date.today().isoformat()
    data = load_data()
    data.append({"date": today, "skills": skills, "note": note})
    save_data(data)

def delete_entry(index):
    data = load_data()
    if 0 <= index < len(data):
        removed = data.pop(index)
        save_data(data)
        return removed
    return None

# 🌟 UI Starts Here
st.title("📘 SkillSnap-Pro: Track Your Growth")

# Section to add new skill entry
st.header("➕ Add New Skill Entry")
skills = st.text_input("🧠 What skill(s) did you practice today?")
note = st.text_area("📝 Add a short note (optional):")

if st.button("✅ Save Entry"):
    if skills:
        add_entry(skills, note)
        st.success("Entry added successfully!")
        st.rerun()
    else:
        st.warning("Please enter at least one skill.")

# View all entries
st.header("📚 Your Skill Entries")
data = load_data()
if not data:
    st.info("No entries yet!")
else:
    for idx, entry in enumerate(data):
        with st.expander(f"📅 {entry['date']} - 🧠 {entry['skills']}"):
            st.markdown(f"📝 **Note:** {entry['note'] or 'No note provided'}")
            if st.button(f"🗑️ Delete Entry #{idx + 1}", key=idx):
                deleted = delete_entry(idx)
                if deleted:
                    st.success(f"Deleted entry: {deleted['skills']}")
                    st.rerun()
