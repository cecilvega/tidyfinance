import json
import pandas as pd
import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build
from pathlib import Path


def read_expenses():
    # Set up the service account credentials
    service_account_info = json.loads(st.secrets.service_account_info)

    creds = service_account.Credentials.from_service_account_info(
        service_account_info, scopes=["https://www.googleapis.com/auth/spreadsheets.readonly"]
    )

    # Create a Sheets API client
    sheets_service = build("sheets", "v4", credentials=creds)

    # Specify the file ID of the Google Sheets file you want to read
    file_id = "1WOcaZOyHYGhebc80gsgoLjw4ofabIymCJkq7smgvsH8"

    # Specify the range of cells you want to read (e.g., "Sheet1!A1:C10")
    range_name = "gastos"

    # Make a request to get the values from the specified range
    result = sheets_service.spreadsheets().values().get(spreadsheetId=file_id, range=range_name).execute()

    # Get the values from the result
    data = result.get("values", [])

    # Convert the data to a pandas DataFrame
    df = pd.DataFrame(data[1:], columns=data[0])
    df.columns = df.columns.str.lower()
    df["fecha"] = pd.to_datetime(df["fecha"]).dt.date
    df["monto"] = pd.to_numeric(df["monto"])
    return df


def styler():
    # logo_path = Path("__file__").absolute().parents[1] / "images/komatsu.png"

    hide_streamlit_style = """
            <style>
            footer {visibility: hidden !important;}
            </style>
            """

    st.markdown(hide_streamlit_style, unsafe_allow_html=True)
    # logo = Image.open()
    # st.sidebar.image(logo)
    # Style
    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
