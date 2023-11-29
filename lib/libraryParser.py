import pandas as pd
import re


class book(object):
    def __init__(self):
        self.school = ''
        self.title = ''
        self.type = ''
        self.callNumber = ''
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
            self.school,
            self.title,
            self.type,
            self.callNumber,
            self.author,
            self.subLocation,
            self.series,
            self.published,
            self.readingLevel,
            self.interestLevel,
            self.lexicalCategoryID,
            self.copiesAvailable
        ]


class libraryParser(object):
    def __init__(self, schoolName, filepath, savepath):
        self.schoolName = schoolName
        self.filepath = filepath
        self.savepath = savepath
        self.bookCount = 0
        self.columns = [
            'School',
            'Title',
            'Type',
            'Call Number',
            'Author',
            'Sublocation',
            'Series',
            'Published',
            'Reading Level',
            'Interest Level',
            'Lexical Category ID',
            'Copies Available'
        ]

    def _getTitle(self, line, book):
        line = line.strip()
        if line.endswith("Open"):
            line = line[:-5]
        if line.endswith('.'):
            line = line[:-1]
        book.title = line.strip()

    def _getTypeCallNumAuthor(self, line, book):
        line = line.strip()
        data = line.split('  \t')
        type = ''
        callNum = ''
        author = ''

        # Get type
        type = data[0]

        # Get call number and author
        if 'call #:' in data[1].lower():
            authorSearch = re.search(r'[A-Za-z]+,\s+[A-Za-z]+\s?([A-Za-z][.]?\s?)*', data[1])
            callNum = data[1][7:].strip()
            if authorSearch is not None:
                author = authorSearch.group()
                iToRemove = callNum.find(author)
                callNum = callNum[:iToRemove]
        else:  # No call number available, return only the type and author
            author = data[1]

        if callNum.endswith('.'):
            callNum = callNum[:-1]
        if author.endswith('.'):
            author = author[:-1]

        book.type = type
        book.callNumber = callNum
        book.author = author

    def _getOther(self, line, book):
        line = line.strip()
        if line.lower().startswith('sublocation'):
            book.subLocation = line.split(':')[1].strip()
        elif line.lower().startswith('series'):
            series = line.split(':')[1].strip()
            if series.endswith(',') or series.endswith('.'):
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

    def parse(self, debug=True):
        # Data
        self.bookCount = 0
        booksList = []

        try:
            with open(self.filepath, 'r', encoding='utf-8') as file:
                if debug:
                    print("Parsing...")
                while True:
                    line = file.readline()

                    if not line:
                        break

                    if line.strip().lower() == 'cover image':
                        myBook = book()

                        myBook.school = self.schoolName
                        self._getTitle(file.readline(), myBook)
                        self._getTypeCallNumAuthor(file.readline(), myBook)
                        while True:
                            line = file.readline()
                            if line is None or 'add to this list' in line.lower():
                                break
                            self._getOther(line, myBook)

                        booksList.append(myBook.toList())
                        self.bookCount += 1
        except Exception as e:
            print("Error while trying to parse file...\n{0}".format(e))
            return False

        if debug:
            print('{0} books parsed!'.format(self.bookCount))
        booksDf = pd.DataFrame(booksList, columns=self.columns)

        try:
            booksDf.to_csv(self.savepath)
            if debug:
                print('Saved results to {0}'.format(self.savepath))
            return True
        except Exception as e:
            print('Error while trying to write books to CSV...\n{0}'.format(e))
            return False
