import json
import random
from typing import List, Dict, Union

from .base_encryptor import BaseEncryptor
from .config import ALPHABET
from .errors import CypherError


class Scramble(BaseEncryptor):
    def __init__(self, source_file: str, cypher_path: str) -> None:
        super().__init__(source_file)
        with open(cypher_path, 'r', encoding='utf-8') as jf:
            self.cypher_json = json.load(jf)
        self.cypher = self.load_cypher()
        self.reverse_cypher = self.create_reverse_cypher()

    def load_cypher(self) -> Dict[str, str]:
        cypher = self.check_and_supplement_alphabet(self.cypher_json)
        return cypher

    def create_reverse_cypher(self) -> Dict[str, str]:
        return {v: k for k, v in self.cypher}

    @staticmethod
    def transform(source_txt_arr: List[List[str]], transform_dict: Dict[str, str]) -> List[List[str]]:
        transformed_txt_arr = []
        for line in source_txt_arr:
            enc_line = []
            for word in line:
                enc_word = ''
                for letter in word:
                    enc_word += transform_dict[letter] if letter in transform_dict else letter
                enc_line.append(enc_word)
            transformed_txt_arr.append(enc_line)
        return transformed_txt_arr

    def encode(self) -> None:
        self.encoded_text_arr = self.transform(self.text_arr, self.cypher)

    def decode(self) -> None:
        self.text_arr = self.transform(self.encoded_text_arr, self.cypher)


class BookCypher(BaseEncryptor):
    def __init__(self, source_file: str, cypher_path: str):
        super().__init__(source_file)
        with open(cypher_path, 'r', encoding='utf-8') as jf:
            self.cypher_json = json.load(jf)
        self.cypher = self.load_cypher()
        self.reverse_cypher = self.create_reverse_cypher()

    def load_cypher(self) -> Dict[str, List[str]]:
        cypher = dict(self.check_and_supplement_alphabet(self.cypher_json))
        if any([not isinstance(val, list) for val in cypher.values()]):
            raise CypherError('Cypher not properly formed')
        cypher_values = [i for lst in cypher for i in lst]
        if len(cypher_values) != len(set(cypher_values)):
            raise CypherError('Non unique values in cypher')
        return cypher

    def create_reverse_cypher(self) -> Dict[str, str]:
        rev_cypher = dict()
        for key, val_lst in self.cypher:
            for value in val_lst:
                rev_cypher[value] = key
        return rev_cypher

    @staticmethod
    def transform(source_txt_arr: List[List[str]], transform_dict: Dict[str, Union[str, List[str]]]) -> List[List[str]]:
        for key in transform_dict:
            if not isinstance(transform_dict[key], list):
                transform_dict[key] = [transform_dict[key]]
        transformed_txt_arr = []
        for line in source_txt_arr:
            t_line = []
            for word in line:
                t_word = ''.join([random.choice(transform_dict[letter]) if letter in transform_dict else letter
                                  for letter in list(word)])
                t_line.append(t_word)
            transformed_txt_arr.append(t_line)
        return transformed_txt_arr

    def encode(self) -> None:
        self.encoded_text_arr = self.transform(self.text_arr, self.cypher)

    def decode(self) -> None:
        self.text_arr = self.transform(self.encoded_text_arr, self.reverse_cypher)


class CodeWord(BaseEncryptor):
    def __init__(self, source_file: str, code_word: str) -> None:
        super().__init__(source_file)
        self.code_word = code_word
        self.cypher = self.load_cypher()
        self.reverse_cypher = self.create_reverse_cypher()

    def load_cypher(self) -> List[Dict[str, str]]:
        cypher = []
        for code_letter in self.code_word:
            offset = ALPHABET.index(code_letter)
            cypher.append({letter: ALPHABET[ALPHABET.index(letter) + offset] for letter in ALPHABET})
            cypher = self.check_and_supplement_alphabet(cypher)
        return cypher

    def create_reverse_cypher(self):
        rev_cypher = []
        for cypher in self.cypher:
            rev_cypher.append({v: k for k, v in cypher})
        return rev_cypher

    @staticmethod
    def transform(source_text_array: List[List[str]], transform_lst: List[Dict[str, str]]) -> List[List[str]]:
        i = 0
        t_arr = []
        for line in source_text_array:
            t_line = []
            for word in line:
                t_word = ''
                for letter in word:
                    if letter not in transform_lst[i]:
                        t_word += letter
                    else:
                        t_word += transform_lst[i][letter]
                        i += 1
                        if i > len(transform_lst):
                            i = 0
                t_line.append(t_word)
            t_arr.append(t_line)
        return t_arr

    def encode(self) -> None:
        self.encoded_text_arr = self.transform(self.text_arr, self.cypher)

    def decode(self) -> None:
        self.text_arr = self.transform(self.text_arr, self.cypher)
