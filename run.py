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
    nouveaux = []
    supprimes = []
    modifies = []

    for item in os.listdir(old_path):
        old_item_path = os.path.join(old_path, item)
        new_item_path = os.path.join(new_path, item)

        if os.path.isfile(old_item_path):
            if not os.path.exists(new_item_path):
                supprimes.append(f"Fichier supprimé: {old_item_path}")
            elif os.path.getsize(old_item_path) != os.path.getsize(new_item_path):
                modifies.append(
                    f"Fichier modifié: {old_item_path} (dernière modification le {datetime.datetime.fromtimestamp(os.path.getmtime(old_item_path)).strftime('%Y-%m-%d %H:%M:%S')})"
                )
        elif os.path.isdir(old_item_path) and not os.path.exists(new_item_path):
            supprimes.append(f"Dossier supprimé: {old_item_path}")
        elif os.path.isdir(old_item_path):
            new_nouveaux, new_supprimes, new_modifies = compare_folders(
                old_item_path, new_item_path
            )
            nouveaux.extend(new_nouveaux)
            supprimes.extend(new_supprimes)
            modifies.extend(new_modifies)

    for item in os.listdir(new_path):
        old_item_path = os.path.join(old_path, item)
        new_item_path = os.path.join(new_path, item)

        if not os.path.exists(old_item_path):
            if os.path.isfile(new_item_path):
                nouveaux.append(f"Nouveau fichier: {new_item_path}")
            elif os.path.isdir(new_item_path):
                nouveaux.append(f"Nouveau dossier: {new_item_path}")

    return nouveaux, supprimes, modifies


def write_to_file(filename, content):
    with open(filename, "w", encoding="utf-8") as f:
        for line in content:
            f.write(line + "\n")


def main():
    create_folder()
    nouveaux, supprimes, modifies = compare_folders(old_path, new_path)

    if not os.path.exists("logs"):
        os.mkdir("logs")

    # Écrire les résultats dans les fichiers.
    write_to_file("logs/nouveaux.txt", nouveaux)
    write_to_file("logs/supprimes.txt", supprimes)
    write_to_file("logs/modifies.txt", modifies)

    # Pour visualiser les résultats dans la console.
    for item in nouveaux:
        print(item)
    for item in supprimes:
        print(item)
    for item in modifies:
        print(item)


if __name__ == "__main__":
    main()
