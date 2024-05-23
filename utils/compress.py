import zlib

def compress_text(data):
    return zlib.compress(data.encode('utf-8'))

def decompress_text(data):
    return zlib.decompress(data).decode('utf-8')

def compress_image(data):
    return zlib.compress(data.encode('utf-8'))