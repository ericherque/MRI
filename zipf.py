import os
from nltk.tokenize import RegexpTokenizer
import numpy as np
import matplotlib.pyplot as plt

directory = "../cacm/split/tokenize/"
dico = {}

def freq_apparition(path) :
    for filename in os.listdir(path):
        print("processing :" + path + filename)
        f = open(path + filename, "r")
        tokenizer = RegexpTokenizer('[A-Za-z]\w{1,}')
        for line in f:
            words = tokenizer.tokenize(line)
            for w in words:
                if w in dico:
                    dico[w] += 1
                else:
                    dico[w] = 1
    for i in dico:
       print(i + " : " + str(dico[i]) + "\n")

def tri_dico(dico) :
    d = sorted(dico.items(), key=lambda x: x[1], reverse=True)
    print(d)

def display_top_10(dico):
    d = sorted(dico.items(), key=lambda x: x[1], reverse=True)
    i = 0
    for word, occur in d:
        i += 1
        print("#"+str(i), word, " : ", occur)
        if i == 10:
            break

# M
def occur_number(dico):
    res = 0
    for word in dico:
        res += dico[word]
    print(res)
    return res

def lambda_theorique(dico):
    # M
    a = occur_number(dico)
    print("number of total occurences: ", a)
    # M_y
    b = len(dico)
    print("numbers of words: ", b)

    # lambda = M / ln(M_y)
    lambdaa = a / (np.log(b))
    print("theorical lambda value: ", lambdaa)

def plot_zipf():
    tab_rang = [None] * 10956
    tab_occur_plot = [None] * 10956
    tab_occur = sorted(dico.items(), key=lambda x: x[1], reverse=True)

    print("debut du plot: ")

    for i in range(10955):
        # print(i)
        tab_rang[i] = i
        tab_occur_plot[i] = tab_occur[i][1]

    plt.plot(tab_rang, tab_occur_plot)

    # plt.plot([1,2,3],[13000, 10000, 6800])
    plt.plot()
    plt.show()

freq_apparition(directory)
# tri_dico(dico)
display_top_10(dico)
lambda_theorique(dico)
plot_zipf()



