import streamlit as st
import pandas as pd
import openai
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json

# Load OpenAI key
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Load Google Sheet
def load_sheet():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds_json = json.loads(st.secrets["GCP_CREDENTIALS_JSON"])
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_json, scope)
    client = gspread.authorize(creds)
    sheet = client.open("Customer_Journeys").sheet1
    return pd.DataFrame(sheet.get_all_records())

# Ask GPT
def ask_bot(question, df):
    prompt = f"""Here is customer journey data:\n{df.head(100).to_csv(index=False)}\n\nAnswer this: {question}"""
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

# UI
st.title("🧠 Customer Journey Bot")

try:
    df = load_sheet()
    st.success("✅ Google Sheet loaded")
    st.dataframe(df.head())
except Exception as e:
    st.error(f"❌ Failed to load sheet: {e}")
    st.stop()

question = st.text_input("Ask about your deals:")
if st.button("Ask GPT") and question:
    with st.spinner("Analyzing..."):
        st.write(ask_bot(question, df))
