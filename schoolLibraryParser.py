import argparse
import pandas as pd
import re


class book(object):
    def __init__(self):
        self.title = ''
        self.type = ''
        self.callNumber = ''
        self.editorDescription = ''
        self.author = ''
        self.subLocation = ''
        self.series = ''
        self.published = ''
        self.readingLevel = ''
        self.interestLevel = ''
        self.lexicalCategoryID = ''
        self.copiesAvailable = ''

    def toList(self):
        return [
            self.title,
            self.type,
            self.callNumber,
            self.editorDescription,
            self.author,
            self.subLocation,
            self.series,
            self.published,
            self.readingLevel,
            self.interestLevel,
            self.lexicalCategoryID,
            self.copiesAvailable
        ]


def getTitle(line, book):
    line = line.strip()
    if line.endswith("Open"):
        line = line[:-5]
    book.title = line.strip()


def getTypeCallNumAuthor(line, book):
    line = line.strip()
    data = line.split('  \t')
    type = ''
    callNum = ''
    author = ''

    # Get type
    type = data[0]

    # Get call number and author
    if 'call #:' in data[1].lower():
        callNum = data[1]
        authorSearch = re.search(r'[A-Za-z]+,\s+[A-Za-z]+\s?([A-Za-z][.]?\s?)*', data[1])
        if authorSearch is not None:
            author = authorSearch.group()
    else:  # No call number available, return only the type and author
        author = data[1]

    book.type = type
    book.callNumber = callNum
    book.author = author


def getOther(line, book):
    line = line.strip()
    if line.lower().startswith('sublocation'):
        book.subLocation = line.split(':')[1].strip()
    elif line.lower().startswith('series'):
        series = line.split(':')[1].strip()
        if series.endswith(','):
            series = series[:-1]
        book.series = series
    elif line.lower().startswith('published'):
        book.published = line.split()[1].strip()
    elif line.lower().startswith('reading level') or line.lower().startswith('interest level'):
        data = line.split('  ')
        if len(data) > 1:
            book.readingLevel = data[0].split(':')[1].strip()
            book.interestLevel = '="{0}"'.format(data[1].split(':')[1].strip())
        else:
            if 'reading level' in line.lower().split(':')[0]:
                book.readingLevel = line.split(':')[1].strip()
            else:
                book.interestLevel = '="{0}"'.format(line.split(':')[1].strip())
    elif line.lower().startswith('lexile'):
        book.lexicalCategoryID = line.split(':')[1].strip()
    elif line.lower().endswith('available'):
        data = line.split()
        book.copiesAvailable = '="{0}/{1}"'.format(data[0], data[2])


def main():
    # Command line parser
    cmdParser = argparse.ArgumentParser(
        prog="schoolLibraryParser",
        description="Parses data from school library database and formats for easier manipulation"
    )
    cmdParser.add_argument('filepath', help='The full filepath for the book database file to parse')
    cmdParser.add_argument('savepath', help='The full filepath to the location that the resulting CSV should save to.')
    # Get filepath to parse
    cmdArgs = cmdParser.parse_args()
    FILEPATH = cmdArgs.filepath
    SAVEPATH = cmdArgs.savepath

    # Data
    bookCount = 0
    booksList = []

    with open(FILEPATH, 'r', encoding='utf-8') as file:
        while True:
            line = file.readline()

            if not line:
                break

            if line.strip().lower() == 'cover image':
                myBook = book()

                getTitle(file.readline(), myBook)
                getTypeCallNumAuthor(file.readline(), myBook)
                while True:
                    line = file.readline()
                    if line is None or 'add to this list' in line.lower():
                        break
                    getOther(line, myBook)

                booksList.append(myBook.toList())
                bookCount += 1

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

    try:
        booksDf.to_csv(SAVEPATH)
        print('Successfully saved results to {0}'.format(SAVEPATH))
    except Exception as e:
        print('Could not write books to CSV...\n{0}'.format(e))


if __name__ == "__main__":
    main()
