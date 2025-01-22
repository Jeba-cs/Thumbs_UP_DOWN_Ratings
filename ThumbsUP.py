import streamlit as st
import pandas as pd

# Streamlit app layout
st.title("Service Provider Ratings")

# Option to choose between sample data or file upload
data_source = st.radio("Select Data Source", options=["Sample Data", "Upload File"])

if data_source == "Sample Data":
    # Sample data: List of services and providers with votes
    data = {
        'Service': ['Laundry', 'Cooking', 'Cleaning', 'Gardening'],
        'Provider': ['Alice', 'Bob', 'Charlie', 'David'],
        'Thumbs_Up': [10, 15, 5, 8],
        'Thumbs_Down': [2, 1, 3, 0]
    }
    df = pd.DataFrame(data)
    st.write("### Using Sample Data:")
    st.dataframe(df)

else:
    # File uploader for CSV or Excel files
    uploaded_file = st.file_uploader("Choose a CSV or Excel file", type=['csv', 'xlsx'])

    if uploaded_file is not None:
        # Determine file type and read the data
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith('.xlsx'):
            df = pd.read_excel(uploaded_file)

        # Display the uploaded DataFrame
        st.write("### Uploaded Data:")
        st.dataframe(df)

# Check if necessary columns exist
if 'df' in locals() and all(col in df.columns for col in ['Service', 'Provider', 'Thumbs_Up', 'Thumbs_Down']):
    # Function to calculate rating out of 5
    def calculate_rating(row):
        total_votes = row['Thumbs_Up'] + row['Thumbs_Down']
        if total_votes == 0:
            return 0.0  # Avoid division by zero
        return round((row['Thumbs_Up'] / total_votes) * 5, 2)

    # Calculate ratings for each service
    df['Rating'] = df.apply(calculate_rating, axis=1)

    # Sort DataFrame by Rating in descending order
    sorted_df = df.sort_values(by='Rating', ascending=False)

    # Display sorted DataFrame
    st.write("### Sorted Services by Ratings")
    st.dataframe(sorted_df[['Service', 'Provider', 'Thumbs_Up', 'Thumbs_Down', 'Rating']])

    # Optionally, allow selection of a service for more details
    selected_service = st.selectbox("Select a Service", sorted_df['Service'])
    service_info = sorted_df[sorted_df['Service'] == selected_service]

    if not service_info.empty:
        st.write(f"**Provider:** {service_info['Provider'].values[0]}")
        st.write(f"**Thumbs Up:** {service_info['Thumbs_Up'].values[0]}")
        st.write(f"**Thumbs Down:** {service_info['Thumbs_Down'].values[0]}")
        st.write(f"**Rating:** {service_info['Rating'].values[0]} / 5")
else:
    if data_source == "Upload File":
        st.error("Uploaded file must contain the following columns: Service, Provider, Thumbs_Up, Thumbs_Down.")

