<<<<<<< HEAD
# Outils de création de bases, de récupération et d'injection de données

## Introduction

Ce projet couvre :

- La création de bases de données déjà mises en forme et prête à recevoir les données des capteurs
- La partie de récupération des données au travers de scripts de mises en forme
- La partie d'injection des données récupérées dans la base choisie

## Création de base

Afin de créer une nouvelle base aux normes définies il faut d'abord crée un Template sur notre serveur de bases de données, ce template sera ensuite réutilisé pour la création de chaque base (une base par ajout de bâtiment).

<br>

Appel du fichier Injector contenant le script de gestion des bases

```python
from Lib.Senders.Injector import DataBase
```

Adresse ip du serveur de base de donnée auquel se connecter, ici la base tourne en local

```python
ip="localhost"
```

Instanciation d'un objet DataBase(ip) afin de manipuler les différentes options de manipulation de bases de données

```python
bd = DataBase(ip)
```

Créons d'abord un template de BDD appelé MonTemplate

```python
nomTemplate = "MonTemplate"
bd.create_template(nomTemplate)
```

Maintenant que le schéma est définit nous pouvons créer notre première base _MaBase_ à partir du template _MonTemplate_ crée ci-dessus

```python
nomBase = "MaBase"
bd.create(nomBase, nomTemplate)
```

Et voilà, notre première base est créer, il ne reste plus qu'à y injecter des données

<br>

Voici d'autres fonctions utiles pour la gestion des bases :

```python
bd.query("Requête ici") # Permet d'executer une requête SQL sur le serveur

bd.liste() # Renvoi la liste des bases présentes sur le serveur

bd.exist("Nom à tester") # Vérifie si une base existe déjà à ce nom
```

## Injection de données

Maintenant que notre base est prête il ne reste plus qu'à injecter les données provenant de notre capteur, pour ce faire il faut avoir préparé en amont un script suivant les protocoles Get et Sender (permettant d'avoir une standardisation)

```python
```

```python
```

```python
```

```python
```

```python
```

```python
```
=======
# 
>>>>>>> 9ffa2072ce916b27c9c08c6f70e7f5061a98010e
