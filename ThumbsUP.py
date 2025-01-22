import streamlit as st
import pandas as pd

# Sample data: List of services and providers with votes
data = {
    'Service': ['Laundry', 'Cooking', 'Cleaning', 'Gardening'],
    'Provider': ['Alice', 'Bob', 'Charlie', 'David'],
    'Thumbs_Up': [10, 15, 5, 8],
    'Thumbs_Down': [2, 1, 3, 0]
}

# Create a DataFrame
df = pd.DataFrame(data)

# Function to calculate the net thumbs up score
def calculate_score(row):
    return row['Thumbs_Up'] - row['Thumbs_Down']

# Calculate scores for each service
df['Score'] = df.apply(calculate_score, axis=1)

# Sort DataFrame by Score in descending order
sorted_df = df.sort_values(by='Score', ascending=False)

# Streamlit app layout
st.title("Service Provider Ratings")

st.write("### Sorted Services by Thumbs Up Votes")
st.dataframe(sorted_df[['Service', 'Provider', 'Thumbs_Up', 'Thumbs_Down', 'Score']])

# Optionally, you can add more interactivity here
selected_service = st.selectbox("Select a Service", sorted_df['Service'])
service_info = sorted_df[sorted_df['Service'] == selected_service]

if not service_info.empty:
    st.write(f"**Provider:** {service_info['Provider'].values[0]}")
    st.write(f"**Thumbs Up:** {service_info['Thumbs_Up'].values[0]}")
    st.write(f"**Thumbs Down:** {service_info['Thumbs_Down'].values[0]}")
    st.write(f"**Score:** {service_info['Score'].values[0]}")

