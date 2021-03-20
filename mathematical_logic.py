import pandas as pd
from itertools import product

#Syntax definition: a sentence is a string satisfying the following forms:
#1) (a) is a sentence where a is a letter
#2) (~(s)) is a sentence where ~ is not and s is a sentence
#3) ((s)o(t)) is a sentence where o is either &(and) or |(or) and s and t are sentences
#example syntax: (((a)&(b))&(~((c)|(d)))

#Note: the conditional and biconditional can be expressed in terms of the basic operators, so they are omitted.

def substitute(sentence, l): #substitute takes a sentence and a list of boolean values and returns the sentence with booleans substituted for atoms
    atoms = sorted(set([x for x in sentence if x.isalpha()])) #separates atoms from sentence
    for i in range(len(atoms)):
        sentence = sentence.replace(atoms[i], str(l[i])) #substitutes booleans for atoms
    return(sentence)

def pop_operator(sentence): #pop_operator takes a sentence and returns the top-level boolean operation
    level = 0 #initializes level
    index = 0 #initializes index
    while index < len(sentence): #loops through sentence
        if level == 1 and sentence[index] != '(': #prevents returning the first bracket
            if sentence[index] == '&': #we replace the shorthands with the full operator
                return ('and', index) 
            else:
                return ('or', index)
        elif sentence[index] == '(': #we go up one level
            level += 1
            index += 1
        elif sentence[index] == ')': #we go down one level
            level -= 1
            index += 1
        else: #level stays the same
            index += 1
    
def eval_sentence(sentence): #eval_sentence takes a sentence and returns its logical value
    if sentence == '(0)':
        return 0 
    elif sentence == '(1)':
        return 1   
    elif sentence[1] == '~':
        return(int(not eval_sentence(sentence[2:-1]))) #we negate the inner expression
    else: 
        return(eval(str(eval_sentence(sentence[1:pop_operator(sentence)[1]])) + ' ' + #first part of upper-level expression
               str(pop_operator(sentence)[0]) + ' ' + #operator
               str(eval_sentence(sentence[pop_operator(sentence)[1] + 1: -1])))) #second part of upper-level expression

def truth_row(sentence): #truth_row takes a sentence and replaces all operators with the truth-values of their expressions
    if sentence == '(0)':
        return '(0)'
    elif sentence == '(1)':
        return '(1)'  
    elif sentence[1] == '~':
        return('(' + 
               str(int(not eval_sentence(sentence[2:-1]))) + 
               truth_row(sentence[2:-1]) +
              ')')
    else: 
        return('(' + 
               truth_row(sentence[1:pop_operator(sentence)[1]]) + 
               str(eval_sentence(sentence)) + 
               truth_row(sentence[pop_operator(sentence)[1] + 1: -1]) +
               ')')
    
def listify(truth_row): #listify takes a sentence and returns the list of atoms
    return [x for x in list(truth_row) if str(x) != '(' and str(x) != ')']
    
               
def truth_table(sentence): #prints truth table
    values = [listify(truth_row(substitute(sentence, x))) for x in product([0,1], repeat=len(set([x for x in sentence if x.isalpha()])))]
    return pd.DataFrame(values,columns=listify(sentence))

#We define an argument as a list of sentences, all but the last being premises and the last being the conclusion.

def eval_argument(argument, l): #eval_argument outputs the list of truth values for an argument for a list of boolean l
    return [eval_sentence(substitute(x, l)) for x in argument]
    
def validate(argument):
    no_of_atoms = len(set([x for x in ''.join(argument) if x.isalpha()])) #counts number of atoms
    values = [eval_argument(argument, x) for x in product([0,1], repeat=no_of_atoms)] #evaluates all possible truth values of argument
    if [1 for x in range(len(argument) - 1)]+[0] in values: #if premises are true and conclusion is false, the argument is invalid
        print("Your argument is invalid, go check it again!")
    else: #otherwise the argument is valid
        print("Your argument is valid, congratulations!")  

truth_table("((~((a)|(b)))&((c)|(d)))")

validate(["((a)|(b))", "((~(a))|(b))", "((a)&(b))"])

#Note: all arguments must contain all atoms: if a sentence s does not contain an atom a, simply use the sentence (((~(a))&(a))|s).
