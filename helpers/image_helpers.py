from hashlib import md5
from time import localtime

def add_prefix(filename):
    prefix = md5(str(localtime()).encode('utf-8')).hexdigest()
    return f"{prefix[:8]}_{filename}"

