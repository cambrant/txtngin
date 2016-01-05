# Return the contents of a file
def read(filename):
    contents = []

    try:
        with open('contents/' + filename) as f:
            for line in f.readlines():
                contents.append(line.strip('\r\n'))

        return contents
    except:
        return False
