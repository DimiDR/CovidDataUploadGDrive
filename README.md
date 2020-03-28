# Google Drive Api
In this project we will outomaticaly download the covid data and upload this data to a folder in Google Drive.

# Thanks to
This Post
https://towardsdatascience.com/how-to-manage-files-in-google-drive-with-python-d26471d91ecd

## Covid Information
The data is comming from here: 
https://www.ecdc.europa.eu/en/publications-data/download-todays-data-geographic-distribution-covid-19-cases-worldwide

# install packages
Python 3.6

pip install pydrive

# How To Start the Script
0. Install the packages in your environment.
1. Create a Google APi be following the instructions in the word document
2. Rename your client_secret.. JSON to "client_secrets.json" and put it in your directory.
3. Create a folder in Google Drive and click on it. In the Folder URL you will then see the Folder ID (last string after "/"). Copy this string to the "main.py" to "FOLDER_ID"
4. Run !python main.py
5. Outh service will open a page for Drive login. Please authorize the access.