import streamlit as st
import pandas as pd

# Load dataset
@st.cache_data
def load_data():
    data = pd.read_csv('Invistico_Airline.csv')
    
    # Data Cleaning Phase
    st.subheader("Data Cleaning Process")
    
    # 1. Handle missing values: remove rows where 'Arrival Delay in Minutes' is missing
    initial_data_length = len(data)
    data = data.dropna(subset=['Arrival Delay in Minutes'])
    cleaned_data_length = len(data)
    st.write(f"Removed {initial_data_length - cleaned_data_length} rows with missing 'Arrival Delay in Minutes'.")
    
    # 2. Cap extreme outliers for delays
    # Capping values for delays at the 99th percentile to remove extreme values
    cap_departure_delay = data['Departure Delay in Minutes'].quantile(0.99)
    cap_arrival_delay = data['Arrival Delay in Minutes'].quantile(0.99)
    data['Departure Delay in Minutes'] = data['Departure Delay in Minutes'].clip(upper=cap_departure_delay)
    data['Arrival Delay in Minutes'] = data['Arrival Delay in Minutes'].clip(upper=cap_arrival_delay)
    st.write(f"Capped extreme delay values at the 99th percentile:")
    st.write(f"- Max 'Departure Delay' capped at {cap_departure_delay} minutes.")
    st.write(f"- Max 'Arrival Delay' capped at {cap_arrival_delay} minutes.")
    
    # 3. Correct data types for categorical columns
    categorical_columns = ['satisfaction', 'Gender', 'Customer Type', 'Type of Travel', 'Class']
    data[categorical_columns] = data[categorical_columns].astype('category')
    st.write("Converted appropriate columns to 'categorical' data type.")
    
    return data

# Load the cleaned data
data = load_data()

# Title of the application
st.title("Airline Customer Satisfaction Analysis")

# Sidebar filters for interaction
st.sidebar.header("Filter Options")

# Satisfaction Filter
satisfaction_filter = st.sidebar.multiselect("Select Satisfaction Level", data["satisfaction"].unique(), default=data["satisfaction"].unique())

# Gender Filter
gender_filter = st.sidebar.multiselect("Select Gender", data["Gender"].unique(), default=data["Gender"].unique())

# Customer Type Filter
customer_type_filter = st.sidebar.multiselect("Customer Type", data["Customer Type"].unique(), default=data["Customer Type"].unique())

# Class Filter
class_filter = st.sidebar.multiselect("Travel Class", data["Class"].unique(), default=data["Class"].unique())

# Type of Travel Filter
travel_type_filter = st.sidebar.multiselect("Type of Travel", data["Type of Travel"].unique(), default=data["Type of Travel"].unique())

# Age Range Filter
age_range = st.sidebar.slider("Select Age Range", int(data["Age"].min()), int(data["Age"].max()), (20, 60))

# Flight Distance Filter
flight_distance = st.sidebar.slider("Select Flight Distance", int(data["Flight Distance"].min()), int(data["Flight Distance"].max()), (100, 5000))

# Seat Comfort Slider
seat_comfort = st.sidebar.slider("Seat Comfort Rating", int(data["Seat comfort"].min()), int(data["Seat comfort"].max()), (0, 5))

# Filter Data
filtered_data = data[
    (data["satisfaction"].isin(satisfaction_filter)) &
    (data["Gender"].isin(gender_filter)) &
    (data["Customer Type"].isin(customer_type_filter)) &
    (data["Class"].isin(class_filter)) &
    (data["Type of Travel"].isin(travel_type_filter)) &
    (data["Age"].between(age_range[0], age_range[1])) &
    (data["Flight Distance"].between(flight_distance[0], flight_distance[1])) &
    (data["Seat comfort"].between(seat_comfort[0], seat_comfort[1]))
]

# Show filtered data
st.subheader("Filtered Customer Data")
st.write(f"Showing {len(filtered_data)} entries out of {len(data)} total.")
st.dataframe(filtered_data)

# Basic stats based on satisfaction
st.subheader("Customer Satisfaction Statistics")

satisfaction_counts = filtered_data["satisfaction"].value_counts()
st.bar_chart(satisfaction_counts)

# Average ratings for various services
st.subheader("Average Service Ratings for Filtered Data")

avg_ratings = filtered_data[["Seat comfort", "Food and drink", "Inflight wifi service",
                            "Inflight entertainment", "Leg room service", "Cleanliness", "Online boarding"]].mean()
st.bar_chart(avg_ratings)

# Departure and Arrival Delays
st.subheader("Departure and Arrival Delays")

delays = filtered_data[["Departure Delay in Minutes", "Arrival Delay in Minutes"]].mean()
st.write(f"Average Departure Delay: {delays['Departure Delay in Minutes']:.2f} minutes")
st.write(f"Average Arrival Delay: {delays['Arrival Delay in Minutes']:.2f} minutes")
