import xml.etree.ElementTree as ET
from datetime import datetime
import streamlit as st

uploaded_file = st.file_uploader("Choose a GPX file", type="gpx")

if uploaded_file is not None:
    # Load the GPX file
    tree = ET.parse(uploaded_file)
    root = tree.getroot()

    # Create a dictionary to store the waypoints by date and time
    waypoints_by_date = {}

    # Iterate over the waypoints
    for wpt in root.findall('.//wpt'):
        time_str = wpt.find('time').text
        dt = datetime.strptime(time_str, '%Y-%m-%dT%H:%M:%SZ')
        date_str = dt.strftime('%Y-%m-%d')
        time_str = dt.strftime('%H')
        if date_str not in waypoints_by_date:
            waypoints_by_date[date_str] = {}
        if time_str not in waypoints_by_date[date_str]:
            waypoints_by_date[date_str][time_str] = []
        waypoints_by_date[date_str][time_str].append(wpt)

    # Create a separate GPX file for each date and time
    for date_str, time_dict in waypoints_by_date.items():
        for time_str, waypoints in time_dict.items():
            filename = f'{date_str}_{time_str}h.gpx'
            with open(filename, 'w') as f:
                f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
                f.write('<gpx version="1.1">\n')
                f.write(f'  <metadata><name>{date_str} {time_str}h</name></metadata>\n')
                for wpt in waypoints:
                    f.write(ET.tostring(wpt, encoding='unicode').strip() + '\n')
                f.write('</gpx>\n')

    # Display a message to indicate that the files have been created
    st.success("GPX files have been created successfully!")
