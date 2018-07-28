import os


class BaseEncryptor(object):
    def __init__(self, source_file: str) -> None:
        if not os.path.exists(source_file):
            pass

    def load_source(self):
        pass

    def write_output(self):
        pass
