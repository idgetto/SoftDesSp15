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

"""
                         =======================
                         == REGEX EXPLANATION ==
                         =======================


    ^                                       # beginning of string
        (?:.{3})*?                          # multiple of any three characters
        (?P<orf>                            # make a group called "orf"
            ATG                             # contains the start codon: ATG
            (?:
                (?:.{3})*?                  # multiple of any three characters
                        (?=TAA|TAG|TGA)     # there should be a stop codon after
                    |                       # or
                        .*                  # anything; this happens when there is no stop codon
            )
        )
    $                                       # end of string



"""

codon_protein_dict = { 
                        "TTT": "F", "TTC": "F", "TTA": "L", "TTG": "L",
                        "TCT": "S", "TCC": "S", "TCA": "S", "TCG": "S",
                        "TAT": "T", "TAC": "T",
                        "TGT": "C", "TGC": "C", "TGG": "W",

                        "CTT": "L", "CTC": "L", "CTA": "L", "CTG": "L",
                        "CCT": "P", "CCC": "P", "CCA": "P", "CCG": "P",
                        "CAT": "H", "CAC": "H", "CAA": "Q", "CAG": "Q",
                        "CGT": "R", "CGC": "R", "CGA": "R", "CGG": "R", 

                        "ATT": "I", "ATC": "I", "ATA": "I", "ATG": "M",
                        "ACT": "T", "ACC": "T", "ACA": "T", "ACG": "T",
                        "AAT": "N", "AAC": "N", "AAA": "K", "AAG": "K",
                        "AGT": "S", "AGC": "S", "AGA": "R", "AGG": "R", 

                        "GTT": "V", "GTC": "V", "GTA": "V", "GTG": "V",
                        "GCT": "A", "GCC": "A", "GCA": "A", "GCG": "A",
                        "GAT": "D", "GAC": "D", "GAA": "E", "GAG": "E",
                        "GGT": "G", "GGC": "G", "GGA": "G", "GGG": "G" 
                     }

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

def shuffle(str):
    list = random.sample(str, len(str))
    return join_list(list)

def convert_to_proteins(list):
    """ Convert each ORF to its protein sequence
    >>> convert_to_proteins(["ATG", "ATGTAT", "ATGGCC"])
    ['M', 'MT', 'MA']
    """

    return map(coding_strand_to_AA, list)


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

    stripped = strip_extra(dna)
    codon_list = split_codons(stripped)
    protein_list = map(codon_to_protein, codon_list)
    proteins = join_list(protein_list)
    return proteins

def split_codons(dna):
    """ Splits a dna strand into separate codons
    >>> split_codons("ATG")
    ['ATG']
    >>> split_codons("ATGTAA")
    ['ATG', 'TAA']
    >>> split_codons("")
    []
    """

    return split_codons_helper(dna, [])

def split_codons_helper(dna, acc):
    if not dna:
        return acc
    acc.append(dna[:3])
    return split_codons_helper(dna[3:], acc)


def codon_to_protein(codon):
    """ Convert codon to the corrosponding protein, 
    if there is no corrosponding protein, then return '?'
    >>> codon_to_protein("TTT")
    'F'
    >>> codon_to_protein("ATC")
    'I'
    >>> codon_to_protein("")
    '?'
    """

    protein = codon_protein_dict.get(codon)
    if (protein):
        return protein
    return "?" 

def strip_extra(dna):
    """ Strips any incomplete codons 
        off the end of a dna strand

        >>> strip_extra("ATG")
        'ATG'
        >>> strip_extra("ATGAA")
        'ATG'
        >>> strip_extra("ATGTAA")
        'ATGTAA'
        >>> strip_extra("ATGCCCGCTTT")
        'ATGCCCGCT'
        """

    str_len = len(dna)
    extra = str_len % 3
    return dna[:str_len - extra]

def gene_finder(dna, threshold):
    """ Returns the amino acid sequences coded by all genes that have an ORF
        larger than the specified threshold.
        
        dna: a DNA sequence
        threshold: the minimum length of the ORF for it to be considered a valid
                   gene.
        returns: a list of all amino acid sequences whose ORFs meet the minimum
                 length specified.
    """

    ORFs = find_all_ORFs_both_stands(dna)
    long_ORFs = keep_if_long(threshold, list)
    return convert_to_proteins(list)

def keep_if_long(length, list):
    """ Keeps the elements of a list that are greater or equal to the given length
    >>> keep_if_long(0, ["cat", "dog", "moose"])
    ['cat', 'dog', 'moose']
    >>> keep_if_long(4, ["cat", "dog", "moose"])
    ['moose']
    >>> keep_if_long(6, ["cat", "dog", "moose"])
    []
    """

    return filter(lambda item: len(item) >= length, list)
if __name__ == "__main__":
    import doctest
    doctest.testmod()
