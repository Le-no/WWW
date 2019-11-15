import os


# def makeHTMLtable(top, depthfirst=False):
#     from xml.sax.saxutils import escape  # To quote out things like &amp;
#     ret = ['<table class="fileList">\n']
#     for top, names in walktree(top):
#         ret.append('   <tr><td class="directory">%s</td></tr>\n' % escape(top))
#         for name in names:
#             ret.append('   <tr><td class="file">%s</td></tr>\n' % escape(name))
#     ret.append('</table>')
#     return ''.join(ret)  # Much faster than += method
#
#
# def walktree(top=".", depthfirst=True):
#     """Walk the directory tree, starting from top. Credit to Noah Spurrier and Doug Fort."""
#
#     names = os.listdir(top)
#     if not depthfirst:
#         yield top, names
#     for name in names:
#         try:
#             st = os.lstat(os.path.join(top, name))
#         except os.error:
#             continue
#         if stat.S_ISDIR(st.st_mode):
#             for (newtop, children) in walktree(os.path.join(top, name), depthfirst):
#                 yield newtop, children
#     if depthfirst:
#         yield top, names


def starting(top):
    names = os.listdir(top)

    print(names)
    dir = ''
    for name in names:
        dir += "<a href=" + top + "/" + name + ">" + name + "</a><br/><br/>\n"
    return dir
