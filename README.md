# Usage des fonctions
## TP Zipf
Dans zipf.py, on a :
* freq_apparition(directory): prend en argument le répertoire contenant les fichiers CACM tonkenizés
* tri_dico(dico), display_top_10(dico), lambda_theorique(dico): prennent en argument une variable globale dico qui est un dictionnaire contenant les mots des fichiers
* plot_zipf(): fonctionne grâce aux données des fonctions précédentes
## TP Vocabulaire
Dans vocab.py on a : 
* filtrage(antidicopath, corpusdirectory): prend en argument le chemin de l'anti-dictionnaire ainsi que le chemin où nos fichiers tokenizés se trouvent
* vocab(path): prend en argument le chemin des fichiers résultants du filtrage précédemment effectué (là où l'on stocke nos .sttr)
* dfi(path): prend en argument le chemin des fichiers résultants du filtrage précédemment effectué (là où l'on stocke nos .sttr)
* idfi(): fonctionne sans arguments, avec les variables globales définies dans le fichier
* list_tf(path): prend en argument le chemin des fichiers résultants du filtrage précédemment effectué (là où l'on stocke nos .sttr)
* vecto(): fonctionne sans arguments, avec les variables globales définies dans le fichier
* indexinverse(): fonctionne sans arguments, avec les variables globales définies dans le fichier
## TP Recherche
Dans request.py on a : 
* request_loop() qui fonctionne avec les variable globales contenant les fichiers json résultants du TP Vocabulaire