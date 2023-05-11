
import streamlit as st
import pandas as pd
import threading
import queue

st.text("hello")

# Function to handle data storage in a background thread
def data_storage_thread(q):
    # Load existing data from the CSV file
    data = load_data()
    
    while True:
        item = q.get()
        if item is None:
            # Save the complete data to the CSV file before exiting
            save_data(data)
            break
        data = data.append(item, ignore_index=True)
        # Perform additional data storage operations here if needed

# Function to load the existing data from the CSV file
def load_data():
    try:
        data = pd.read_csv('user_data.csv')
    except FileNotFoundError:
        data = pd.DataFrame(columns=['First Name', 'Last Name'])
    return data

# Function to save the data to the CSV file
def save_data(data):
    data.to_csv('user_data.csv', index=False)

# Create a queue for data storage
data_queue = queue.Queue()

# Start the background thread for data storage
storage_thread = threading.Thread(target=data_storage_thread, args=(data_queue,))
storage_thread.start()

# Input fields for first name and last name
first_name = st.text_input("First Name")
last_name = st.text_input("Last Name")

# Submit button
if st.button("Submit"):
    # Enqueue the entered data for storage
    data_queue.put({'First Name': first_name, 'Last Name': last_name})
    st.success("Data submitted successfully!")

# Cleanup: Stop the background thread
data_queue.put(None)
storage_thread.join()
# Cleanup: Stop the background thread
data_queue.put(None)
storage_thread.join()
