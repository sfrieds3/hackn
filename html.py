def init_html():
    res = []

    res.append('<!DOCTYPE html>')
    res.append('<html>')
    res.append('<head>')
    res.append('<link href="style.css" rel="stylesheet" type="text/css"/>')
    res.append('</head>')
    res.append('<body>')
    return ''.join(res)

def end_html():
    res = []

    res.append('</body>')
    res.append('</html>')
    return ''.join(res)


def link_html(address, name):
    res = []

    res.append('<a href="')
    res.append(address)
    res.append('">')
    res.append(name)
    res.append('</a>')

    return ''.join(res)

def text_html(s):
    res = []
    res.append('<p>')
    res.append(s)
    res.append('</p>')
    return ''.join(res)
