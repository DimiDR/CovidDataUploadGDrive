# Google Drive Api
In this project we will outomaticaly download the covid data and upload this data to a folder in Google Drive.

This project was done on the basis of this Video done by 
https://www.youtube.com/watch?v=9OYYgJUAw-w
Original Git Rep: https://github.com/samlopezf/google-drive-api-tutorial

Only the upload functionality was used, as this is the only thing I needed.
Many other functions are explained in the Tutorial and in Google Documentaiton

## YouTube
https://www.youtube.com/watch?v=9OYYgJUAw-w
## Original Git
https://github.com/samlopezf/google-drive-api-tutorial
## Google Docs
https://developers.google.com/drive/api/v3/folder#insert_a_file_in_a_folder
## Covid Information
The data is comming from here: 
https://www.ecdc.europa.eu/en/publications-data/download-todays-data-geographic-distribution-covid-19-cases-worldwide

# install packages
Tested with Python 3.6

pip install httplib2

pip install apiclient

pip install --upgrade google-api-python-client

pip install timedelta

pip install oauth2client

pip install pickle-mixin

# Prerequisits
0. install the packages in your environment. Testes with python 3.6
1. You need to create an API connected to your account.
In the Link: https://developers.google.com/drive/api/v3/quickstart/python
API type I choose is desctop application.
Click on "Enable the Drive API" and download the credentials JSON.
2. Rename this JSON to "client_secrets.json" and put it in your directory.
3. Create a folder in Google Drive and click on it. In the Folder URL you will then see the Folder ID (last string after "/"). Copy this string to the "main.py" to "DRIVE_FOLDER_ID"
4. Run !python main.py
5. Outh service will open a page for Drive login. Please authorize the access.

# workflow
- getCovidData() will download and rename the covid data xlsx file to the working directory
- uploadFile('covid.xlsx','covid.xlsx','application/vnd.openxmlformats-officedocument.spreadsheetml.sheet') will use your credentials and folder to upload the xlsx file to Google Drive
