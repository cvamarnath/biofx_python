#!/usr/bin/env python3
""" Probabalistically subset FASTA files """

import argparse
import os
import random
from Bio import SeqIO
from typing import List, NamedTuple, TextIO


class Args(NamedTuple):
    """ Command-line arguments """
    files: List[TextIO]
    percent: float
    seed: int
    outdir: str


# --------------------------------------------------
def get_args() -> Args:
    """ Get command-line arguments """

    parser = argparse.ArgumentParser(
        description='Probabalistically subset FASTA files',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('file',
                        metavar='FILE',
                        type=argparse.FileType('r'),
                        nargs='+',
                        help='Input FASTA file(s)')

    parser.add_argument('-p',
                        '--percent',
                        help='Percent of reads',
                        metavar='reads',
                        type=float,
                        default=.1)

    parser.add_argument('-s',
                        '--seed',
                        help='Random seed value',
                        metavar='seed',
                        type=int,
                        default=None)

    parser.add_argument('-o',
                        '--outdir',
                        help='Output directory',
                        metavar='DIR',
                        type=str,
                        default='out')

    args = parser.parse_args()

    if not 0 < args.percent < 1:
        parser.error(f'--percent "{args.percent}" must be between 0 and 1')

    if not os.path.isdir(args.outdir):
        os.makedirs(args.outdir)

    return Args(files=args.file,
                percent=args.percent,
                seed=args.seed,
                outdir=args.outdir)


# --------------------------------------------------
def main() -> None:
    """ Make a jazz noise here """

    args = get_args()
    random.seed(args.seed)

    total_num = 0
    for i, fh in enumerate(args.files, start=1):
        basename = os.path.basename(fh.name)
        out_file = os.path.join(args.outdir, basename)
        print(f'{i:3}: {basename}')

        out_fh = open(out_file, 'wt')
        num_taken = 0

        for rec in SeqIO.parse(fh, 'fasta'):
            if random.random() <= args.percent:
                num_taken += 1
                SeqIO.write(rec, out_fh, 'fasta')

        out_fh.close()
        total_num += num_taken

    num_files = len(args.files)
    print(f'Wrote {total_num:,} sequence{"" if total_num == 1 else "s"} '
          f'from {num_files:,} file{"" if num_files == 1 else "s"} '
          f'to directory "{args.outdir}"')


# --------------------------------------------------
if __name__ == '__main__':
    main()
