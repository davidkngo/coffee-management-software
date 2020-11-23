def loadStyleSheet(filename):
    with open(filename, 'r') as f:
        qss = str(f.read())
    return qss
