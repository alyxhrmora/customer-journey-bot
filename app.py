import streamlit as st
import pandas as pd
import openai

# Load OpenAI key
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Ask GPT
def ask_bot(question, df):
    prompt = f"""You are a helpful assistant. Use the following customer journey data to answer this question:\n\n{df.head(100).to_csv(index=False)}\n\nQuestion: {question}"""
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

# UI
st.title("🧠 Customer Journey Bot (CSV Version)")
uploaded_file = st.file_uploader("📁 Upload your customer journey CSV file")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.success("✅ File uploaded!")
    st.dataframe(df.head())

    question = st.text_input("Ask a question about your customer journeys:")
    if st.button("Ask GPT") and question:
        with st.spinner("Analyzing..."):
            st.write(ask_bot(question, df))
