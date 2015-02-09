# -*- coding: utf-8 -*-
"""
 Created on Sun Feb  2 11:24:42 2014

@author: Isaac Getto

"""

# you may find it useful to import these variables (although you are not required to use them)
from amino_acids_less_structure import aa, codons
from amino_acids import aa_table
import random
from load import load_seq
import re
from itertools import imap
from itertools import ifilter
from itertools import repeat

### YOU WILL START YOUR IMPLEMENTATION FROM HERE DOWN ###

CODON_LEN = 3
ORF_REGEX = "^(?:.{3})*?(?P<orf>ATG(?:(?:.{3})*?(?=TAA|TAG|TGA)|.*$))"
orf_pattern = re.compile(ORF_REGEX)

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

def generic_sum(L):
    """ Reduces a list into a sigle entity
    >>> generic_sum(['a', 'b', 'c'])
    'abc'
    >>> generic_sum([1, 2, 3])
    6
    >>> generic_sum([(1, 2), (3, 4), (5, 6)])
    (1, 2, 3, 4, 5, 6)
    """
    return reduce(lambda acc, item: acc + item, L)

def find_all_ORFs(dna):
    """ Finds all non-nested open reading frames in given DNA
    >>> find_all_ORFs("ATGCATGAATGTAG")
    ['ATGCATGAATGTAG', 'ATGAATGTAG', 'ATG']
    """

    ORFs = imap(find_all_ORFs_one_frame, [dna, dna[1:], dna[2:]])
    return generic_sum(ORFs)

def find_all_ORFs_one_frame(dna):
    """ Finds non-nested open reading frames in given DNA
    >>> find_all_ORFs_one_frame("ATGAATTGA")
    ['ATGAAT']
    >>> find_all_ORFs_one_frame("ATGTTGATGTAA")
    ['ATGTTGATG']
    >>> find_all_ORFs_one_frame("ATGTATTGAAAAATGTATTAA")
    ['ATGTAT', 'ATGTAT']
    >>> find_all_ORFs_one_frame("ATGA")
    ['ATGA']
    >>> find_all_ORFs_one_frame("AATG")
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

    list = imap(complement_nucleotide, dna)
    str = generic_sum(list)
    return str

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

    if list:
        return max(list, key = len)

def longest_ORF_noncoding(dna, num_trials):
    """ Computes the maximum length of the longest ORF over num_trials shuffles
        of the specfied DNA sequence
        
        dna: a DNA sequence
        num_trials: the number of random shuffles
        returns: the maximum length longest ORF """

    dnas         = repeat(dna, num_trials);
    shuffled_dna = imap(shuffle, dnas)
    longest_ORFs = imap(longest_ORF, shuffled_dna)
    max_len      = len(longest_in_list(longest_ORFs))
    return max_len

def shuffle(str):
    list = random.sample(str, len(str))
    return generic_sum(list)

def convert_to_proteins(L):
    """ Convert each ORF to its protein sequence
    >>> list(convert_to_proteins(["ATG", "ATGTAT", "ATGGCC"]))
    ['M', 'MY', 'MA']
    """

    return imap(coding_strand_to_AA, L)

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

    stripped     = strip_extra(dna)
    codon_list   = split_codons(stripped)
    protein_list = imap(codon_to_protein, codon_list)
    proteins     = generic_sum(protein_list)
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

    protein = aa_table.get(codon)
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

    ORFs = find_all_ORFs_both_strands(dna)
    long_ORFs = keep_if_long(threshold, ORFs)
    return convert_to_proteins(long_ORFs)

def keep_if_long(length, list):
    """ Keeps the elements of a list that are greater or equal to the given length
    >>> list(keep_if_long(0, ["cat", "dog", "moose"]))
    ['cat', 'dog', 'moose']
    >>> list(keep_if_long(4, ["cat", "dog", "moose"]))
    ['moose']
    >>> list(keep_if_long(6, ["cat", "dog", "moose"]))
    []
    """

    return ifilter(lambda item: len(item) >= length, list)

if __name__ == "__main__":
    import doctest
    doctest.testmod()

    from load import load_seq
    dna = load_seq("./data/X73525.fa")

    threshold = 700
    genes = gene_finder(dna, threshold)
    print list(genes)
