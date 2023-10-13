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
    """Compare le contenu de deux dossiers et affiche toutes les modifications effectuées.

    Args:
      old_path: Le chemin du premier dossier.
      new_path: Le chemin du deuxième dossier.

    Returns:
      Une liste de chaînes représentant les modifications effectuées.
    """

    # Liste des modifications effectuées.
    modifications = []

    # Liste des fichiers et dossiers du deuxième dossier.
    files2 = os.listdir(new_path)
    dirs2 = [dir for dir in os.listdir(new_path) if os.path.isdir(os.path.join(new_path, dir))]

    # Parcours récursif des dossiers.
    for root, dirs, files in os.walk(old_path):
        # Parcours des fichiers du dossier actuel.
        for file in files:
            # Chemin complet du fichier dans le dossier actuel.
            path1 = os.path.join(root, file)

            # Existe-t-il un fichier correspondant dans le deuxième dossier ?
            if file in files2:
                # Chemin complet du fichier dans le deuxième dossier.
                path2 = os.path.join(new_path, file)

                # Les fichiers sont-ils identiques ?
                if os.path.isfile(path1) and os.path.isfile(path2):
                    if os.path.getsize(path1) == os.path.getsize(path2):
                        # Les fichiers sont identiques.
                        continue
                    else:
                        # Les fichiers sont différents.
                        modifications.append(
                            f"Fichier modifié : {path1} (dernière modification le {datetime.datetime.fromtimestamp(os.path.getmtime(path1)).strftime('%Y-%m-%d %H:%M:%S')})"
                        )
                else:
                    # Les fichiers sont différents.
                    modifications.append(
                        f"Fichier modifié : {path1} (dernière modification le {datetime.datetime.fromtimestamp(os.path.getmtime(path1)).strftime('%Y-%m-%d %H:%M:%S')})"
                    )
            else:
                # Le fichier n'existe pas dans le deuxième dossier.
                modifications.append(f"Fichier supprimé : {path1}")

        # Parcours des sous-dossiers.
        for dir in dirs:
            # Chemin complet du dossier dans le premier dossier.
            path1 = os.path.join(root, dir)

            # Existe-t-il un dossier correspondant dans le deuxième dossier ?
            if dir in dirs2:
                # Chemin complet du dossier dans le deuxième dossier.
                path2 = os.path.join(new_path, dir)

                # Comparaison des dossiers.
                modifications += compare_folders(path1, path2)
            else:
                # Le dossier n'existe pas dans le deuxième dossier.
                modifications.append(f"Dossier supprimé : {path1}")

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
