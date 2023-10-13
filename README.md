# Comparateur de Dossiers pour la Refactorisation

Cet outil Python est spécialement conçu pour accompagner les développeurs pendant le processus de refactorisation. En comparant le contenu de deux dossiers (généralement une "ancienne version" et une "nouvelle version" du code), il détecte toutes les modifications, qu'il s'agisse de fichiers ou de dossiers ajoutés, supprimés ou modifiés.

## Fonctionnalités

- **Comparaison Profonde** : analyse récursive de tous les fichiers et sous-dossiers.
- **Préparation de l'Environnement** : création automatique des dossiers de version s'ils n'existent pas.
- **Documentation Automatique** : exportation des résultats dans des fichiers log distincts pour les ajouts, suppressions et modifications.
- **Compatibilité des Caractères** : prise en charge intégrale de l'UTF-8 pour assurer la lisibilité des caractères spéciaux.
- **Refactorisation Assistée** : idéal pour documenter et suivre les changements lors de la refactorisation du code.

## Comment utiliser

1. Placez ce script Python dans un répertoire contenant les dossiers "ancienne_version" et "nouvelle_version" que vous souhaitez comparer.
2. Exécutez le script.
3. Consultez le dossier "logs" pour voir les fichiers qui contiennent les différences détectées.

## Fichiers de sortie

- `nouveaux.txt` : liste des fichiers et dossiers ajoutés lors de la refactorisation.
- `supprimes.txt` : liste des fichiers et dossiers supprimés lors de la refactorisation.
- `modifies.txt` : liste des fichiers qui ont été modifiés avec leur date de dernière modification.

## Licence

Ce projet est sous licence selon les termes de la "GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007". Consultez le fichier `LICENSE` pour plus de détails.



un outil Python pour détecter et documenter les modifications apportées lors de la refactorisation du code entre deux versions d'un projet.
