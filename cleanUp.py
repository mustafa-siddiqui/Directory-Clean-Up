'''
@file   cleanUp.py
@brief  This program cleans up a directory by storing pdfs, .docx, png files into
        their separate folders named after the files' respective extensions.
        
        Arguments have to be provided by typing --path <path_to_directory> after
        python3 cleanUp.py if a directory other than the one this file is in needs
        to be sorted/cleaned up.

        For a more detailed info about the process, see this link I read and followed
        to write this program:
        https://www.freecodecamp.org/news/building-bots/#creating-a-directory-clean-up-script

@author Mustafa Siddiqui
@date   07/30/2020
'''

import os
import argparse as arg

if __name__ == "__main__":

    parser = arg.ArgumentParser(
        description="Clean up directory and put files into according folders"
    )

    parser.add_argument(
        "--path",
        type=str,
        default=".",
        help="Directory path of the to be cleaned directory"
    )

    # parse the arguments given by the user and extract the path
    args = parser.parse_args()
    path = args.path

    print(f"Cleaning up directory {path}")

    # get all files from a given directory
    directoryContent = os.listdir(path)

    # create a relative path from the path to the file and the document name
    pathDirectoryContent = [os.path.join(path, doc) for doc in directoryContent]

    # filter directory content into a documents and folders list
    docs = [doc for doc in pathDirectoryContent if os.path.isfile(doc)]
    folders = [folder for folder in pathDirectoryContent if os.path.isdir(folder)]

    # counter to keep track of amount of moved files
    moved = 0

    # list of already created folders to avoid multiple creations
    createdFolders = []

    print(f"Cleaning up {len(docs)} of {len(directoryContent)} elements.")

    for doc in docs:
        # separate filename from file extension
        fullDocPath, fileType = os.path.splitext(doc)
        docPath = os.path.dirname(fullDocPath)
        docName = os.path.basename(fullDocPath)

        # skip this file when it is in directory
        if docName == "directory_clean" or docName.startswith('.'):
            continue

        '''
        print(f"File Type: {fileType}")
        print(f"Full Doc Path: {fullDocPath}")
        print(f"Doc Path: {docPath}")
        print(f"Doc Name: {docName}")
        '''

        # get the subfolder name and create folder if not exist
        subfolderPath = os.path.join(path, fileType[1:].lower())

        if subfolderPath not in folders and subfolderPath not in createdFolders:
            # create the folder
            try:
                os.mkdir(subfolderPath)
                createdFolders.append(subfolderPath)
                print(f"Folder {subfolderPath} created.")
            except FileExistsError as err:
                print(f"Folder already exits at {subfolderPath}...{err}")

        # get the new folder path and move the file
        newDocPath = os.path.join(subfolderPath, docName) + fileType
        os.rename(doc, newDocPath)
        moved += 1

        print(f"Moved file {doc} to {newDocPath}")