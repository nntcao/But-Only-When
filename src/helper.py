def strip_filename_from_path(path: str):
    path = path.replace('\\', '/')
    filename = (path.split('/')[-1]).split('.')[0]
    return filename

def backslash_to_forward_slash(path: str):
    l = list(path)
    for i, c in enumerate(l):
        if c == '\\':
            l[i] = '/'
    return "".join(l)