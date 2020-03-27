
#Video: https://www.youtube.com/watch?v=9OYYgJUAw-w
from __future__ import print_function
import httplib2
import os, io
import requests
import pickle

from datetime import datetime, timedelta
from apiclient import discovery, errors
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
#from apiclient.http import MediaFileUpload, MediaIoBaseDownload
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None
import auth
# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/drive-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/drive'
CLIENT_SECRET_FILE = 'client_secrets.json'
APPLICATION_NAME = 'Drive API Python Quickstart'
authInst = auth.auth(SCOPES,CLIENT_SECRET_FILE,APPLICATION_NAME)
credentials = authInst.getCredentials()
DRIVE_FOLDER_ID = '1RovjMstZWYNIQevwvjaaiKt2GuKw3Ks4'

http = credentials.authorize(httplib2.Http())
drive_service = discovery.build('drive', 'v3', http=http)

def listFiles(size):
    results = drive_service.files().list(
        pageSize=size,fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])
    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print('{0} ({1})'.format(item['name'], item['id']))

def uploadFile(filename,filepath,mimetype):
    file_metadata = {'name': filename, "parents": '1RovjMstZWYNIQevwvjaaiKt2GuKw3Ks4'}
    media = MediaFileUpload(filepath,
                            mimetype=mimetype, 
                            resumable=False)
    file = drive_service.files().create(body=file_metadata,
                                        media_body=media,
                                        fields='id').execute()
    print('File ID: %s' % file.get('id'))
    save_filename(file.get('id'))

def downloadFile(file_id,filepath):
    request = drive_service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print("Download %d%%." % int(status.progress() * 100))
    with io.open(filepath,'wb') as f:
        fh.seek(0)
        f.write(fh.read())

def createFolder(name):
    file_metadata = {
    'name': name,
    'mimeType': 'application/vnd.google-apps.folder'
    }
    file = drive_service.files().create(body=file_metadata,
                                        fields='id').execute()
    print ('Folder ID: %s' % file.get('id'))

def searchFile(size,query):
    results = drive_service.files().list(
    pageSize=size,fields="nextPageToken, files(id, name, kind, mimeType)",q=query).execute()
    items = results.get('files', [])
    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print(item)
            print('{0} ({1})'.format(item['name'], item['id']))

def getCovidData(d):
    
    year = d.year
    month = d.month
    day = d.day

    if d.month < 10:
        month = "0{}".format(d.month)
    if d.day < 10:
        day = "0{}".format(d.day)

    URL = "https://www.ecdc.europa.eu/sites/default/files/documents/COVID-19-geographic-disbtribution-worldwide-{}-{}-{}.xlsx".format(year, month, day)
    print(URL)

    r = requests.get(URL, allow_redirects=True)
    if r.status_code != 200:
        print("Download not successful")
        last_day = datetime.today() - timedelta(days=1)
        getCovidData(last_day)
    else:
        open('covid.xlsx', 'wb').write(r.content)
        print("Download successful")
    
def delete_file(service, file_id):
    print("Trying to delete - {}".format(file_id))
    try:
        service.files().delete(fileId=file_id).execute()
        print("File was deleted from Drive")
    except:
        print('No file to delete')

def save_filename(id):
    pickle.dump([id], open("id.p", "wb"))

def load_filename():
    return pickle.load(open("id.p","rb"))

# Execution
last_file_id = ''
try:
    last_file_id = load_filename()
except:
    print("no file")
delete_file(drive_service, last_file_id)
d = datetime.today()
getCovidData(d)
uploadFile('covid.xlsx','covid.xlsx','application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
#uploadFile('unnamed.jpg','unnamed.jpg','image/jpeg')
#downloadFile('1Knxs5kRAMnoH5fivGeNsdrj_SIgLiqzV','google.jpg')
#createFolder('Google')
#searchFile(10,"name contains 'Getting'")