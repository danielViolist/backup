#!/usr/bin/python3
import zipfile
import os
import argparse
import re

def backup_to_zip(folder, name, regex, verbose):
    # Creating zip file object.
    if name == "":
        name = os.path.basename(folder) + ".zip"
    regex_bool = False
    if regex != "":
        regex_bool = True
    zip = zipfile.ZipFile(name, 'w')
    if regex_bool is False:
        # Walk through the directory and add files/folders to the zip.
        for foldername, subfolders, filenames in os.walk(folder):
            if verbose == 1 or verbose == 2:
                print('Adding files in %s...' % foldername)
            zip.write(foldername)
            # Adding all the files in this folder to the zip.
            for filename in filenames:
                if verbose == 2:
                    print("\tAdding file: %s" % filename)
                zip.write(os.path.join(foldername, filename))
    else:
        re_filter = re.compile(regex)
        for foldername, subfolders, filenames in os.walk(folder):
            if verbose == 1 or verbose == 2:
                print('Folder %s...' % foldername)
            zip.write(foldername)
            for filename in filenames:
                if re_filter.match(filename):
                    if verbose == 2:
                        print('\tAdding file: %s' % filename)
                    zip.write(os.path.join(foldername, filename))
    zip.close()
    print("Done.")

if __name__ == "__main__":
    # Argument handling ========================================================================================================================
    parser = argparse.ArgumentParser(
        description="Backup files into a zip file by entering a folder location and optional regex that can be used to only include certain files.")
    # Folder
    parser.add_argument("-f", "--folder", dest="folder",
                        help="Folder location to backup into a zip file. Provide relative or absolute path.",
                        required=True, type=str)
    # Zip file name
    parser.add_argument("-n", "--name", dest="name", help="Name of the zip file to create. This can also be a path.",
                        default="", type=str)
    # Regex
    parser.add_argument("-r", "--regex", dest="regex",
                        help="Regex used to find files to add to zip. Must use the \"'\" character to enclose the regular expression. "
                             "[Example Command] `backup -f folder_name -r '\d'`", type=str, default="")
    # Verbose
    parser.add_argument("-v", "--verbose",
                        help="Display extra details while running. Levels of verbosity: 0, 1 or 2. Default: 0",
                        type=int, default=0)
    args = parser.parse_args()
    # End Argument handling ====================================================================================================================
    # Ensuring correct verbose value was entered
    verbose = 0
    if args.verbose >= 2:
        verbose = 2
    elif args.verbose == 1:
        verbose = 1
    else:
        verbose = 0
    name = ""
    if not args.name.endswith('.zip'): # appending '.zip' if it wasn't there
        name = args.name + '.zip'
    else:
        name = args.name
    if not os.path.exists('./' + name): # Making sure the file doesn't already exist as this would overwrite it.
        if os.path.exists(os.path.abspath(args.folder)): # Making sure the file location to copy actually exists.
            backup_to_zip(args.folder, name, args.regex, verbose)
        else:
            print("Folder", args.folder, "does not exist! Aborting")
            exit(2)
    else:
        print("The file", name, "already exists! Aborting.")
        exit(1)
