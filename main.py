#https://towardsdatascience.com/how-to-manage-files-in-google-drive-with-python-d26471d91ecd
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import requests
from datetime import datetime, timedelta

gauth = GoogleAuth()
gauth.LocalWebserverAuth() # client_secrets.json need to be in the same directory as the script
drive = GoogleDrive(gauth)

# Put in your folder ID here
FOLDER_ID = '1RovjMstZWYNIQevwvjaaiKt2GuKw3Ks4'

def uploadNewFile(filename,FOLDER_ID,mimetype):
    file1 = drive.CreateFile({"mimeType": mimetype, "parents": [{"kind": "drive#fileLink", "id": FOLDER_ID}]})
    file1.SetContentFile(filename)
    try:
        file1.Upload() # Upload the file.
        print("Upload successful. ID: {}".format(file1.get('id')))
    except:
        print("Upload failed. ID: {}".format(file1.get('id')))

def deleteOldFile(file_name):
    # search fr file id
    fileList = drive.ListFile({'q': "'1RovjMstZWYNIQevwvjaaiKt2GuKw3Ks4' in parents and trashed=false"}).GetList()
    for file in fileList:
        # Get the folder ID that you want
        if(file['title'] == file_name):
            file_id = file['id']
    try:
        file2 = drive.CreateFile({'id': file_id}) # Initialize GoogleDriveFile instance with file id.
        file2.Delete() # Permanently delete the file.
        print("File was deleted from Drive. ID: {}".format(file['id']))
    except:
        print('No file to delete')

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

#Execution
print("---Downloading New Covid Data---")
d = datetime.today() # outside def because of recursion
getCovidData(d)

print("---Updating Covid Data on Drive---")
deleteOldFile('covid.xlsx')
uploadNewFile('covid.xlsx', FOLDER_ID ,'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
