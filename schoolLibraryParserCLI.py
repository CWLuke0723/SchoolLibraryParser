import os
import argparse
from lib.libraryParser import libraryParser

APP_NAME = "School Library Parser"
VERSION = "v1.1.0"


def main():
    print("{0} - {1}".format(APP_NAME, VERSION))

    # Command line parser
    cmdParser = argparse.ArgumentParser(
        prog="schoolLibraryParserCLI.py",
        description="Parses data from school library database and formats for easier manipulation"
    )
    cmdParser.add_argument('schoolName', help="The name of the school that the file is being pulled from")
    cmdParser.add_argument('filepath', help='The full filepath for the book database file to parse')
    cmdParser.add_argument('savepath', help='The full filepath to the location that the resulting CSV should save to.')
    cmdArgs = cmdParser.parse_args()

    SCHOOL_NAME = cmdArgs.schoolName
    FILEPATH = cmdArgs.filepath
    SAVEPATH = cmdArgs.savepath

    if os.path.exists(FILEPATH):
        parser = libraryParser(SCHOOL_NAME, FILEPATH, SAVEPATH)
        success = parser.parse(debug=True)

        if success:
            print("SUCCESS")
        else:
            print("FAILED")
    else:
        print("Problem opening source file: {0}\nPlease check that the filepath is correct and try again...".format(FILEPATH))


if __name__ == "__main__":
    main()
