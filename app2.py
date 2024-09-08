import xml.etree.ElementTree as ET
from datetime import datetime
import streamlit as st
import io
import zipfile

# Set the language to French
st.set_page_config(page_title="Découpe horaire de fichiers Mothy", layout="wide", initial_sidebar_state="expanded")

# Add a title to the app
st.title("Découpe horaire de fichiers Mothy")

# Add a logo to the app
st.image("logo.png", width=200)

# Add a file uploader widget to allow the user to upload the GPX file
uploaded_file = st.file_uploader("Insérez le fichier gpx créé par Mothy pour le découper heure par heure", type="gpx")

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

    # Create a ZIP archive to store the GPX files
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, mode='w', compression=zipfile.ZIP_DEFLATED) as zipf:
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

                # Add the file to the ZIP archive
                with open(filename, 'rb') as f:
                    zipf.writestr(filename, f.read())

    # Display a download button for the ZIP archive
    st.download_button(label="Téléchargement de tous les fichiers GPX en .zip", data=zip_buffer.getvalue(), file_name="decoupage_mothy.zip")

    # Display a message to indicate that the files have been created
    st.success("Découpage effectué avec succès, zip disponible. N'oubliez pas de dézipper pour faire glisser dans un SIG. Pour télécharger des fichiers individuellement, choisissez plus bas.")

    # Display download buttons for the individual files
    for date_str, time_dict in waypoints_by_date.items():
        for time_str, waypoints in time_dict.items():
            filename = f'{date_str}_{time_str}h.gpx'
            with open(filename, 'rb') as f:
                data = f.read()
            st.download_button(label=f"Fichier horaire (UTC) {filename}", data=data, file_name=filename)
