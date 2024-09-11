# DDBoat-Guerlédan (reymanta <3)

## Description
Projet Guerlédan septembre 2024.
Emma, Rémi et Yasmine.
On s'appelle reymanta (REY comme Rémi Emma Yasmine tu l'as)

## Composition du groupe
Rémi GenouxLubain, Yasmine Raoux, Emma Royant

## Fichiers
Les résultats des différentes missions (photos, vidéos, relevés GPS, affichage maps) sont chacun par dans un dossier numéroté.

# Fichiers .py
* calibration.py : calibrer l'accéléromètre et le magnétomètre et renvoie les angles d'Euler
* cap_ouest.py : suivre un cap et enregistrer les données GPS dans un log
* sens_imu.py : ????
* analyse_gps.py : convertir les données GPS du log en données GPX
* mission_2 : A REMPLIR A LA FIN DE J3

## Déroulé de la semaine

# Jour 1 : Suivi de cap
Calibrage boussole
Suivre le cap NW

Obtention du log du parcours : 30s vers le NW puis 30s wait puis 30s vers le SE :

## Jour 2 : Rejoindre un waypoint
Transformation des données sphériques en coordonnées cartésiennes
Problèmes rencontrés : penser à convertir lesdonnées GPS en radians

<img src="./mission_2/mission_2.png" alt="Aller-Retour vers une bouée" width="400">

## Jour 3 : Suivi de trajectoire
Problème : l'IMU prend l'eau : on doit le re-calibrer
Puis test du suivi de Lissajou
