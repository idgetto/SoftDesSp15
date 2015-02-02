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
orf_pattern = re.compile("^(?:.{3})*?(?P<orf>ATG(?:(?:.{3})*?(?=TAA|TAG|TGA)|.*$))")

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
    >>> find_all_ORFs("AATG")
    []
    """

    ORFs = []
    match = orf_pattern.search(dna)

    while match:
        dict = match.groupdict()
        orf = dict.get("orf")
        ORFs.append(orf)

        dna = dna[match.end():] # remove matched part of dna
        match = orf_pattern.search(dna)

    return ORFs

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
