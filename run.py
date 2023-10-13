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
        # print("Les dossiers existent déjà")
        pass


# Fonction qui permet de vérifier si il y a des nouveau fichiers dans le dossier new_path
def check_new_files():
    for file in os.listdir(new_path):
        if file not in os.listdir(old_path):
            print(f"Le fichier {new_path}/{file} a été ajouté")
            return True
    return False


# Fonction qui permet de vérifier si il y a des fichiers modifiés dans le dossier new_path
def check_modified_files():
    for file in os.listdir(new_path):
        if file in os.listdir(old_path):
            if os.path.getmtime(f"{new_path}/{file}") > os.path.getmtime(
                f"{old_path}/{file}"
            ):
                print(f"Le fichier {new_path}/{file} a été modifié")
                return True
    return False


# Fonction qui permet de vérifier si il y a des fichiers supprimés dans le dossier new_path
def check_deleted_files():
    for file in os.listdir(old_path):
        if file not in os.listdir(new_path):
            print(f"Le fichier {old_path}/{file} a été supprimé")
            return True
    return False


def main():
    create_folder()
    check_new_files()
    check_modified_files()
    check_deleted_files()


if __name__ == "__main__":
    main()
