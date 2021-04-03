import os
import json
from nltk.tokenize import RegexpTokenizer
from nltk.tokenize import RegexpTokenizer
from nltk.stem.porter import *
import math
from operator import itemgetter
import numpy as np
import operator

vocabpath = "../cacm/vocabulaire.json"
normepath = "../cacm/norme.json"
indexinversepath = "../cacm/indexinverse.json"

def request_loop():
    ## chargement vocab
    fv = open(vocabpath, "r")
    dict_vocab = json.load(fv)
    fv.close()
    ## chargement normes
    fn = open(normepath, "r")
    dict_norme = json.load(fn)
    fn.close()
    ## chargement index inversé
    fii = open(indexinversepath, "r")
    dict_indexinverse = json.load(fii)
    fii.close()

    ## Boucle de traitement des requêtes
    while(True):
        ## recup input user
        request = str(input("Enter request: "))

        ## creation list de mots de la request
        request_tab = request.split(" ")

        ## calcul du tfi dans dico_vocab_req
        dico_vocab_req = {}
        for word in request_tab :
            if word not in dico_vocab_req :
                dico_vocab_req[word] = 1
            else :
                dico_vocab_req[word] += 1

        ## calcul du idf dans dico_idf_req
        dico_idfi_req = {}
        N = 3204
        for word in dico_vocab_req :
            dico_idfi_req[word] = np.log(N/dico_vocab_req[word])

        ## calcul du vecteur de la requete
        dico_vec_req = {}
        for word in dico_vocab_req :
            dico_vec_req[word] = dico_idfi_req[word]*dico_vocab_req[word]

        ## calcul de la norme de la requete
        sum_carre = 0
        for word in dico_vec_req :
            sum_carre += pow(dico_vec_req[word], 2)
        norme_req = math.sqrt(sum_carre)


        ## traitement de la requete calcul de res_partiel
        res_partiel = {}
        for word in request_tab:
            if dict_indexinverse.get(word) is not None:
                dico_terme = dict_indexinverse[word]
                for i in range(len(dico_terme)):
                    list_dico_terme_doc = dico_terme[i]
                    dico_terme_doc = list_dico_terme_doc[0]
                    score = 0
                    for numdoc, value in dico_terme_doc.items():
                        # produit scalaire ?
                        score = value * dico_vec_req[word]
                        if numdoc in res_partiel:
                            res_partiel[numdoc] += score
                        else:
                            res_partiel[numdoc] = score
        ## res final
        res = {}
        for numdoc in res_partiel:
            ## modif des valeurs de res par /(norme de d * norme de q)
            res[numdoc] = res_partiel[numdoc] / (dict_norme[numdoc] * norme_req)

        ## tri ordre décroissant
        sorted_d = dict(sorted(res.items(), key=operator.itemgetter(1), reverse=True))

        # K premiers resultats
        # k = 4
        resultat_requete = list(sorted_d.items())[:4]

        ## affichage res
        for elt in resultat_requete:
            print(elt)


request_loop()





