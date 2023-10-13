import os
import datetime

# Chemins des dossiers à comparer.
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


def compare_folders(old_path, new_path):
    modifications = []

    # Vérification des fichiers dans old_path par rapport à new_path.
    for item in os.listdir(old_path):
        old_item_path = os.path.join(old_path, item)
        new_item_path = os.path.join(new_path, item)

        if os.path.isfile(old_item_path):
            if not os.path.exists(new_item_path):
                modifications.append(f"Fichier supprimé: {old_item_path}")
            elif os.path.getsize(old_item_path) != os.path.getsize(new_item_path):
                modifications.append(
                    f"Fichier modifié: {old_item_path} (dernière modification le {datetime.datetime.fromtimestamp(os.path.getmtime(old_item_path)).strftime('%Y-%m-%d %H:%M:%S')})"
                )
        elif os.path.isdir(old_item_path) and not os.path.exists(new_item_path):
            modifications.append(f"Dossier supprimé: {old_item_path}")
        elif os.path.isdir(old_item_path):
            modifications += compare_folders(old_item_path, new_item_path)

    # Vérification des nouveaux fichiers ou dossiers dans new_path qui n'étaient pas dans old_path.
    for item in os.listdir(new_path):
        old_item_path = os.path.join(old_path, item)
        new_item_path = os.path.join(new_path, item)

        if not os.path.exists(old_item_path):
            if os.path.isfile(new_item_path):
                modifications.append(f"Nouveau fichier: {new_item_path}")
            elif os.path.isdir(new_item_path):
                modifications.append(f"Nouveau dossier: {new_item_path}")

    return modifications


def main():
    # Création des dossiers si nécessaire.
    create_folder()

    # Comparaison des dossiers.
    modifications = compare_folders(old_path, new_path)

    # Affichage des modifications.
    for modification in modifications:
        print(modification)


if __name__ == "__main__":
    main()
