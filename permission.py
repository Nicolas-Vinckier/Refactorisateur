import os

# Liste de permissions avec leurs valeurs octales et explications
# Les valeurs octales sont utilisées pour définir les autorisations en utilisant os.chmod.

permissions_list = [
    (0o400, "Lecture (read) : Permet de lire un fichier."),  # 0
    (0o200, "Écriture (write) : Permet de modifier un fichier existant."),  # 1
    (0o100, "Exécution (execute) : Permet d'exécuter un fichier exécutable."),  # 2
    (0o700, "Lecture, écriture et exécution pour l'utilisateur propriétaire."),  # 3
    (0o600, "Lecture et écriture pour l'utilisateur propriétaire."),  # 4
    (0o500, "Lecture et exécution pour l'utilisateur propriétaire."),  # 5
    (
        0o755,
        "Lecture, écriture et exécution pour le propriétaire, et lecture et exécution pour les autres.",
    ),  # 6
    (
        0o644,
        "Lecture et écriture pour le propriétaire, lecture seule pour les autres.",
    ),  # 7
    (
        0o555,
        "Exécution pour le propriétaire, et lecture et exécution pour les autres.",
    ),  # 8
    (
        0o777,
        "Lecture, écriture et exécution pour tous (utilisateur, groupe, autres).",
    ),  # 9
]


import os


def change_permissions(directory_path, permission):
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            file_path = os.path.join(root, file)
            os.chmod(file_path, permission)
            print(f"Changement des permissions de {file_path} en {permission:o}")
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            os.chmod(dir_path, permission)
            print(f"Changement des permissions de {dir_path} en {permission:o}")


# Exemple d'utilisation
directory_path = "./"
permission = 0o777  # Par exemple, autorisations rwxr-xr-x
change_permissions(directory_path, permission)
