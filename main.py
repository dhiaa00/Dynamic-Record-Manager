from pickle import dumps, loads
from sys import getsizeof
global b #Nombre maximal d'enregistrement dans le buffer ou le bloc
global tnom #La taille du champ Nom
global tprénom #La taille du champ Prénom
global tmat #La taille du champ Matricule
global tniveau #La taille du champ Niveau
global tsupprimer #La taille du champ indiquant l'effacement logique de l'enregistrement
global bufsize #La taille dubfuffer ou du bloc
b = 10
tmat = 20
tnom = 20
tprenom = 20
tniveau = 10
tsupprimer = 1
etud1 = '#' * (tmat + tnom + tprenom + tniveau + tsupprimer)
buf = [0, [etud1] * b] #Utilisé pour le calcul de la taille du buffer
bufsize = getsizeof(dumps(buf)) + (len(etud1) + 1) *  (b - 1) #Formule de calcul de la taille du buffer

def resize_chaine(chaine, maxtaille):
    """Fonction de redémentionnement des champs de l'enregistrement afin de ne pas avoir des problèmes de taille"""
    for i in range(len(chaine),maxtaille):
        chaine = chaine + '#' 
    return chaine

def Creer_fichier():
    """ Procédure de création d'un fichier binaire"""
    fn = input("Donner le nom du fichier : ")
    j = 0 #Parcours des enregistrement
    i = 0 #Parcours des blocs
    n = 0 #Nombre des enregistrements
    #initialisation du buffer : 
    buf_tab = [etud1]*b
    buf_nb = 0 #buf_nb représente le nombre d'enregistrements dans le bloc
    try:
        f = open(fn, "wb")
    except:
        print("Creation du fichier est impossible ")
    rep = 'O'
    while (rep.upper() == 'O'):
        #Lecture des information :
        Nom = input('Donner le nom : \n')
        Prenom = input('Donner le prenom : \n')
        Matricule = input('Donner le matricule : \n')
        Niveau = input('Donner le niveau : \n')
        #Redémentionnement des informations : 
        Matricule = resize_chaine(Matricule, tmat)
        Nom = resize_chaine(Nom, tnom)
        Prenom = resize_chaine(Prenom, tprenom)
        Niveau = resize_chaine(Niveau, tniveau)
        #Enregistrement sous-forme d'une chaine de caractères
        Etud = Matricule + Nom + Prenom + Niveau + '0' #'0' pour non-supprimé
        n += 1 #Augmenter le nombre d'enregistrement
        if(j < b): #bloc non-plain
            buf_tab[j] = Etud
            buf_nb += 1 #Augmenter le nombre d'enregistrement
            j += 1
        else: #bloc plain
            buf=[buf_nb, buf_tab]
            ecrireBloc(f, i, buf) #Ecrire le bloc dans le fichier
            buf_tab=[etud1] * b #Créer un nouveau bloc
            #Mettre dans le bloc le nouveau enregistrement
            buf_nb = 1 
            buf_tab[0] = Etud
            j = 1
            i += 1 #Augmenter le nombre de blocs
        rep = input("Un autre étudiant à ajouter O/N ? ")
    buf=[j,buf_tab]
    ecrireBloc(f, i, buf) #Ecrire le dernier bloc
    affecter_entete(f, 0, n) #Ecrire la première caractéristique
    affecter_entete(f, 1, i+1) #Ecrire la deuxième caractéristique
    f.close()

def affecter_entete(f, offset, val):
    """Fonction pour écrire les caractéristiques dans le fichier selon 'offset'"""
    Adr = offset * getsizeof(dumps(0))
    f.seek(Adr, 0)
    f.write(dumps(val))
    return

def ecrireBloc(f, ind, buff):
    """Procédure pour écrire le bloc dans le fichier selon 'ind'"""
    Adr = 2 * getsizeof(dumps(0)) + ind * bufsize
    f.seek(Adr, 0)
    f.write(dumps(buff))
    return

def lirebloc(f, ind) :
    """Fonction pour lire le bloc du fichier selon 'ind'"""
    Adr = 2 * getsizeof(dumps(0)) + ind * bufsize
    f.seek(Adr, 0)
    buf = f.read(bufsize)
    return (loads(buf))

def entete(f, ind):
    """fonction de récupération des caractéristiques selon 'ind'"""
    Adr = ind * getsizeof(dumps(0))
    f.seek(Adr, 0)
    tete = f.read(getsizeof(dumps(0)))
    return loads(tete)

def afficher_fichier():
    """Procédure d'affichage du fichier"""
    fn = input('Entrer le nom du fichier à afficher: ')
    f = open(fn,'rb')
    secondcar = entete(f,1) #Récupération de nombre des blocs
    print(f'votre fichier contient {secondcar} block \n')
    for i in range (0,secondcar):
        buf = lirebloc(f,i)
        buf_nb = buf[0]       
        buf_tab = buf[1]
        print(f'Le contenu du block {i+1} est:\n' )
        for j in range(buf_nb):
            if (buf_tab[i][-1] != '1'): #Ne pas affichier les enregistrements supprimés logiquement
                print(afficher_enreg(buf_tab[j]))
        print('\n')        
    f.close()
    return

def afficher_enreg(e):
    """Fonction de mise en forme des enregistrements
    Retourne une chaine de caractères sans le '#'"""
    Matricule = e[0:tmat].replace('#',' ')
    Nom = e[tmat:tmat+tnom].replace('#',' ')
    Prenom = e[tmat+tnom:tmat+tnom+tprenom].replace('#',' ')
    Niveau = e[tmat+tnom+tprenom:tmat+tnom+tprenom+tniveau].replace('#',' ')
    Supprimer = e[-1]
    return Matricule + ' ' + Nom + ' ' + Prenom + ' ' + Niveau + Supprimer

def rechercher(f, mat):
    fichier = open(f,'rb')
    nbr = entete(fichier,1)
    trouve = False
    for i in range (0,nbr):
        buf = lirebloc(fichier,i)
        buf_nb = buf[0]    
        buf_tab = buf[1]
        for j in range(buf_nb):
            if (buf_tab[j][0:tmat].rstrip('#') == mat):
                trouve = True
                return [i,j,trouve]
    fichier.close()
    return [-1,-1,trouve]

def insertion(f,e):
    fichier = open(f,'rb+')
    [i,j,trouve] = rechercher(f,e[0:tmat])
    if (trouve == False):
        buf = lirebloc(fichier,entete(fichier,1)-1)      
        if buf[0] == b :
            buf_tab=[etud1] * b #Créer un nouveau bloc
            #Mettre dans le bloc le nouveau enregistrement
            buf_tab[0] = e
            buf = [1,buf_tab]
            ecrireBloc(fichier,entete(fichier,1),buf)
            affecter_entete(fichier, 1, entete(fichier,1)+1)
        else :
            buf_tab = buf[1]
            buf_tab[buf[0]] = e
            buf[0] += 1
            buf[1] = buf_tab
            ecrireBloc(fichier,entete(fichier,1)-1,buf)
        fichier.close()
        return ("insertion avec succes")
    else:
        fichier.close()
        return ("l'etudiant existe deja")
    
def supprimer_phy(f,mat):
    fichier = open(f,'rb+')
    [i,j,trouve] = rechercher(f,mat)
    if (trouve == True):
        buf = lirebloc(fichier,entete(fichier,1)-1)
        if buf[0] == 1 and i == entete(fichier,1)-1 :
            affecter_entete(fichier,1,entete(fichier,1) - 1)
        else : 
            dernier = buf[1][buf[0]-1]
            buf[0] = buf[0] - 1
            if (buf[0] == 0):
                affecter_entete(fichier,1,entete(fichier,1) - 1)
            else:
                ecrireBloc(fichier,entete(fichier,1)-1,buf)
            buf = lirebloc(fichier,i)    
            buf_tab = buf[1]
            buf_tab[j] = dernier
            buf[1] = buf_tab
            ecrireBloc(fichier,i,buf)
        fichier.close()
        return ("suppression avec succes")
    else:
        fichier.close()
        return ("l'etudiant n'existe pas")

def supprimer_log(f,mat):
    fichier = open(f,'rb+')
    [i,j,trouve] = rechercher(f,mat)
    if (trouve == True):
        buf = lirebloc(fichier,i)    
        buf_tab = buf[1]
        buf_tab[j] = buf_tab[j][0:-1] + '1'
        buf[1] = buf_tab
        ecrireBloc(fichier,i,buf)
        fichier.close()
        return ("suppression avec succes")
    else:
        fichier.close()
        return ("l'etudiant n'existe pas")

def frangmenter(f,mat1,mat2):
    t1 = []
    t2 = []
    t3 = []
    fichier = open(f,'rb+')
    for i in range(0,entete(fichier, 1)):
        buf = lirebloc(fichier, i)
        tab = buf[1]
        for j in range(0,buf[0]):
            if int(tab[j][0:tmat].rstrip('#')) < mat1 :
                t1.append(tab[j])
            elif int(tab[j][0:tmat].rstrip('#')) > mat2 :
                t3.append(tab[j])
            else :
                t2.append(tab[j])
    #creer les 3 fichier
    for a in range(0,3):
        """ Procédure de création d'un fichier binaire"""
        fn = "f{}.txt".format(a+1)
        j = 0 #Parcours des enregistrement
        i = 0 #Parcours des blocs
        n = 0 #Nombre des enregistrements
        #initialisation du buffer : 
        buf_tab = [etud1]*b
        buf_nb = 0 #buf_nb représente le nombre d'enregistrements dans le bloc
        try:
            f = open(fn, "wb")
        except:
            print("Creation du fichier {} est impossible ".format(a+1))
        rep = 'O'
        if a == 0 :
            current_t = t1
        elif a == 1 :
            current_t = t2
        elif a == 2 :
            current_t = t3
        elem = 0
        while (elem < len(current_t)):
            #Lecture des information :
            Etud = current_t[elem] #'0' pour non-supprimé
            n += 1 #Augmenter le nombre d'enregistrement
            if(j < b): #bloc non-plain
                buf_tab[j] = Etud
                buf_nb += 1 #Augmenter le nombre d'enregistrement
                j += 1
            else: #bloc plain
                buf=[buf_nb, buf_tab]
                ecrireBloc(f, i, buf) #Ecrire le bloc dans le fichier
                buf_tab=[etud1] * b #Créer un nouveau bloc
                #Mettre dans le bloc le nouveau enregistrement
                buf_nb = 1 
                buf_tab[0] = Etud
                j = 1
                i += 1 #Augmenter le nombre de blocs
            elem += 1
        buf=[j,buf_tab]
        ecrireBloc(f, i, buf) #Ecrire le dernier bloc
        affecter_entete(f, 0, n) #Ecrire la première caractéristique
        affecter_entete(f, 1, i+1) #Ecrire la deuxième caractéristique
        f.close()
    fichier.close()


def supprime_bloc(f,i):
    fichier = open(f,'rb+')
    buf = lirebloc(fichier,entete(fichier,1)-1)
    ecrireBloc(fichier,i,buf)
    affecter_entete(fichier, 1, entete(fichier,1)-1)
    f.close()


############ fichier avec zone de debordement ##################

global bufsize_d #La taille dubfuffer ou du bloc de fichier de debordement
buf_d = [0, [etud1] * b,-1] #Utilisé pour le calcul de la taille du buffer
bufsize_d = getsizeof(dumps(buf_d)) + (len(etud1) + 1) *  (b - 1) #Formule de calcul de la taille du buffer
tab_d = ["#"*tmat, 0, 0]

def index_ordrer(e) : # la fonction qui mettre la table d'index en ordre 
    return e[0]

def table_ordre(e):
    return int(e[0:tmat].rstrip('#'))

def Creer_fichier_avec_zoneDebordement() :
    """ Procédure de création d'un fichier binaire"""
    fn = input("Donner le nom du fichier : ")
    j = 0 #Parcours des enregistrement
    i = 0 #Parcours des blocs
    n = 0 #Nombre des enregistrements
    #initialisation du buffer : 
    buf_tab = [etud1]*b
    buf_nb = 0 #buf_nb représente le nombre d'enregistrements dans le bloc
    buf_next = -1 #buf_next représente le bloc de debordement
    try:
        f = open(fn, "wb")
    except:
        print("Creation du fichier est impossible ")
    rep = 'O'
    tindex = []
    table_etudiants = []
    while (rep.upper() == 'O'):
        #Lecture des information :
        Nom = input('Donner le nom : \n')
        Prenom = input('Donner le prenom : \n')
        Matricule = input('Donner le matricule : \n')
        Niveau = input('Donner le niveau : \n')
        #Redémentionnement des informations : 
        Matricule = resize_chaine(Matricule, tmat)
        Nom = resize_chaine(Nom, tnom)
        Prenom = resize_chaine(Prenom, tprenom)
        Niveau = resize_chaine(Niveau, tniveau)
        #Enregistrement sous-forme d'une chaine de caractères
        Etud = Matricule + Nom + Prenom + Niveau + '0' #'0' pour non-supprimé
        table_etudiants.append(Etud)    
        rep = input("Un autre étudiant à ajouter O/N ? ")
    table_etudiants.sort(key=table_ordre) #Ordonner la table des etudiants
    for a in range(len(table_etudiants)):
        if(j < b): #bloc non-plain
            buf_tab[j] = table_etudiants[a]
            buf_nb += 1 #Augmenter le nombre d'enregistrement#Ajouter les element non ordonnes a l'index
            j += 1
        else: #bloc plain
            buf=[buf_nb, buf_tab,buf_next]
            tindex.append([int(buf_tab[9][0:tmat].rstrip('#')),i,9,False]) #Ajouter les element non ordonnes a l'index
            ecrireBloc_d(f, i, buf) #Ecrire le bloc dans le fichier
            buf_tab=[etud1] * b #Créer un nouveau bloc
            #Mettre dans le bloc le nouveau enregistrement
            buf_nb = 1
            buf_tab[0] = table_etudiants[a]
            j = 1
            i += 1 #Augmenter le nombre de blocs
            
    tindex.append([int(buf_tab[j-1][0:tmat].rstrip('#')),i,j-1,False]) #Ajouter les element non ordonnes a l'index
    buf_d=[j,buf_tab,buf_next]
    ecrireBloc_d(f, i, buf_d) #Ecrire le dernier bloc
    affecter_entete(f, 0, len(table_etudiants)) #Ecrire la première caractéristique
    affecter_entete(f, 1, i+1) #Ecrire la deuxième caractéristique
    f.close()
    
    
    # """ Procédure de création d'un fichier de debordement"""
    
    
    try:
        f = open(fn.replace(".txt","") + "db.txt", "wb")
    except:
        print("Creation du fichier de debordement est impossible ")
    affecter_entete(f, 0, 0) #Ecrire la première caractéristique
    affecter_entete(f, 1, 0) #Ecrire la deuxième caractéristique
    f.close()
    
    
    # Creation de table d'index
    return tindex

def reorganiser(f):
    fichier = open(f,'rb')
    #      Creation de nouveau fichier
    fn = input("entrez le nom de nouveau fichier: ")
    try:
        fichier_d = open(fn, "wb")
    except:
        print("Creation du fichier est impossible ")
    
    # """ Procédure de création d'un fichier de debordement"""
    try:
        fd = open(fn.replace(".txt","") + "db.txt", "wb")
    except:
        print("Creation du fichier de debordement est impossible ")
    affecter_entete(fd, 0, 0) #Ecrire la première caractéristique
    affecter_entete(fd, 1, 0) #Ecrire la deuxième caractéristique
    fd.close()
    
    # l'ajout des element au nouveau fichier et Creation d'index
    
    blocs = entete(fichier,1)
    tindex = []
    table_etudiants = []
    for i in range(blocs):
        buf = lirebloc(fichier,i)
        buf_tab = buf[1]
        nbr = buf[0]
        for j in range(nbr):
            table_etudiants.append(buf_tab[j]) 
    table_etudiants.sort(key=table_ordre)
    j = 0
    i = 0
    buf_nb = 0
    for a in range(len(table_etudiants)):
        if(j < b): #bloc non-plain
            buf_tab[j] = table_etudiants[a]
            buf_nb += 1 #Augmenter le nombre d'enregistrement
            j += 1
        else: #bloc plain
            buf=[buf_nb, buf_tab,-1]
            tindex.append([int(buf_tab[9][0:tmat].rstrip('#')),i,9,False])
            ecrireBloc_d(fichier_d, i, buf) #Ecrire le bloc dans le fichier
            buf_tab=[etud1] * b #Créer un nouveau bloc
            #Mettre dans le bloc le nouveau enregistrement
            buf_nb = 1
            buf_tab[0] = table_etudiants[a]
            j = 1
            i += 1 #Augmenter le nombre de blocs
            
    buf_d=[j,buf_tab,-1]
    tindex.append([int(buf_tab[j-1][0:tmat].rstrip('#')),i,j-1,False])
    ecrireBloc_d(fichier_d, i, buf_d) #Ecrire le dernier bloc
    affecter_entete(fichier_d, 0, len(table_etudiants)) #Ecrire la première caractéristique
    affecter_entete(fichier_d, 1, i+1) #Ecrire la deuxième caractéristique
    fichier.close()
    fichier_d.close()
    return tindex


def ecrireBloc_d(f, ind, buff):
    """Procédure pour écrire le bloc dans le fichier selon 'ind'"""
    Adr = 2 * getsizeof(dumps(0)) + ind * bufsize_d
    f.seek(Adr, 0)
    f.write(dumps(buff))
    return

def lirebloc_d(f, ind) :
    """Fonction pour lire le bloc du fichier selon 'ind'"""
    Adr = 2 * getsizeof(dumps(0)) + ind * bufsize_d
    f.seek(Adr, 0)
    buf = f.read(bufsize_d)
    return (loads(buf))

def afficher_fichier_d():
    """Procédure d'affichage du fichier"""
    fn = input('Entrer le nom du fichier à afficher: ')
    f = open(fn,'rb')
    secondcar = entete(f,1) #Récupération de nombre des blocs
    print(f'votre fichier contient {secondcar} block \n')
    for i in range (0,secondcar):
        buf = lirebloc_d(f,i)
        buf_nb = buf[0]       
        buf_tab = buf[1]
        print(f'Le contenu du block {i+1} est:\n' )
        for j in range(buf_nb):
            if (buf_tab[i][-2] != '-1'): #Ne pas affichier les enregistrements supprimés logiquement
                print(afficher_enreg(buf_tab[j]))
        print('\n')  
        print("next :",buf[2]) 
    f.close()
    return

def rechercher_d(f1,index, mat): # return [trouve, i, j, debordement]
    F1 = open(f1,"rb")
    F2 = open(f1.replace(".txt","") + "db.txt","rb")
    n = len(index)
    j = 0
    cont = None
    while True :
        i = (n - j) // 2
        if index[i][0] == mat :
            buf = lirebloc_d(F1,index[i][1])
            if (buf[1][index[i][2]][-2] != '-1'):
                return [True, index[i][1],index[i][2],index[i][3]]
        elif index[i][0] < mat :
            if len(index) == 1 :
                i -= 1
            if index[i+1][0] > mat or len(index) == 1:
                buf = lirebloc_d(F1,i+1)
                buf_nb = buf[0]
                buf_tab = buf[1]
                buf_next = buf[2]
                for a in range(buf_nb):
                    if int(buf_tab[a][0:tmat].rstrip("#")) == mat and buf_tab[a][-2] != '-1' :
                        return [True, i+1, a, False]
                    elif int(buf_tab[a][0:tmat].rstrip("#")) > mat :
                        return [False, i+1, a, False]
                while buf_next != -1 :
                    buf = lirebloc_d(F2,buf_next)
                    buf_nb = buf[0]
                    buf_tab = buf[1]
                    buf_next = buf[2]
                    for a in range(buf_nb):
                        if int(buf_tab[a][0:tmat].rstrip("#")) == mat and buf_tab[a][-2] != '-1' :
                            return [True, i+1, 9, True]
                return [False, i+1, -1, False]
            else:
                j = i + 1
        else :
            if len(index) == 1 or i == 0 :
                i += 1
                cont = True
            if index[i-1][0] < mat or len(index) == 1 or cont:
                if len(index) == 1 or cont :
                    i -= 1
                buf = lirebloc_d(F1,i)
                buf_nb = buf[0]
                buf_tab = buf[1]
                buf_next = buf[2]
                for a in range(buf_nb):
                    if int(buf_tab[a][0:tmat].rstrip("#")) == mat and buf_tab[a][-2] != '-1' :
                        return [True, i, a, False]
                    elif int(buf_tab[a][0:tmat].rstrip("#")) > mat :
                        return [False, i, a, False]
                while buf_next != -1 :
                    buf = lirebloc_d(F2,buf_next)
                    buf_nb = buf[0]
                    buf_tab = buf[1]
                    buf_next = buf[2]
                    for a in range(buf_nb):
                        if int(buf_tab[a][0:tmat].rstrip("#")) == mat and buf_tab[a][-2] != '-1' :
                            return [True, i, 9, True]
                return [False, i, -1, False]
            else :
                n = i-1


def requete_intervale(f1, index, inf, sup):
    F1 = open(f1,"rb")
    F2 = open(f1.replace(".txt","") + "db.txt","rb")
    liste_etudiant = []
    [trouve, i, j, debordement] = rechercher_d(f1,index,inf)
    if trouve == False : ## si l'inf n'existe pas on cherche le premier element superieur a inf
        buf = lirebloc_d(F1,i)
        new_inf = []
        a = 0
        while int(buf[1][a][0:tmat].rstrip("#")) < inf and i < entete(F1,1):
            if a == b :
                while buf[2] != -1:
                    buf = lirebloc_d(F2,buf[2])
                    for a in range(buf[0]):
                        if int(buf[1][a][0:tmat].rstrip("#")) > inf:
                            new_inf = buf[1][a]
                            [trouve, i, j, debordement] = [True, i, 9, True]
                            break
                i += 1
                buf = lirebloc_d(F1,i)
            a += 1
            if int(buf[1][a][0:tmat].rstrip("#")) > inf:
                            new_inf = buf[1][a]
                            [trouve, i, j, debordement] = [True, i, a, False]
            if new_inf != -1 :
                break
    if trouve == False :
        return "l'intervale n'existe pas"
    buf = lirebloc_d(F1,i)
    a = j
    while int(buf[1][a][0:tmat].rstrip("#")) <= sup:
        liste_etudiant.append(buf[1][a].replace("#"," "))
        a += 1
        if a == b :
            while buf[2] != -1:
                buf = lirebloc_d(F2,buf[2])
                for a in range(buf[0]):
                    if int(buf[1][a][0:tmat].rstrip("#")) <= sup:
                        liste_etudiant.append(buf[1][a].replace("#"," "))
            i += 1
            buf = lirebloc_d(F1,i)
            a = 0
    F1.close()
    F2.close()
    return liste_etudiant

def inserer_d(f, index, etudiant):
    try:
        fichier = open(f,'rb+')
    except:
        print("ouverture du fichier impossible")
    try:
        F2 = open(f.replace(".txt","") + "db.txt","rb+")
    except:
        print("ouverture du fichier de debordement impossible")
    [trouve,i,j,debordement] = rechercher_d(f,index,int(etudiant[0:tmat].rstrip("#")))
    print([i,j,trouve,debordement])
    if not(trouve) :
        buf = lirebloc_d(fichier,i)
        buf_nb = buf[0]
        buf_tab = buf[1]
        buf_next = buf[2]
        if buf_nb == b :
            if buf_next == -1 :
                decal_elem = buf_tab[b-1]
                print(decal_elem)
                for a in range(b-1,j,-1):
                    buf_tab[a] = buf_tab[a-1]
                buf_tab[j] = etudiant
                buf = [buf_nb,buf_tab,entete(F2,1)]
                ecrireBloc_d(fichier,i,buf)
                buf_tab = [etud1] * b
                buf_tab[0] = decal_elem
                buf = [1,buf_tab,-1]
                ecrireBloc_d(F2,entete(F2,1),buf)
                affecter_entete(F2,1,entete(F2,1)+1)
            else :
                while buf_next != -1 :
                    pre = buf[2]
                    buf = lirebloc_d(F2,buf_next)
                    buf_nb = buf[0]
                    buf_tab = buf[1]
                    buf_next = buf[2]
                if buf_nb == b :
                    buf[2] = entete(F2,1)
                    ecrireBloc_d(F2,pre,buf)
                    buf_tab = [etud1] * b
                    buf_tab[0] = etudiant
                    buf = [1,buf_tab,-1]
                    ecrireBloc_d(F2,entete(F2,1),buf)
                    affecter_entete(F2,1,entete(F2,1)+1)
                else :
                    buf[buf_nb-1] = etudiant
                    buf = [buf_nb+1, buf_tab, -1]
                    ecrireBloc_d(F2,entete(F2,1)-1,buf)
            index[i][3] = True
        else :
            for a in range(buf_nb,j,-1):
                buf_tab[a] = buf_tab[a-1]
            buf_tab[j] = etudiant
            buf = [buf_nb + 1, buf_tab, buf_next]
            ecrireBloc_d(fichier,i,buf)
            index[i][2] = buf_nb - 1
    fichier.close()
    F2.close()


def supprimer_log_d(f, index, mat):
    fichier = open(f,'rb+')
    [trouve,i,j,debordement] = rechercher_d(f,index,mat)
    if trouve :
        ## supprimer de fichier de donner
        buf = lirebloc_d(fichier,i)
        buf_tab = buf[1]
        buf_tab[j] = buf_tab[j][0:-1] + '1'
        buf[1] = buf_tab
        ecrireBloc_d(fichier,i,buf)
        fichier.close()
        return ("suppression avec succes")
    else:
        fichier.close()
        return ("l'etudiant n'existe pas")


#### CA C'EST UN CATALOG D'UTILISATION DE PROGRAMME ####
##   POUR TESTER UN PARTIE JUSTE ENLEVER LE COMMENTAIRE ET LE TESTER  ##
### Note : IL EXISTE UN FICHIER TEXTE NOMMEE "f.txt" QUI CONTIENT 2 BLOC D'ENREGISTREMENT VOUS POUVEZ UTILISER POUR LA REORGANISATION ####


#
#### test de fonction de creation d'un nouveau fichier et son fichier de debordement en retournant la table d'index ####
#
# index = Creer_fichier_avec_zoneDebordement()
# afficher_fichier_d()
# print(index)


#
#### test de la fonction recherche avec la reorganisation ####
#
# il est conseille de nommer le nouveau fichier "test.txt" et la fonction reorganiser ou la creation d'un nouveau fichier va cree un fichier de debordement qui s'appler "testdb.txt" automatiquement
#
# index = reorganiser("f.txt")
# afficher_fichier_d()
# print(index)
# print(rechercher_d("test.txt",index,12))


#
#### test de l'insertion avec la reorganisation
#
# index = reorganiser("f.txt")
# for ad in range(1) :
#     nom = input("nom :")
#     prenom = input("prenom :")
#     mat = input("matricule :")
#     niveau = input("niveau :")
#     Matricule = resize_chaine(mat, tmat)
#     Nom = resize_chaine(nom, tnom)
#     Prenom = resize_chaine(prenom, tprenom)
#     Niveau = resize_chaine(niveau, tniveau)
#     element = Matricule + Nom + Prenom + Niveau + '0'
#     inserer_d("test.txt",index,element)


#
#### test de fonction de suppression logique 
#
# index = reorganiser("f.txt")
# supprimer_log_d("test.txt",index,10)