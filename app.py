# app.py
import streamlit as st
import pandas as pd
import plotly.express as px

def load_data(file_paths):
    # Read data from Excel file
    data = pd.DataFrame()
    for file_path in file_paths:
        df = pd.read_excel(file_path, header=None, names=['timestamp', 'name', 'empty', 'value'])
        df = df.drop('empty', axis=1)
        data = pd.concat([data, df], ignore_index=True)

    # Convert timestamp to datetime
    data['timestamp'] = pd.to_datetime(data['timestamp'])

    # Drop all rows with name "gebyr
    data = data[data['name'] != 'Gebyr']

    return data

def calculate_sum_by_name(data):
    # Group by 'name' and calculate the sum of 'value' for each group
    sum_by_name = data.groupby('name')['value'].sum().reset_index()
    sum_by_name.columns = ['name', 'total_value']
    # Sort by 'total_value' in descending order
    sum_by_name = sum_by_name.sort_values(by='total_value', ascending=False)
    return sum_by_name

def main():
    st.title("GAHK FEST APPEN")

    # Load data
    file_paths = ["131120231111SA.xlsx", "131120233469RL.xlsx"]
    data = load_data(file_paths)
    # Calculate sum of values by name
    sum_by_name = calculate_sum_by_name(data)

    # Display raw data
    # st.subheader("Raw Data")
    # st.write(data)

    # Filtering by name
    selected_name = st.text_input("Filtrer efter navn, husk at skrive hele dit navn:", "")
    filtered_data = data[data['name'].str.contains(selected_name, case=False, na=False)]

    # Display summary statistics for the selected person
    if selected_name:
        st.subheader(f"Summary for {selected_name}")
        selected_data = data[data['name'] == selected_name]
        total_value = selected_data['value'].sum()
        frequency = selected_data.shape[0]

        st.write(f"Brugt i baren: {total_value} DKK")
        st.write(f"Antal gange i baren: {frequency} gange")

    # Display filtered data
    st.subheader("Filtreret Data")
    st.write(filtered_data)

    # Display total sum by name
    st.subheader("Total brugt i baren")
    st.write(sum_by_name)

    # Plot bar chart with Plotly
    st.subheader("Bar Chart - Chart over Baren")
    fig = px.bar(sum_by_name, x='name', y='total_value', labels={'total_value': 'Total Value'})
    st.plotly_chart(fig)

    

if __name__ == "__main__":
    main()