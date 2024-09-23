
# Guerlédan - Reymanta

## Description
Projet Guerlédan septembre 2024.
Composition du groupe : Emma, Rémi et Yasmine.
Nom de groupe : reymanta


# Fichiers
Les résultats des différentes missions (photos, vidéos, relevés GPS, affichage maps) sont chacun dans un dossier numéroté.

## Nos différents fichiers python
* **calibration.py** : calibrer l'accéléromètre et le magnétomètre et renvoie les angles d'Euler ains que calculer les valeurs de l'accéléromètre et du mgnétomètre corrigées
* **cap_ouest.py** : suivre un cap et enregistrer les données GPS dans un log (pour la mission 1)
* **sens_imu.py** : permet de tester si l'IMU fonctionne bien (pour quand on commence à avoir des valeurs aberrantes/ qui ne bougent plus)
* **analyse_gps.py** : convertir les données GPS du log (fichier txt) en données GPX automatiquement pour tous les fichiers txt du dossier
* **stop.py** : permet d'arrêter les moteurs du bateau
* **test_lissajou.py : fichier pour afficher le lissajou grâce à matplotlib pour vérifier les équations/ les paramètres d'entrée
* **main.py** : contient tous les codes des missions 2, 3, 4 et 5 (suivre un cap fixe, suivre une ligne, suivre une liste de waypoints, lissajou etc...)

# Déroulé de la semaine

## Jour 1 : Suivi de cap
   Le premier jour, il nous a d'abord fallu calibrer l'accéléromètre ainsi que le magnétomètre (création du fichier calibration.py). Une fois avoir testé à l'extérieur que le DDboat était bien calibré, nous avons pu passer à la mission du jour qui consistait à suivre le cap ouest pendant 30 secondes.  
   Nous avons aussi réussi à récupérer les logs dans un fichier texte, que nous avons ensuite traité grâce à ce que nous avions déjà fait le vendredi précédent avec les essais sur le stade. Avec le fichier .gpx obtenu, nous avons pu afficher le trajet du ddboat sur Google Maps.

![Mission 1 : suivi NW pendant 30s depuis le ponton](./mission_1/mission_1.png "Mission 1")


## Jour 2 : Rejoindre un waypoint
Nous avons eu un cours sur comment rejoindre un waypoint, et notamment la conversion des coordonnées sphériques (latitude/longitude) en coordonnées cartésiennes dans le plan du lac (avec un point du ponton comme origine).  
Les différents problèmes que nous avons rencontrés dans la journée ont été :  
* l'oubli de la conversion des angles des degrés en radians  
* le GPS est en NED (et les coordonnées classiques dans Google Maps par exemple) alors que nos équations étaient dans un repère avec les coordonées en Ouest positives, il fallait donc veiller à mettre les bonnes valeurs négatives.  
L'image ci-dessous montre le trajet du bateau, qui a fait un suivi de cap jusqu'à la bouée avant de revenir au ponton (validation de la bouée quand le ddboat était dans un rayon de 5m de la bouée) 

![Mission 2 : aller à la bouée et revenir au ponton](./mission_2/mission_2.png "Mission 2")

## Jour 3 : Suivi de trajectoire (navigation)
Problème : l'IMU prend l'eau : on doit le re-calibrer
Puis test du suivi de Lissajou
Ajout de la fonction verif_gps car sinon les premières valeurs sont aberrantes et le ddboat part bizarrement

## Jour 4 : Suivi de ligne (guidage)
Effectuer un suivi de ligne vers la bouée puis continuer pendant 2 minutes (couloir de 5m)
Aller de points en points grâce au suivi de ligne jusqu'à ne plus voir le ddboat
!attention! commande à 120 pour conserver les batteries -> endurance !!
IMU a pris l'eau -> recalibration 

## Jour 5 : Différentes zones
Problème avec le suivi des waypoints (on ne sait pas pourquoi)
à l'heure de la mission, erreur d'inattention sur l'heure de départ

# Les commandes de base

Savoir si le ddboat nous répond :
```bash
ping 172.20.25.212
```
Se connecter au ddboat
```bash
ssh ue32@172.20.25.208  #mot de passe : ue32
```
Pour envoyer tout le fichier au dd-boat:
```bash
scp fichier.py ue32@172.20.25.208:reymanta 
```
Exécuter le fichier
```bash
cd reymanta
python3 fichier.py
```
Pour récupérer le fichier de log du ddboat, qui sera placé dans le dossier courant :
```bash
scp ue32@172.20.25.208:reymanta/log.txt log.txt  
```
