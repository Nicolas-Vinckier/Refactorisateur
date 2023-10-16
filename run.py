import os
import datetime
import shutil

old_path = "ancienne_version"
new_path = "nouvelle_version"
refacto_folder = "refacto_version"


def create_folder():
    for path in [old_path, new_path, refacto_folder]:
        if not os.path.exists(path):
            os.mkdir(path)
            print(f"Création du dossier {path}")


def sync_and_refactor(old_path, new_path, refacto_path):
    # Suppression des fichiers/dossiers supprimés
    for item in os.listdir(refacto_path):
        if item not in os.listdir(new_path):
            item_path = os.path.join(refacto_path, item)
            if os.path.isfile(item_path):
                os.remove(item_path)
            else:
                shutil.rmtree(item_path)
            print(f"Suppression de {item_path}")

    # Ajout/Mise à jour des fichiers/dossiers
    for item in os.listdir(new_path):
        old_item_path = os.path.join(old_path, item)
        new_item_path = os.path.join(new_path, item)
        refacto_item_path = os.path.join(refacto_path, item)

        if os.path.isfile(new_item_path):
            if not os.path.exists(old_item_path) or os.path.getmtime(
                old_item_path
            ) != os.path.getmtime(new_item_path):
                shutil.copy2(new_item_path, refacto_item_path)
                print(f"Copie de {new_item_path} vers {refacto_item_path}")

        elif os.path.isdir(new_item_path):
            if not os.path.exists(refacto_item_path):
                os.mkdir(refacto_item_path)
                print(f"Création du dossier {refacto_item_path}")
            sync_and_refactor(old_item_path, new_item_path, refacto_item_path)


def main():
    create_folder()
    sync_and_refactor(old_path, new_path, refacto_folder)


if __name__ == "__main__":
    main()
