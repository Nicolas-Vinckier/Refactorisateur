import os
import time


def get_date():
    return time.strftime("%Y-%m-%d", time.gmtime())


def get_time():
    return time.strftime("%H-%M-%S", time.gmtime())


old_path = "ancienne_version"
new_path = "nouvelle_version"


def create_folder():
    if not os.path.exists(old_path):
        os.mkdir(old_path)
        print(f"Création du dossier {old_path}")
    if not os.path.exists(new_path):
        os.mkdir(new_path)
        print(f"Création du dossier {new_path}")
    else:
        pass


# Fonction qui permet de vérifier si il y a des nouveau fichiers dans le dossier new_path
def check_new_files():
    new_files = []
    for file in os.listdir(new_path):
        if file not in os.listdir(old_path):
            new_files.append(f"Le fichier {new_path}/{file} a été ajouté")
    return new_files


# Fonction qui permet de vérifier si il y a des fichiers modifiés dans le dossier new_path
def check_modified_files():
    modified_files = []
    for file in os.listdir(new_path):
        if file in os.listdir(old_path):
            if os.path.getmtime(f"{new_path}/{file}") > os.path.getmtime(
                f"{old_path}/{file}"
            ):
                modified_files.append(f"Le fichier {new_path}/{file} a été modifié")
    return modified_files


# Fonction qui permet de vérifier si il y a des fichiers supprimés dans le dossier new_path
def check_deleted_files():
    deleted_files = []
    for file in os.listdir(old_path):
        if file not in os.listdir(new_path):
            deleted_files.append(f"Le fichier {old_path}/{file} a été supprimé")
    return deleted_files


def main():
    create_folder()
    new_files = check_new_files()
    modified_files = check_modified_files()
    deleted_files = check_deleted_files()

    if new_files:
        print("Nouveaux fichiers/dossiers détectés:")
        for file in new_files:
            print(file)

    if modified_files:
        print("Fichiers/dossiers modifiés détectés:")
        for file in modified_files:
            print(file)

    if deleted_files:
        print("Fichiers/dossiers supprimés détectés:")
        for file in deleted_files:
            print(file)


if __name__ == "__main__":
    main()
