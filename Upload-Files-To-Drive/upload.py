"""
This is  an automation script to upload all the folders and files in a taregt directory to my google
drive. The main task is run here, but it requires a bash script to activate the virtual environment,
and a crontab to schedule the upload on every reboot.
"""
from glob import glob
import logging
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os


FOLDER = "application/vnd.google-apps.folder"
PATH = "/".join(os.path.abspath(__file__).split('/')[:-1])
CREDS = os.path.join(PATH, "mycreds.txt")
LOG = os.path.join(PATH, "uploads.log")
TARGET = "path/to/target/folder"

logging.basicConfig(level=logging.INFO, filename=LOG, format="%(asctime)s :: %(levelname)s :: %(message)s")
g_auth = GoogleAuth()
"""
Google Authentication requires a client_secrets.json file, which is basically an API key.
How to get an API key? Link - https://medium.com/analytics-vidhya/how-to-connect-google-drive-to-python-using-pydrive-9681b2a14f20
"""
g_auth.DEFAULT_SETTINGS["client_config_file"] = os.path.join(PATH, "client_secrets.json")

if os.path.isfile(CREDS):
    g_auth.LoadCredentialsFile(CREDS)
else:
    g_auth.LocalWebserverAuth()
    #This saves the credentials to automate browser authentication
    g_auth.SaveCredentialsFile(CREDS)

drive = GoogleDrive(g_auth)


def get_folders(og_path, recur):
    """
    Recusrsively checks every folder and every file in the target directory, and uploads it to drive.
    """
    try:
        parent = drive.ListFile({"q": "title='{}' and trashed=false".format(og_path.split('/')[-2])}).GetList()
        search_path = os.path.join(og_path, "*/")
        folders = glob(search_path)

        for folder in folders:
            dir_name = folder.split('/')[-2]
            query = drive.ListFile({"q": "title='{}' and trashed=false".format(dir_name)}).GetList()
            if query == []:
                if parent == []:
                    create_folder = drive.CreateFile({"title": dir_name, "mimeType": FOLDER})
                    create_folder.Upload()
                else:
                    create_folder = drive.CreateFile({"title": dir_name, "mimeType": FOLDER, "parents": [{"id": parent[0]["id"]}]})
                    create_folder.Upload()
                logging.info("Creating - {}".format(dir_name))
            else:
                logging.info("{} exists".format(dir_name))
            get_folders(folder, True)
            

        if recur:
            for file in os.listdir(og_path):
                file_path = os.path.join(og_path, file)
                if not os.path.isdir(file_path):
                    query = drive.ListFile({"q": "title='{}' and trashed=false".format(file)}).GetList()
                    if query == []:
                        if parent == []:
                            create_folder = drive.CreateFile()
                            create_folder.SetContentFile(file_path)
                            create_folder.Upload()
                        else:
                            create_folder = drive.CreateFile({"parents": [{"id": parent[0]["id"]}]})
                            create_folder.SetContentFile(file_path) 
                            create_folder.Upload()
                        logging.info("{} created in {}".format(file, parent[0]["title"]))
                    else:
                        logging.info("{} already exists".format(file))
                    logging.info("{} deleted from local storage.".format(file))
                    os.remove(file_path)
    except Exception as e:
        logging.error(e)
        get_folders(og_path, recur)


get_folders(TARGET + '/', False)
