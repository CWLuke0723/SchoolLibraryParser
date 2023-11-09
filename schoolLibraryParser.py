import argparse
import pandas as pd


def getTitle(line):
    line.strip()
    if line.endswith("Open"):
        line = line[:-5]
    return line.strip()


def getTypeCallNumAuthor(line):
    line.strip()
    data = line.split()

    if data[0] != 'Follett':
        type = data[0]
        data = data[1:]
    else:
        type = data[0] + " " + data[1]
        data = data[2:]

    callNum = None
    author = None

    if data[0] == 'Call' and data[1] == '#:':
        callNum = " ".join(data[2:])
        for item in data[2:-1]:
            if item.endswith(','):
                author = " ".join([item, data[data.index(item) + 1].replace(',', '').replace('.', '')])
                break
    else:  # No call number available, return only the type and author
        author = " ".join(data)

    return type, callNum, author


def main():
    # Command line parser
    cmdParser = argparse.ArgumentParser(
        prog="schoolLibraryParser",
        description="Parses data from school library database and formats for easier manipulation"
    )
    cmdParser.add_argument('filepath', help='The full filepath for the book database file to parse')
    # Get filepath to parse
    cmdArgs = cmdParser.parse_args()
    FILEPATH = cmdArgs.filepath

    # Data
    bookCount = 0
    booksList = []

    with open(FILEPATH, 'r', encoding='utf-8') as file:
        while True:
            line = file.readline()

            if not line:
                break

            if line.strip().lower() == 'cover image':
                title = getTitle(file.readline())
                type, callNum, author = getTypeCallNumAuthor(file.readline())

                booksList.append([
                    title,
                    type,
                    callNum,
                    '',
                    author,
                    '',
                    '',
                    '',
                    '',
                    '',
                    '',
                    ''
                ])

                bookCount += 1

    print(booksList)
    print('{0} books parsed...'.format(bookCount))
    booksDf = pd.DataFrame(
        booksList,
        columns=[
            'Title',
            'Type',
            'Call Number',
            'Editor Description',
            'Author',
            'Sublocation',
            'Series',
            'Published',
            'Reading Level',
            'Interest Level',
            'Lexical Category ID',
            'Copies Available'
        ]
    )
    booksDf.to_csv('.\\testresults\\results.csv')


if __name__ == "__main__":
    main()
