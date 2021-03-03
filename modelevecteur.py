import os
import json
from nltk.tokenize import RegexpTokenizer
from nltk.tokenize import RegexpTokenizer
from nltk.stem.porter import *
import math
from operator import itemgetter
import numpy as np

vocabpath = "../cacm/vocabulaire.json"
normepath = "../cacm/norme.json"
indexinversepath = "../cacm/indexinverse.json"

def request_loop():
    fv = open(vocabpath, "r")
    dict_vocab = json.load(fv)
    fv.close()
    fn = open(normepath, "r")
    dict_norme = json.load(fn)
    fn.close()
    fii = open(indexinversepath, "r")
    dict_indexinverse = json.load(fii)
    fii.close()

    while(True):
        request = str(input("Enter request: "))
        request = request.split(" ")

        #calcule du tfi dans dico_vocab_req
        dico_vocab_req = {}
        for word in request :
            if word not in dico_vocab_req :
                dico_vocab_req[word] = 1
            else :
                dico_vocab_req[word] += 1

        #calcule du idf dans dico_idf_req
        dico_idfi_req = {}
        N = len(dico_vocab_req)
        for word in dico_vocab_req :
            dico_idfi_req[word] = np.log(N/dico_vocab_req[word])

        #calcule du vecteur de la requete
        dico_vec_req = {}
        for word in dico_vocab_req :
            dico_vec_req[word] = dico_idfi_req[word]*dico_vocab_req[word]

        #calcule de la norme de la requete
        sum_carre = 0
        for word in dico_vec_req :
            sum_carre += dico_vec_req[word]*dico_vec_req[word]
        norme_req = math.sqrt(sum_carre)




        #Traitement de la requete calcule de res_partiel
        res_partiel = {}
        for terme in dict_indexinverse :
            for word in dico_vocab_req :
                if (word == terme) :
                    dico_vec_doc = dict_indexinverse[terme]
                    ligne_trave = {}
                    for name_doc in dico_vec_doc :
                        ligne_trave[name_doc] = ligne_trave[name_doc]*dico_vec_req[word]
                        if name_doc not in res_partiel :
                            res_partiel[name_doc] = ligne_trave[name_doc]
                        else :
                            res_partiel[name_doc] += ligne_trave[name_doc]

        #Calcule du produit scalaire
        for name_doc in res_partiel :
            res_partiel[name_doc] = res_partiel/dict_norme[name_doc]*norme_req

        print(sorted(res_partiel.items(), key=itemgetter(1)))


request_loop()





