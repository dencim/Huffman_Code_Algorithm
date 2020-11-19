# -*- coding: utf-8 -*-
"""
Huffman Code Generator
Takes in a txt file name (String) 
Returns a Dictionary with an optimized character encoding based on num of occurences

@author: Denis
"""
import fileinput 

#Node class being used to store sums and Node or Leaf children
class Node:
    def __init__(self, left, right):
        self.left = left
        self.right = right
        self.value = left.getValue() + right.getValue()
    
    def getValue(self):
        return self.value
    
    def getLeftChild(self):
        return self.left
    
    def getRightChild(self):
        return self.right
        
#Leaf class used to store Leaf Nodes (letters and occurence)
class Leaf:
    def __init__(self, letter, value):
        self.letter = letter
        self.value = value
    
    def getLetter(self):
        return self.letter
        
    def getValue(self):
        return self.value

'''
Takes in a file name and outputs optimal binary encoding for letters based 
on occurences as well as a dictionary of letters and the number of occurences
'''
def huffman_code(file_name):
    file = fileinput.FileInput(files =file_name)
    
    values_dict = dict()
   
    #Creating dictionary with occurences of each letter
    for line in file:
        for letter in line:
            
            if letter in values_dict:
                values_dict[letter] = values_dict[letter] + 1
            else:
                values_dict[letter] = 1
    
    file.close()
    #print(values_dict)
    
    values = []
    
    #Making a list of Leaf classes
    for key in values_dict:
        #print(key, '->', values_dict[key])
        values.append(Leaf(key, values_dict[key]))
        
     
        
    #Using Occurences to calculate optimal prefix codes using Huffman Algo
    
    getValueFunction = lambda x: x.getValue() #Aid for sorting function for list
    
    while(len(values) > 1):
        
        values.sort(key=getValueFunction)
        
        left = values[0]
        right = values[1]
            
        parent = Node(left, right)
        
        values = values[2:]
        
        values.insert(0, parent)

    
    return find_encoding(values), values_dict


#takes in a list of Nodes and returns a Dictionary of optimal binary char encodings
def find_encoding(values):
    
    final_encoding = dict()
    
    current = [values[0]] #will be used like stack for tree traversal -> start with tree root
    
    encoding = ""
    #traverse tree with depth first search to find all leaves -> Using stack
    while len(current) > 0:
        
        if type(current[-1]).__name__ == 'Leaf':
            #insert enc into dict
            final_encoding[current[-1].getLetter()] = encoding
            current = current[:-1]
            encoding = encoding[:-1]
        else:
            if current[-1].getLeftChild() != None:
                left = current[-1].getLeftChild()
                current[-1].left = None
                current.append(left)
                encoding = encoding + "0" #Going left
            elif current[-1].getRightChild() != None:
                right = current[-1].getRightChild()
                current[-1].right = None
                current.append(right)
                encoding = encoding + "1" #going right
            else:
                current = current[:-1]
                encoding = encoding[:-1]
    return final_encoding

#Compares encoding letters with a fixed length vs variable length
def before_and_after(codes, occurences):
    
    #Fixed length -> Assuming 8 bit encoding (Size of byte)
    
    total_fixed = 0
    for key in occurences:
        total_fixed = total_fixed + occurences[key] * 8
    
    print("Fixed length: ", total_fixed)
    
    
    #Variable length -> Using encoding calculated from Huffman Code function
    
    total_variable = 0
    for key in occurences:
        total_variable = total_variable + occurences[key] * len(codes[key])
    
    print("Variable length: ", total_variable)
    
    print("Memory saved: ", total_fixed - total_variable, " bits")
    
    
    
#Testing Code
optimum_codes, occurences = huffman_code("test.txt")
    
print("Number of occurences:\n", occurences, "\n")
print("Optimum Binary encoding for each letter:\n", optimum_codes, "\n")

before_and_after(optimum_codes, occurences)
