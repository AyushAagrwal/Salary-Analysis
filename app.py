import streamlit as st
import pandas as pd
from dotenv import load_dotenv
import os
import plotly.express as px
from groq import Groq  # Assuming Groq SDK is installed and available

# Load the data
main_table = pd.read_csv('main_data.csv')
df = pd.read_csv('salaries.csv')

# Streamlit app title
st.title("ML Engineer Salaries Insights 📈 and Chatbot 🤖")

# Display the main table
st.subheader("ML Engineer Salaries Data (2020 - 2024)")
st.dataframe(main_table.style.format({"average_salary": "${:.2f}"}))

# Plotly Line Chart for job count over the years
st.subheader("Job Count Over Time 📊 (2020 - 2024)" )
fig = px.line(main_table, x='work_year', y='total_jobs', markers=True, 
              labels={'work_year': 'Year', 'total_jobs': 'Number of Jobs'},
              title='Total Number of Jobs (2020-2024)')
fig.update_traces(line=dict(color='royalblue', width=3))
st.plotly_chart(fig)

# Step 2: Interactive table - When a row is clicked, show job titles for that year
st.subheader("Select a Year to View Job Titles")

# Create a selectbox for the year selection
selected_year = st.selectbox("Choose a Year", main_table['work_year'])

# Filter the main dataframe based on the selected year
filtered_data = df[df['work_year'] == selected_year]

# Group by job title to count the number of jobs
job_title_table = filtered_data.groupby('job_title').agg(
    number_of_jobs=('job_title', 'count')
).reset_index()

# Sort the table by number_of_jobs in descending order
job_title_table = job_title_table.sort_values(by='number_of_jobs', ascending=False)

# Display the second table when a year is selected
if not filtered_data.empty:
    st.write(f"Job Titles and Counts for {selected_year}")
    st.table(job_title_table)

# Set up the chat app interface
st.subheader("Chat with the ML Salary Insights Bot")

# Input prompt from the user
user_input = st.text_input("Ask a question about the data:")

# Initialize Groq Client with API key from environment variable
client = Groq(api_key="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")
# Load the environment variables from the .env file
# load_dotenv()

# Retrieve the API key from the environment
# api_key = os.getenv("GROQ_API_KEY")

# Initialize the Groq client with the API key
# client = Groq(api_key=api_key)


# Function to query Groq API for chat completion
def query_groq_llm(prompt):
    try:
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama3-8b-8192",  # Using llama3-8b-8192 model as in your example
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"Error: {e}"

# Check if the user entered a query
if user_input:
    with st.spinner('Fetching insights...'):
        # Get the response from Groq API
        response = query_groq_llm(user_input)
        
        # Display the response in the app
        st.write("### Insight:")
        st.write(response)

# Display a few examples to help users
st.subheader("Example questions you can ask:")
st.write("""
- What is the average salary for ML engineers in 2022?
- How many job opportunities were there in 2023?
- What is the trend of ML jobs from 2020 to 2024?
- What job titles were most common in 2021?
- How has the average salary changed over the years?
""")

