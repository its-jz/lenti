import pathlib
import pandas as pd
import dropbox
from dropbox.exceptions import AuthError

DROPBOX_ACCESS_TOKEN = "sl.BUZXdsuIYJPye1u5uFcCn0ZaBYEccaBwMgflvHWZZGKFrDaV8Kc32oJDOg64Edr3NKDRulFPWx4KviPEiyAf1E_MiuXw6o799j9Fyv7FhT0WQvnASxxKQm8sW5CS0CZ0cC0lT4t0"

def dropbox_connect():
    """Create a connection to Dropbox."""

    try:
        dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)
    except AuthError as e:
        print('Error connecting to Dropbox with access token: ' + str(e))
    return dbx

def dropbox_upload_file(local_path, local_file, dropbox_file_path):
    """Upload a file from the local machine to a path in the Dropbox app directory.

    Args:
        local_path (str): The path to the local file.
        local_file (str): The name of the local file.
        dropbox_file_path (str): The path to the file in the Dropbox app directory.

    Example:
        dropbox_upload_file('.', 'test.csv', '/stuff/test.csv')

    Returns:
        meta: The Dropbox file metadata.
    """

    try:
        dbx = dropbox_connect()

        local_file_path = pathlib.Path(local_path) / local_file

        with local_file_path.open("rb") as f:
            meta = dbx.files_upload(f.read(), dropbox_file_path, mode=dropbox.files.WriteMode("overwrite"))

            return meta
    except Exception as e:
        print('Error uploading file to Dropbox: ' + str(e))

dropbox_connect()
local_path = "."
local_file = "rando-img.jpg"
dropbox_file_path = "/"
# dropbox_upload_file('.', 'test.csv', '/stuff/test.csv')
# dropbox_upload_file(local_path,local_file,dropbox_file_path)
dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)
for entry in dbx.files_list_folder('').entries:
    print(entry.name)
f = open("./rando-img.jpg", 'rb')
meta = dbx.files_upload(f.read(), "/lenti/rando-img.jpg")

