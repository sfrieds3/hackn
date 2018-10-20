def init_html():
    res = []

    res.append('<!DOCTYPE html>')
    res.append('\n\t')
    res.append('<html>')
    res.append('\n\t\t')
    res.append('<head>')
    res.append('\n\t\t\t')
    res.append('<link href="style.css" rel="stylesheet" type="text/css"/>')
    res.append('\n\t\t')
    res.append('</head>')
    res.append('\n\t\t')
    res.append('<body>')
    res.append('\n')
    return ''.join(res)

def end_html():
    res = []

    res.append('\n\t\t')
    res.append('</body>')
    res.append('</html>')
    res.append('\n')
    return ''.join(res)


def link_html(address, name):
    res = []

    res.append('\t\t\t')
    res.append('<a href="')
    res.append(address)
    res.append('\n\t\t\t')
    res.append('" class="link"')
    res.append('>')
    res.append(name)
    res.append('</a>')
    res.append('\n')

    return ''.join(res)

def text_html(string):
    res = []
    res.append('\t\t\t')
    res.append('<p>')
    res.append(string)
    res.append('</p>')
    res.append('\n')
    return ''.join(res)


# def text_html(name, link):
#     res = []

#     res.append('<a href="')
#     res.append(link)
#     res.append('" class="title"')
#     res.append('>')
#     res.append('<p>')
#     res.append(name)
#     res.append('</p>')
#     res.append('</a>')

#     return ''.join(res)
