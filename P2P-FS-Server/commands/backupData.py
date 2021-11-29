from pathlib import Path
import pickle


# ************************************************************
# restoreData:
#   Description: Loads the clients data from the file. Used when the server reboots and needs to re-populate
#       the clients array.
#   Parameters:
#       filename: The name of the file where to pull the backup data
# ************************************************************


def restoreData(filename):
    # Restore data if file exists
    if Path(f"backup/{filename}").exists():
        try:
            return pickle.load(open(f"backup/{filename}", "rb"))
        except EOFError as e:
            # Error occurs if the file is empty
            pass
    return []


# ************************************************************
# saveData:
#   Description: Saves the clients data to a file. Used to backup the clients array
#   Parameters:
#       filename: The name of the file where to save the backup data
#       dataArray: Store all data from the file into this array (clients)
# ************************************************************


def saveData(filename, dataArray):
    pickle.dump(dataArray, open(f"backup/{filename}", "wb"))
