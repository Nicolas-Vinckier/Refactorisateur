import os
import time

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


# Fonction récursive pour vérifier les fichiers et dossiers
def check_directory(old_dir, new_dir):
    for root, dirs, files in os.walk(new_dir):
        for file in files:
            old_file_path = os.path.join(old_dir, os.path.relpath(root, new_dir), file)
            new_file_path = os.path.join(new_dir, os.path.relpath(root, new_dir), file)

            if not os.path.exists(old_file_path):
                print(f"Le fichier {new_file_path} a été ajouté")
            elif os.path.getmtime(new_file_path) > os.path.getmtime(old_file_path):
                print(f"Le fichier {new_file_path} a été modifié")

        for dir in dirs:
            old_sub_dir = os.path.join(old_dir, os.path.relpath(root, new_dir), dir)
            new_sub_dir = os.path.join(new_dir, os.path.relpath(root, new_dir), dir)

            if not os.path.exists(old_sub_dir):
                print(f"Le dossier {new_sub_dir} a été ajouté")
            else:
                check_directory(old_sub_dir, new_sub_dir)


def main():
    create_folder()
    check_directory(old_path, new_path)


if __name__ == "__main__":
    main()
