import streamlit as st
import pandas as pd
import datetime
import numpy as np
import json
from os.path import join
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pytz
import re

# Authenticate
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(
    st.secrets["gspread_service_account"], scopes=scope
)
client = gspread.authorize(creds)

# Open the sheet
sheet = client.open("unfc-python-spring-attendance").sheet1  # or by title

st.set_page_config(page_title='UNFC Attendance (CPSC-610-5)',page_icon=':raised_hand:',layout='wide')

st.markdown('''
        1. Select your name in the list.
        2. Select the card given to you.
        3. Click submit.
            '''
            )

suit_options = ['♦️','♣️','♥️','♠️']
rank_options = ['2','3','4','5','6','7','8','9','10','J','Q','K','A']

suit_image_map = dict(zip(suit_options,['diamonds','clubs','hearts','spades']))
rank_image_map = dict(zip(rank_options,['2','3','4','5','6','7','8','9','10','jack','queen','king','ace']))
suit_map = dict(zip(suit_options,['d','c','h','s']))

cols = st.columns(3)
with cols[0]:
    student_id = st.text_input('Enter your student ID (7 digit number):')
with cols[1]:
    suit = st.selectbox('Select the suit on your card:',options=suit_options)
with cols[2]:
    rank = st.selectbox('Select the number (or letter) on your card:',options=rank_options)

eastern_tz = pytz.timezone("US/Eastern")

match = re.search(r"\d{7}", student_id)
if match:
    student_id = match.group()
else:
    student_id = ''
student_name = st.secrets["students"].get(student_id, "Unknown ID")

if rank in 'JQKA':
    card_image_name = f"{rank_image_map[rank]}_of_{suit_image_map[suit]}2.png"    
else:
    card_image_name = f"{rank_image_map[rank]}_of_{suit_image_map[suit]}.png"
st.image(join('card_images',card_image_name),width=100)

if student_name != "Unknown ID":
    container = st.container(border=True)
    container.markdown(f'Student found :heavy_check_mark:')
    container.write(f'{student_name}')
    button = st.button('Submit')
else:
    container = st.container(border=True)
    container.markdown(f'Student not found :x:')
    button = st.button('Submit',disabled=True)


if button:
    now = datetime.datetime.now(eastern_tz).strftime("%Y-%m-%d %H:%M:%S")
    sheet.append_row([
        now,
        student_name,
        suit_map[suit],
        rank
    ])