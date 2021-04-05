import os
import json
from nltk.tokenize import RegexpTokenizer
from nltk.tokenize import RegexpTokenizer
from nltk.stem.porter import *
import math
from operator import itemgetter
import numpy as np
import operator

# définir le chemin où on sotcke les fichiers json issu du TP précédent
#vocabpath = "../cacm/vocabulaire.json"
#normepath = "../cacm/norme.json"
#indexinversepath = "../cacm/indexinverse.json"

# fichiers json fournis par nous même
vocabpath = "json/vocabulaire.json"
normepath = "json/norme.json"
indexinversepath = "json/indexinverse.json"

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
        k = str(input("Number of documents: "))

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


        ## tritement de la requete calcul de res_partiel
        ## pour chaque mots, on parcours les fichiers le contenant
        ## on calcule le score qui est égal au:
        ## tf.idf du mot dans la requête * tf.idf du mot dans le fichier
        res_partiel = {}
        for word in request_tab:
            if dict_indexinverse.get(word) is not None:
                dico_terme = dict_indexinverse[word]
                for i in range(len(dico_terme)):
                    # on récupère une liste contenant un dico contenant 1 CACM et 1 tf.idf
                    list_dico_terme_doc = dico_terme[i]
                    # on extrait le dico contenant CACM-X: tf.idf
                    # puis on traite cette donnée dans la boucle
                    dico_terme_doc = list_dico_terme_doc[0]
                    score = 0
                    for numdoc, value in dico_terme_doc.items():
                        # produit scalaire : ligne trav : tf.idf * tf.idf
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
        if(int(k)>len(sorted_d)):
            resultat_requete = list(sorted_d.items())[:int(len(sorted_d))]
        else:
            resultat_requete = list(sorted_d.items())[:int(k)]

        ## affichage res
        if len(resultat_requete)==0:
            print("no results...")
        else:
            pertinence = {}
            max = 0
            for value in resultat_requete[0]:
                max = value

            i=0
            for numdoc, value in resultat_requete:
                pertinence[i] = value / max
                i += 1

            print("results: ")
            count = 0
            for elt in resultat_requete:
                if pertinence[count]>=0.75:
                    print(elt, " ~ ++++")
                elif pertinence[count]>=0.50:
                    print(elt, " ~ +++")
                elif pertinence[count]>=0.25:
                    print(elt, " ~ ++")
                else:
                    print(elt, " ~ +")
                count += 1


request_loop()





