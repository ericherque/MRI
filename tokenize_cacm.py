import os
from nltk.tokenize import RegexpTokenizer
directory = "cacm/split/"
outpathname = "cacm/split/tokenize/"

def ModifDesFichiers(inpathname, outpath) :
    for filename in os.listdir(inpathname):
        print("processing :" + inpathname + filename)
        if filename != ".DS_Store" and filename != "tokenize":
            # entrée
            f = open(inpathname+filename, "r")
            # sortie
            g = open(outpath + filename + ".flt", "w+")
            tokenizer = RegexpTokenizer('[A-Za-z]\w{1,}')

            for line in f:
                line.lower()
                words = tokenizer.tokenize(line)
                words.append("\n")
                for word in words:
                    g.write(word.lower())
                    if(word != '\n'):
                        g.write(" ")

ModifDesFichiers(directory,outpathname)