import os
import tkinter.messagebox
import shutil

def generatePath(path, exist_ok=False):
    stringPath = "{}".format(path)
    if not os.path.exists(stringPath):
        try:
            os.makedirs(stringPath, exist_ok=exist_ok)
        except Exception as error:
            print("Generate Path", "{}".format(error))
def pathExisted(path):
    return  os.path.exists(path)

def deleteFile(path):
    if os.path.exists(path):
        os.remove(path)

def deleteFolder(path):
    stringPath = "{}".format(path)
    if os.path.exists(stringPath):
         try:
             shutil.rmtree(stringPath)
             return True
         except Exception as error:
             tkinter.messagebox.showerror("Delete Folder", "{}".format(error))
             return False

    return True

def copyfile2(src, dst):
    try:
        shutil.copy2(src, dst)
    except Exception as error:
        print("ERROR Copy File: {}".format(error))

def copyTree(src, dst):
    try:
        shutil.copytree(src, dst)
    except Exception as error:
        print("ERROR Copy File: {}".format(error))

def moveFolder(src, dst):
    try:
        shutil.move(src, dst)
        return True
    except Exception as error:
        print("ERROR move folder: {}".format(error))
        return False

def rename(oldPath, newPath):
    if os.path.exists(oldPath):
        try:
            os.rename(r'{}'.format(oldPath), r'{}'.format(newPath))
        except Exception as error:
            print("ERROR Rename file: {}".format(error))