from os import path


def get_jpeg_scan_fixture():
    fname = path.join(path.dirname(__file__),
                      'media_fixtures', 'gatherer_scan.jpeg')
    return open(fname, 'rb').read()
