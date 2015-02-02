# -*- coding: utf-8 -*-
"""
Created on Sun Feb  2 11:24:42 2014

@author: Isaac Getto

"""

# you may find it useful to import these variables (although you are not required to use them)
from amino_acids_less_structure import aa, codons
import random
from load import load_seq
import re

### YOU WILL START YOUR IMPLEMENTATION FROM HERE DOWN ###

CODON_LEN = 3
#START_CODON = "ATG"
#STOP_CODONS = ["TAA", "TAG", "TGA"]

start_pattern = re.compile("ATG")
stop_pattern  = re.compile("(TAA)|(TAG)|(TGA)")

def find_all_ORFs(dna):
    """ Finds non-nested open reading frames in given DNA
    >>> find_all_ORFs("ATGAATTGA")
    ['ATGAAT']
    >>> find_all_ORFs("ATGTTGATGTAA")
    ['ATGTTGATG']
    >>> find_all_ORFs("ATGTATTGAAAAATGTATTAA")
    ['ATGTAT', 'ATGTAT']
    >>> find_all_ORFs("ATGA")
    ['ATGA']
    """

    i = 0
    ORFs = []
    done = False
    while (not done):
        start_index = find_start_codon(i, dna)
        stop_index  = find_stop_codon(start_index + CODON_LEN, dna)

        if start_index != len(dna):
                ORF = dna[start_index:stop_index]
                ORFs.append(ORF)
        else:
            done = True

        i = stop_index + 1

    return ORFs

def find_pattern(i, dna, pattern):

    match = pattern.search(dna, i)

    while True:

        if match:
            match_start = match.start()
            if match_start % CODON_LEN != 0:
                match = pattern.search(dna, match_start + 1)
            else:
                return match_start
        else:
            return len(dna)


def find_start_codon(i, dna):
    """ Finds the index of the first start
    codon after index i that is a multiple
    of three. If there is not one, 
    then we return the length of dna.
    >>> find_start_codon(0, "ATG")
    0
    >>> find_start_codon(1, "ATG")
    3
    >>> find_start_codon(0, "AATG")
    4
    >>> find_start_codon(0, "TAGATG")
    3
    """

    return find_pattern(i, dna, start_pattern)

def find_stop_codon(i, dna):
    """ Finds the index of the first stop
    codon after index i that is a multiple
    of three. If there is not one,
    then we return the length of dna.
    >>> find_stop_codon(0, "TAG")
    0
    >>> find_stop_codon(1, "TAG")
    3
    >>> find_stop_codon(0, "TTAA")
    4
    >>> find_stop_codon(3, "ATGTAG")
    3
    """

    return find_pattern(i, dna, stop_pattern)

def any_codons_remaining(i, dna):
    """ Determines if there are any full codons remaining
    >>> any_codons_remaining(0, "ATGGATTA")
    True
    >>> any_codons_remaining(3, "ATGGAT")
    True
    >>> any_codons_remaining(2, "ATGA")
    False
    """

    dna_len = len(dna)
    return i + CODON_LEN <= dna_len

def get_codon(i, dna):
    """ Retrives codon starting at index i
    >>> get_codon(0, "ATG")
    'ATG'
    >>> get_codon(3, "ATGTAT")
    'TAT'
    >>> get_codon(4, "AGTAT")
    ''
    """

    if any_codons_remaining(i, dna):
        return dna[i:i+CODON_LEN]
    return ""

def reverse_complement_dna(dna):
    """ Returns the reversed complement of the dna 
    >>> reverse_complement_dna("ATG")
    'CAT'
    >>> reverse_complement_dna("GATTACA")
    'TGTAATC'
    """

    dna = complement_dna(dna)
    return reverse_str(dna)

def reverse_str(str):
    """ Reverses a string
    >>> reverse_str("string")
    'gnirts'
    >>> reverse_str("")
    ''
    >>> reverse_str("A")
    'A'
    """

    if not str:
        return ""

    return reduce(lambda a, b: b + a, str)

def complement_dna(dna):
    """ Finds the complements of dna
    >>> complement_dna("ATG")
    'TAC'
    >>> complement_dna("GATTACA")
    'CTAATGT'
    """

    list = map(complement_nucleotide, dna)
    str = join_list(list)
    return str

def join_list(list):
    """ Reduces a list into a sigle entity
    >>> join_list(['a', 'b', 'c'])
    'abc'
    >>> join_list([1, 2, 3])
    6
    >>> join_list([(1, 2), (3, 4), (5, 6)])
    (1, 2, 3, 4, 5, 6)
    """

    return reduce(lambda acc, el: acc + el, list)

def complement_nucleotide(nucleotide):
    """ Finds the complement nucloetide
    >>> complement_nucleotide('A')
    'T'
    >>> complement_nucleotide('T')
    'A'
    >>> complement_nucleotide('G')
    'C'
    >>> complement_nucleotide('C')
    'G'
    >>> complement_nucleotide("foo")
    '?'
    """
    if nucleotide == 'A':
        return 'T'
    elif nucleotide == 'T':
        return 'A'
    elif nucleotide == 'G':
        return 'C'
    elif nucleotide == 'C':
        return 'G'
    else:
        return '?'



def find_all_ORFs_both_strands(dna):
    """ Finds all non-nested open reading frames in the given DNA sequence on both
        strands.
        
        dna: a DNA sequence
        returns: a list of non-nested ORFs
    >>> find_all_ORFs_both_strands("ATGCGAATGTAGCCATAAA")
    ['ATGCGAATG', 'ATGGCTACATTCGCAT']
    """

    orfs = []
    rc_dna = reverse_complement_dna(dna)

    orfs += find_all_ORFs(dna)
    orfs += find_all_ORFs(rc_dna)

    return orfs

def longest_ORF(dna):
    
    orfs = find_all_ORFs_both_strands(dna)
    return longest_in_list(orfs)

def longest_in_list(list):
    """ Returns the longest item in a list
    >>> longest_in_list(["a", "ab", "abc"])
    'abc'
    >>> longest_in_list([(1, 2, 3, 4, 5), (1, 2, 3), (1, 2)])
    (1, 2, 3, 4, 5)
    """

    return max(list, key = lambda item: len(item))

def longest_ORF_noncoding(dna, num_trials):
    """ Computes the maximum length of the longest ORF over num_trials shuffles
        of the specfied DNA sequence
        
        dna: a DNA sequence
        num_trials: the number of random shuffles
        returns: the maximum length longest ORF """
    # TODO: implement this
    pass

def coding_strand_to_AA(dna):
    """ Computes the Protein encoded by a sequence of DNA.  This function
        does not check for start and stop codons (it assumes that the input
        DNA sequence represents an protein coding region).
        
        dna: a DNA sequence represented as a string
        returns: a string containing the sequence of amino acids encoded by the
                 the input DNA fragment

        >>> coding_strand_to_AA("ATGCGA")
        'MR'
        >>> coding_strand_to_AA("ATGCCCGCTTT")
        'MPA'
    """
    # TODO: implement this
    pass

def gene_finder(dna, threshold):
    """ Returns the amino acid sequences coded by all genes that have an ORF
        larger than the specified threshold.
        
        dna: a DNA sequence
        threshold: the minimum length of the ORF for it to be considered a valid
                   gene.
        returns: a list of all amino acid sequences whose ORFs meet the minimum
                 length specified.
    """
    # TODO: implement this
    pass

if __name__ == "__main__":
    import doctest
    doctest.testmod()
