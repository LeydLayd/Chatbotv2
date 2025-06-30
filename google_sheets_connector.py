# archivo: google_sheets_connector.py
# autor: robles garcia diego
# descripcion: conexion de lina a google shets
# version : 1.0

import gspread
import streamlit as st
from google.oauth2.service_account import Credentials

class GoogleSheetsConnector:
    def __init__(self, sheet_name: str):
        scopes = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'
        ]
        info = st.secrets["gcp_service_account"]
        creds = Credentials.from_service_account_info(info, scopes=scopes)
        self.client = gspread.authorize(creds)
        self.sheet = self.client.open(sheet_name).sheet1

    def guardar_fila(self, datos: dict):
        encabezados = self.sheet.row_values(1)
        fila = [datos.get(col, "") for col in encabezados]
        self.sheet.append_row(fila, value_input_option="USER_ENTERED")

