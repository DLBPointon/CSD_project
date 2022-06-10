"""
Simple python script to convert 
genomic multi-fasta into pep sequence.

Author: dp24/DLBPointon
"""

import os 
import sys

from Bio.Seq import Seq
from Bio import File
from Bio import SeqIO


def read_fasta(filetoparse):
    """
    Desc: A function which opens and splits a fasta into name and seq.
    Returns: Header and sequence of input file
    """
    name, seq = None, []

    for line in filetoparse:
        line = line.rstrip()

        if line.startswith(">"):
            if name:
                yield name, ''.join(seq)
            name, seq = line, []
        else:
            seq.append(line)

    if name:
        yield name, ''.join(seq)


def dnafile_to_pepfile(file_in, file_out):
    """
    Desc: Opens input dna.fasta and uses Biopython to convert to pep.fasta.
            Also attempts to add 'N's to sequence not divisible by 3.
    Returns: Output file in file_out
    """
    with open(file_in, 'r') as filetoparse:
        with open(file_out , 'a') as peptowrite:
            for name, seq in read_fasta(filetoparse):
                if not len(seq)%3 == 0:
                    multiplier = (len(seq)%3) - 3
                    seq = seq + multiplier * 'N'
                pep = Seq(seq).translate()
                peptowrite.write(f'{str(name)}\n{str(pep)}\n')


def main():
    """
    Desc: Main logic function, forms new outfile name
    Returns: NA
    """
    input_list = sys.argv[1].split('/')[-1]
    out_file = sys.argv[2] + input_list + '.pep'

    print(f'Working on: {sys.argv[1]}, Outputting: {out_file}')

    dnafile_to_pepfile(sys.argv[1], out_file)


if __name__ == "__main__":
    main()