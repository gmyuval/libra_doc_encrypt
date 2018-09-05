import argparse

from .encryptors import Scramble, BookCypher, CodeWord


def parse_commandline() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(title='Cypher type', dest='enc_type', help='Choice of cyphers')
    scramble_parser = subparsers.add_parser('scramble')
    scramble_parser.add_argument('cypherfile', action='store', help='Path to the cypher JSON')
    ref_parser = subparsers.add_parser('ref')
    ref_parser.add_argument('cypherfile', action='store', help='Path to the cypher JSON')
    codeword_parser = subparsers.add_parser('codeword')
    codeword_parser.add_argument('code', action='store', help='Word to use for text encryption')
    parser.add_argument('source', action='strore', help='Source file for encoding')
    return parser.parse_args()


def main() -> None:
    args = parse_commandline()
    if args.enc_type == 'scramble':
        enc = Scramble(args.source, args.cypherfile)
    elif args.enc_type == 'ref':
        enc = BookCypher(args.source, args.cypherfile)
    elif args.enc_type == 'code':
        enc = CodeWord(args.source, args.code)

