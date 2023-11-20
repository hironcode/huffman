"""
This project reads a file and creates variable-length and fixed-length binary codes,
and interpret the code into the original text.
You can compare the file size of the two kinds of binarycode files
"fixed_binary-encoding.txt" and "huffman_binary-encoding.txt" to see the difference in length of two binary codes.
The implementation of the Huffman binarycode tree references
the Geeks-for-Geeks python code: https://www.geeksforgeeks.org/huffman-coding-greedy-algo-3/
"""

import heapq
import time
import datetime
import random


def create_random_file(filename='FinProj_Huffman_RandomText.txt'):
    """This function creates a file with randomly selected 500000 alphabets"""
    text = ''
    for i in range(5000):
        # if the iteration is multiple of 50, change a line
        if i != 0 and i % 50 == 0:
            text += '\n'
            continue
        # otherwise, randomly select an alphabet based on unicode
        # and add it to the sequence of alphabets
        text += chr(random.randint(97, 122))
    # transcript the text to a new file
    with open(filename, 'w') as f:
        f.write(text)


def loadfile(filename):
    """This function reads the original text from a txt file
    and returns a list of lines and a dict of characters and their corresponding frenquency"""
    with open(filename, 'r') as file:
        lines = file.readlines()
        characters = set()
        # split each line into characters and add them to the set
        for line in lines:
            for character in line:
                characters.add(character)
        # place the characters from the set into a dictionary and initialize the corresponding frequency as 0
        symbols = {i: 0 for i in characters}
        # scan through every single character of each line and increment the frequency by 1
        for line in lines:
            for character in line:
                symbols[character] += 1
    return lines, symbols


class node:
    """This class is a node of the Huffman's binarycode tree.
    Referenced from Geeks-for-Geeks, URL is at the top of this file"""
    def __init__(self, weight, symbol, right=None, left=None):
        self.weight = weight    # frequency
        self.symbol = symbol    # an alphabet or symbol
        self.right = right  # the root of the right subtree of this node
        self.left = left    # the root of the left subtree of this node
        self.code = ''  # binarycode for this node

    def __lt__(self, child):
        # for inequality operations with another node object
        return self.weight < child.weight


def huffman_tree(symbols: dict):
    """This funciton bulids a Huffman binarycode tree with bottom-up approach using the node class
    Referenced from Geeks-for-Geeks, URL is at the top of this file"""
    # creates a list of nodes with frequency and symbol from the symbols dict
    htree = [node(w, s) for s, w in symbols.items()]
    # heapify the list to always pick up the least frequent symbol
    heapq.heapify(htree)
    while len(htree) > 1:   # until the symbols are merged into one big tree
        left = heapq.heappop(htree)     # the root of the left subtree (or a symbol) with the (first) least frequency
        right = heapq.heappop(htree)    # the root of the right subtree (or a symbol) with the (second) least frequency
        left.code = 0   # a bit for the root of the left subtree (or a symbol)
        right.code = 1  # a bit for the root of the right subtree (or a symbol)
        # merge the subtrees (or symbols) into one small tree with connected symbols (like "abde")
        # and aggregate frequency. Push a node with the aggregate frequency, the combined symbol,
        # the right subtree (symbol), and the left subtree (or symbol) into the htree list
        heapq.heappush(htree, node(left.weight+right.weight, left.symbol + ' , ' + right.symbol, right, left))
    return htree


def fixed_tree(symbols: dict):
    """This funciton bulids a naive fixed binarycode binary tree with bottom-up approach using the node class"""
    # place all the symbols into a list with no distinct frequencies (so tentatively set as 0)
    ftree = [node(0, s) for s in symbols.keys()]
    while len(ftree) > 1:   # until the symbols are merged into one big tree
        left = ftree.pop(0)     # pick up the left subtree (or symbol)
        right = ftree.pop(0)    # pick up the right subtree (or symbol)
        left.code = 0   # a bit for the root of the left subtree (or a symbol)
        right.code = 1  # a bit for the root of the right subtree (or a symbol)
        # merge the subtrees (or symbols) into one small tree with connected symbols (like "abde")
        # Push a node with the combined symbol,
        # the right subtree (symbol), and the left subtree (or symbol) into the htree list
        ftree.append(node(0, left.symbol + ' , ' + right.symbol, right, left))
    return ftree


def update_binary_dict(node: node, binarycode='', status='huffman'):
    """This function recursively fills in a dict with symbols and corresponding binary codes
        A modified approach from Geeks-for-Geeks, URL is at the top of this file"""
    new_code = binarycode + str(node.code)  # add the new bit of the node given
    # recursively add the bit of the root of the left subtree (or symbol)
    if node.left:
        update_binary_dict(node.left, new_code, status)
    # recursively add the bit of the root of the right subtree (or symbol)
    if node.right:
        update_binary_dict(node.right, new_code, status)
    # if there is no left or right subtrees, or the node is a leaf of the tree
    if not node.left and not node.right:
        # if this function is building a Huffman binarycode dictionary
        # insert a symbol and its corresponding binarycode into the huffman dict
        if status == 'huffman':
            huffman_binary_dict[node.symbol] = new_code
        # if this function is building a fixed binarycode dictionary
        # insert a symbol and its corresponding binarycode into the fixed binarycode dict
        elif status == 'fixed':
            fixed_binary_dict[node.symbol] = new_code


def get_huff_binary_code(lines:list):
    """This function converts the original text into a sequence of the huffman binarycode"""
    binary_code = ''
    # for each character, get its Huffman binarycode and add it to the sequence of binarycode
    for line in lines:
        for character in line:
            binary_code += huffman_binary_dict[character]
    return binary_code


def get_fixed_binary_code(lines:list):
    """This function converts the original text into a sequence of the fixed-length binarycode"""
    binary_code = ''
    # for each character, get its fixed-length binarycode and add it to the sequence of binarycode
    for line in lines:
        for character in line:
            binary_code += fixed_binary_dict[character]
    return binary_code


def interpret(binary_code:str, binary_dict_swapped:dict, status):
    """This function converts a sequence of binarycode into the original text"""
    p = 1
    text = ''
    print(f'start!: {datetime.datetime.now()}')
    start_time = time.perf_counter()    # start timing
    # scan through the binary code bit by bit and see if the set is in the dictionary
    while len(binary_code) >= 1:
        code = binary_code[:p]
        # if the binary code is in dict, add the character to the sequence of symbols
        if code in binary_dict_swapped:
            text += binary_dict_swapped[code]
            binary_code = binary_code[p:]   # update the binarycode sequence by cutting of the part already interpreted
            p = 1   # reset the position of the pointer
        # if the binarycode picked up in this iteration is not in the dict, move the pointer to the right
        elif code not in binary_dict_swapped:
            p += 1
    end_time = time.perf_counter()  # finish timing
    print(f'encoding time = {end_time - start_time} Seconds')   # show the runtime
    # trapnscripts the text onto a respective file
    if status == 'huffman':
        with open('huffman_encoding.txt', 'w') as f:
            f.write(text)
    elif status == 'fixed':
        with open('fixed_encoding.txt', 'w') as f:
            f.write(text)


def correction(newfilename, init_filename):
    """This program checks if the encoded text is the same as the original one"""
    # open the original file and the file created in the interpret function
    with open(init_filename, 'r') as f1, open(newfilename, 'r') as f2:
        lines1 = f1.readlines()
        lines2 = f2.readlines()
        if lines1 == lines2:    # if the files are identical, print so
            print("Correctly encoded the original text!")
        else:
            # if not, print so
            print("Something is wrong! Icorrectly encoded the original text!")
            # check through lines from these and print them out if different
            for line1, line2 in zip(lines1, lines2):
                if line1 != line2:
                    print(f'{line1}\n\n|||||||||||\n\n{line2}\n----------')


def huffman(filename):
    """This function perform the huffman binarycode operations"""
    # get the text and characters with frequencies
    lines, symbols = loadfile(filename)
    # get a list with one node representing a big tree
    hufftree = huffman_tree(symbols)
    # define a global dictionary of Huffman binarycode
    global huffman_binary_dict
    huffman_binary_dict = {}
    # recursively check through the node representing a tree and get a dictionary of symbols and Huffman binarycodes
    update_binary_dict(hufftree[0], status='huffman')
    # get a sequence of Huffman binarycodes representing the orignal text
    huff_binary_code = get_huff_binary_code(lines)
    # transcript the binarycode onto a file
    with open('huffman_binary-encoding.txt', 'w') as f:
        f.write(huff_binary_code)
    # swap the keys and values of the Huffman binarycode dictionary for convenience
    huffman_binary_dict_swapped = {v: k for k, v in huffman_binary_dict.items()}
    print('\n------------------------')
    # convert the binarycode into a text and transcript it on a file
    interpret(huff_binary_code, huffman_binary_dict_swapped, status='huffman')
    # check if the conversion is correct
    correction('huffman_encoding.txt', init_filename=filename)
    print('------------------------\n')


def fixed(filename):
    """This function perform the huffman binarycode operations"""
    # get the text and characters with frequencies
    lines, symbols = loadfile(filename)
    # get a list with one node representing a big binary tree
    hufftree = fixed_tree(symbols)
    # define a global dictionary of fixed-length binarycode
    global fixed_binary_dict
    fixed_binary_dict = {}
    # recursively check through the node representing a tree
    # and get a dictionary of symbols and fixed-length binarycodes
    update_binary_dict(hufftree[0], status='fixed')
    # get a sequence of Huffman binarycodes representing the orignal text
    fixed_binary_code = get_fixed_binary_code(lines)
    # transcript the binarycode onto a file
    with open('fixed_binary-encoding.txt', 'w') as f:
        print(fixed_binary_code, file=f)
    # swap the keys and values of the fixed-length binarycode dictionary for convenience
    fixed_binary_dict_swapped = {v: k for k, v in fixed_binary_dict.items()}
    print('\n------------------------')
    # convert the binarycode into a text and transcript it on a file
    interpret(fixed_binary_code, fixed_binary_dict_swapped, status='fixed')
    # check if the conversion is correct
    correction('fixed_encoding.txt', init_filename=filename)
    print('------------------------\n')


def main():
    # ask if the user has a file to process
    filename = input("Enter the filename, if no, enter No: ")
    # if the input is "no", process the existing file and text
    huffman(filename=filename)
    fixed(filename=filename)
    with open(filename, 'r') as f:
        lines = f.readlines()
    count_original = 0
    for line in lines:
        count_original += len(line)
    count_original *= 8

    with open('huffman_binary-encoding.txt', 'r') as f:
        lines = f.readlines()
    count_huffman_binary = 0
    for line in lines:
        count_huffman_binary += len(line)

    with open('fixed_binary-encoding.txt', 'r') as f:
        lines = f.readlines()
    count_fixed_binary = 0
    for line in lines:
        count_fixed_binary += len(line)
    print("ORIGINAL")
    print(f'{count_original} bits')
    print('=============')
    print("HUFFMAN BINARY")
    print(f'{count_huffman_binary} bits | {count_huffman_binary / count_original * 100} % of the original')
    print('=============')
    print("FIXED BINARY")
    print(f'{count_fixed_binary} bits | {count_fixed_binary / count_original * 100} % of the original')


if __name__ == '__main__':
    main()