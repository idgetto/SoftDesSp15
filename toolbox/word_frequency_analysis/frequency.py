""" Analyzes the word frequencies in a book downloaded from
	Project Gutenberg """

import string
import re

HEADER_STRING = "START OF THIS PROJECT GUTENBERG EBOOK"

def header_string_regex():
	""" regex for the start of the book """
	return r'' + HEADER_STRING + '.*(?:\*){3}'

def ignored_punctuation_regex():
	""" regex for puctuation that can be removed """
	return r'[!\"#$%&()*+\,-./:;<=>?@\[\]\\^_`{}|~]+'

def strip_header(book):
	""" returns the book without the starting header 
	>>> strip_header("***" + HEADER_STRING + "***" + "some text")
	'some text'
	>>> strip_header("stuff" + "***" + HEADER_STRING + "***" + "other stuff")
	'other stuff'
	"""
	header_regex = header_string_regex()
	header_match = re.search(header_regex, book)

	header_end = 0
	if header_match:
		header_end = header_match.end()

	return book[header_end:]

def strip_punctuation(book):
	""" returns the book without punctuation
	>>> strip_punctuation("Luke, I am your father!")
	'Luke I am your father'
	>>> strip_punctuation("She's got $400.")
	"She's got 400"
	"""
	punc_regex = ignored_punctuation_regex()
	replace_regex = r''
	res, repls = re.subn(punc_regex, replace_regex, book)

	return res

def get_file_text(file_name):
	""" gets the text form a file """
	f = open(file_name, 'r')
	text = f.read()
	return text

def get_word_list(file_name):
	""" Reads the specified project Gutenberg book.  Header comments,
		punctuation, and whitespace are stripped away.  The function
		returns a list of the words used in the book as a list.
		All words are converted to lower case.
	"""
	book = get_file_text(file_name)
	book = strip_header(book)
	book = strip_punctuation(book)
	book = book.lower()
	words = re.split(r'\s+', book)
	return words

def get_word_frequencies(word_list):
	freqs = {}
	for word in word_list:
		freqs[word] = freqs.get(word, -1) + 1

	return freqs


def get_top_n_words(word_list, n):
	""" Takes a list of words as input and returns a list of the n most frequently
		occurring words ordered from most to least frequently occurring.

		word_list: a list of words (assumed to all be in lower case with no
					punctuation
		n: the number of words to return
		returns: a list of n most frequently occurring words ordered from most
				 frequently to least frequentlyoccurring
	"""
	freqs = get_word_frequencies(word_list)
	freq_words = sorted(freqs, key=freqs.get, reverse=False)
	return freq_words[:n]

def analyze_book(file_name):
	word_list = get_word_list(file_name)
	top_words = get_top_n_words(word_list, 10)
	return top_words

if __name__ == "__main__":
	import doctest
	doctest.testmod()

	print analyze_book('pg32325.txt')
