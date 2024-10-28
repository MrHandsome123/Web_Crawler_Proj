import sys


# Part A
def tokenizer(TextFilePath):

    """
    Tokenizer function: O(n) time complexity
    The function processes each character in the file exactly once, 
    making the runtime linear relative to the size of the file.
    """
    try:
        tokens = []
        current_token = []
        with open(TextFilePath, 'r') as file:

            for line in file:
                for char in line.lower():
                    if char.isalnum():
                        current_token.append(char)
                    elif current_token:
                        tokens.append("".join(current_token))
                        current_token = [] 

        if current_token:
            tokens.append("".join(current_token))      
        return tokens
    except FileNotFoundError:
        print(f"The file {TextFilePath} does not exsit. Please Provide valid path!")
        return []
    except UnicodeDecodeError:
        print(f"Unable to decode file {TextFilePath}. It may contain non-UTF-8 characters.")
        return []

def computeWordFrequencies(tokenList):
    """
    Compute word frequencies function: O(n) time complexity
    The function iterates over the list of tokens once, updating the frequency count for each token.
    """
    wordFrequencies = {}
    for str in tokenList:
        if str in wordFrequencies:
            wordFrequencies[str] += 1
        else:
             wordFrequencies[str] = 1
    return wordFrequencies

def printWordFrequencies(wordFrequencies):

    """
    Print word frequencies function: O(n) time complexity
    The function iterates over the dictionary of word frequencies once.
    """


    for key, value in wordFrequencies.items():
        print(f"{key} = {value}")
        

    

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python PartA.py <file>")
        sys.exit(1)
    file1 = sys.argv[1]

    tokens = tokenizer(file1)
    wordFrequencies = computeWordFrequencies(tokens)
    printWordFrequencies(wordFrequencies)