import os
import hashlib
# noinspection PyPackageRequirements
from typing import List, Dict, Any

from .config import ALPHABET, FINAL_LETTERS
from .errors import CypherError


class BaseEncryptor(object):
    output_path: str
    output_sha1: str
    encoded_text_arr: List[List[str]]

    def __init__(self, source_file: str) -> None:
        if not os.path.exists(source_file):
            raise OSError('File does not exist')
        self.source_path = source_file
        self.text_arr = self.load_text_source()
        self.input_sha1 = self.calculate_sha1(source_file)
        self.output_path = None
        self.output_sha1 = None
        self.encoded_text_arr = None

    def load_text_source(self) -> List[List[str]]:
        text_arr = []
        with open(self.source_path, 'r', encoding='utf-8') as src:
            for line in src:
                text_arr.append(line.split())
        return text_arr

    def write_output(self):
        pass

    def load_cypher(self) -> Any:
        raise NotImplementedError

    def create_reverse_cypher(self) ->Any:
        raise NotImplementedError

    def encode(self) -> None:
        raise NotImplementedError

    def decode(self) -> None:
        raise NotImplementedError

    @staticmethod
    def check_and_supplement_alphabet(cypher: Dict[str, Any]) -> Dict[str, Any]:
        corrected_cypher = dict(cypher)
        if not ALPHABET.issubset(cypher):
            raise CypherError('not all letters present')
        for letter, sub in FINAL_LETTERS:
            if letter not in corrected_cypher:
                corrected_cypher[letter] = corrected_cypher[sub]
        return corrected_cypher

    @staticmethod
    def calculate_sha1(path: str) -> str:
        doc_sha1 = hashlib.sha1()
        with open(path, 'rb') as f:
            block = f.read(2**16)
            while len(block) != 0:
                doc_sha1.update(block)
                block = f.read(2**16)
        return doc_sha1.hexdigest()
