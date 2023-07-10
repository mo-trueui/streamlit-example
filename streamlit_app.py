from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st
from selenium import webdriver
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

"""
# Welcome to Streamlit!

Edit `/streamlit_app.py` to customize this app to your heart's desire :heart:

If you have any questions, checkout our [documentation](https://docs.streamlit.io) and [community
forums](https://discuss.streamlit.io).

In the meantime, below is an example of what you can do with just a few lines of code:
"""

def send_email(email_address, filename):
    from_address = "your_email_address"
    password = "your_password"

    msg = MIMEMultipart()
    msg['From'] = from_address
    msg['To'] = email_address
    msg['Subject'] = "Your Streamlit Chart"

    with open(filename, 'rb') as f:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="chart.png"')
        msg.attach(part)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(from_address, password)
    text = msg.as_string()
    server.sendmail(from_address, email_address, text)
    server.quit()

with st.echo(code_location='below'):
    total_points = st.slider("Number of points in spiral", 1, 5000, 2000)
    num_turns = st.slider("Number of turns in spiral", 1, 100, 9)

    Point = namedtuple('Point', 'x y')
    data = []

    points_per_turn = total_points / num_turns

    for curr_point_num in range(total_points):
        curr_turn, i = divmod(curr_point_num, points_per_turn)
        angle = (curr_turn + 1) * 2 * math.pi * i / points_per_turn
        radius = curr_point_num / total_points
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        data.append(Point(x, y))

    chart = alt.Chart(pd.DataFrame(data), height=500, width=500).mark_circle(color='#0068c9', opacity=0.5).encode(x='x:Q', y='y:Q')
    st.altair_chart(chart)

    email_address = st.text_input("Email address")
    if st.button("Send Email"):
        chart.save('chart.png')
        send_email(email_address, 'chart.png')
