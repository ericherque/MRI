import json
import os
import numpy as np
import math
from nltk.tokenize import RegexpTokenizer
from nltk.stem.porter import *

directory = "../cacm/split/tokenize/"
antidicofile = "../cacm/common_words"

outpath = "../cacm/filtrage/"

jsonpath = "../cacm/"

dico = {}
antidico = {}

vocabulaire = {}
dico_idfi = {}

list_tfid = []
dico_vecto = {}
dico_norme = {}
indexinversedico = {}


# init du dico et de l'antidico
def filtrage(antidicopath, corpusdirectory):
    # init de l'antidictionnaire
    f = open(antidicopath, "r")
    for line in f:
        antidico[line.rstrip("\n")] = 1

    stemmer = PorterStemmer()
    # fileindex = 1
    # traitement file par file des .flt
    for filename in os.listdir(corpusdirectory):
        print("processing :" + corpusdirectory + filename)

        # on remplit le dico pour chaque file
        g = open(corpusdirectory + filename, "r")
        tokenizer = RegexpTokenizer('[A-Za-z]\w{1,}')
        for line in g:
            words = tokenizer.tokenize(line)
            for w in words:
                if w in dico:
                    dico[w] += 1
                else:
                    dico[w] = 1

        # pour chaque dico on applique l'antidico = 1er filtrage
        for word in antidico:
            if dico.get(word) is not None:
                dico.pop(word)
                print(word, " deleted")

        # réduction des mots (troncature) = 2nd filtrage
        # écriture du fichier .sttr correspondant
        h = open(outpath + filename.rstrip(".flt") + ".sttr", "w+")
        for i in dico:
            print("initial word: ", i)
            racine = stemmer.stem(i)
            print("racine: ", racine)
            h.write(racine + "\n")

        # on clear le dico pour pouvoir traiter le prochain fichier
        dico.clear()


def vocab(path):
    # on remplit vocab en parcourant chaque .sttr
    for filename in os.listdir(path):
        print("processing :" + path + filename)
        f = open(path + filename, "r")
        for line in f:
            word = line.rstrip("\n")
            if vocabulaire.get(word) is None:
                vocabulaire[word] = 0
            else:
                vocabulaire[word] = 1

        # on écrit le fichier vocab de sortie
        jsonfile = open(jsonpath + "vocabulaire.json", "w+")
        jsonobject = json.dumps(vocabulaire, indent=4)
        jsonfile.write(jsonobject)
        jsonfile.close()


def dfi(path):
    samefile = False
    for filename in os.listdir(path):
        print("processing :" + path + filename)
        f = open(path + filename, "r")
        for line in f:
            word = line.rstrip("\n")
            if vocabulaire.get(word) is None:
                vocabulaire[word] = 0
            else:
                samefile = True
                vocabulaire[word] += 1
        samefile = False

    jsonobject = json.dumps(vocabulaire, indent=4)
    jsonfile = open(jsonpath + "vocabulaire.json", "w+")
    jsonfile.write(jsonobject)


def idfi():
    N = len(vocabulaire)

    for word in vocabulaire:
        if vocabulaire[word.rstrip("\n")] != 0:
            dico_idfi[word.rstrip("\n")] = np.log(N / vocabulaire[word.rstrip("\n")])
        # else:
        # dico_idfi[word.rstrip("\n")] = 0
    #return dico_idfi


def list_tf(path):
    dico_count = {}
    for filename in os.listdir(path):
        print("processing :" + path + filename)
        if filename != "vocabulaire.json":
            f = open(path + filename, "r")

            # fileindex = le numéro dans le nom du fichier
            fileindex = re.findall('\d+', filename)
            print("fileindex = ", int(fileindex[0]))

            # pour chaque ligne (donc mot) on l'ajout au dico d'occurences
            # ce dico sert à compter l'occurence d'un mot dans le fichier
            # le dico est réinitialisé à chaque itération

            for line in f:
                word = line.rstrip("\n")
                if word in dico_count:
                    dico_count[word] += 1
                else:
                    dico_count[word] = 1

            # une fois le dico rempli, on ajoute la liste [fileindex, mot, occurence] dans le liste
            for w in dico_count:
                list_tfid.append([int(fileindex[0]), w, dico_count[w]])

            dico_count.clear()


def vecto():
    print(" début vecto")
    # itération pour chaque numéro de document
    for i in range(1,3205):
        #on déclare le dico_doc ici pour le reset à chaque fois
        dico_doc = {}
        sum_carre = 0
        # itération pour chaque terme de la liste de liste
        for j in range(len(list_tfid)):
            triplet = list_tfid[j]
            # si le triplet appartient au même document, on traite
            if triplet[0] == i:
                w = triplet[2] * dico_idfi[triplet[1]] * 1
                dico_doc[triplet[1]] = w
                sum_carre += w*w
        dico_norme["CACM-"+str(i)] = math.sqrt(sum_carre)
        #on range le dictionnaire du i-ème doc dans le dictionnaire de dictionnaire
        dico_vecto["CACM-" + str(i)] = dico_doc

        json_object = json.dumps(dico_norme, indent=4)
        vocabFile = open(jsonpath + "norme.json", "w")
        vocabFile.write(json_object)
        vocabFile.close()



def indexinverse():
    for numdoc in dico_vecto:
        dico_doc = dico_vecto[numdoc]
        for terme in dico_doc:
            dico_documents = {}

            val = dico_doc[terme]
            dico_documents[numdoc] = val
            #print(dico_documents)
            if terme in indexinversedico:
                elt_dico = indexinversedico[terme]
                elt_dico.append([dico_documents])
                indexinversedico[terme] = elt_dico
            else:
                indexinversedico[terme] = []
                indexinversedico[terme].append([dico_documents])
    json_object = json.dumps(indexinversedico, indent=4)
    vocabFile = open(jsonpath+"indexinverse.json", "w")
    vocabFile.write(json_object)
    vocabFile.close(

# filtrage: on applique l'antidico + on tronque les termes (racine)
filtrage(antidicofile, directory)
# compte les occurences des termes tronqués
vocab(outpath)

# occurences des termes tronqués par fichiers dans vocabulaire.json
dfi(outpath)

# print(vocabulaire)

# question 4'
# print(idfi())
idfi()
########################################################################
# caractérisation du terme dans le document
# ptf = tf_ti
# ce le nombre de fois où le terme apparait dans LE document
# caractérisation du terme dans le corpus
# pdf = idf = ln(N/df_ti)
# dfi = res de la focntion dfi

# normalisation du vecteur
# nd = 1
########################################################################
# vectorisation: on traite pour chaque documents chaque mots


list_tf(outpath)

vecto()

indexinverse()
print(indexinversedico)
