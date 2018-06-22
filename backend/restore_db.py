"""
Restore recent db file to local.
"""

import sys
import getopt
import dropbox
from dropbox.files import WriteMode
from dropbox.exceptions import ApiError, AuthError

LOCALFILE = 'game.db'
BACKUPPATH = '/game_backup.db'

# Restore the local and Dropbox files to a certain revision
def restore(rev=None):
    # Restore the file on Dropbox to a certain revision
    print("Restoring " + BACKUPPATH + " to revision " + rev + " on Dropbox...")
    dbx.files_restore(BACKUPPATH, rev)

    # Download the specific revision of the file at BACKUPPATH to LOCALFILE
    print("Downloading current " + BACKUPPATH + " from Dropbox, overwriting " + LOCALFILE + "...")
    dbx.files_download_to_file(LOCALFILE, BACKUPPATH, rev)

# Look at all of the available revisions on Dropbox, and return the oldest one
def select_revision():
    # Get the revisions for a file (and sort by the datetime object, "server_modified")
    print("Finding available revisions on Dropbox...")
    entries = dbx.files_list_revisions(BACKUPPATH, limit=30).entries
    revisions = sorted(entries, key=lambda entry: entry.server_modified)

    for revision in revisions:
        print(revision.rev, revision.server_modified)

    # Return the oldest revision (first entry, because revisions was sorted oldest:newest)
    return revisions[0].rev

if __name__ == '__main__':
    argv = sys.argv[1:]

    token = ''
    try:
        opts, args = getopt.getopt(argv, "ht:", ["help", "token="])
    except getopt.GetoptError:
        print("restore_db.py --token <Dropbox token string>")
        sys.exit()
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print("restore_db.py --token <Dropbox token string>")
            sys.exit()
        elif opt in ("-t", "--token"):
            token = arg

    # Check for an access token
    if (len(token) == 0):
        sys.exit("ERROR: Looks like you didn't add your access token.")

    # Create an instance of a Dropbox class, which can make requests to the API.
    print("Creating a Dropbox object...")
    dbx = dropbox.Dropbox(token)

    # Check that the access token is valid
    try:
        dbx.users_get_current_account()
    except AuthError as err:
        sys.exit("ERROR: Invalid access token; try re-generating an "
            "access token from the app console on the web.")

    # Restore the local and Dropbox files to a certain revision
    to_rev = select_revision()
    restore(to_rev)

    print("Done!")