import os
import shutil

old_path = "ancienne_version"
new_path = "nouvelle_version"
refacto_folder = "refacto_version"
user_modifications_folder = "modifications_utilisateur"


def create_folder():
    for path in [old_path, new_path, refacto_folder, user_modifications_folder]:
        if not os.path.exists(path):
            os.mkdir(path)
            print(f"Création du dossier {path}")


def sync_and_refactor(old_path, new_path, refacto_path):
    for item in os.listdir(refacto_path):
        if item not in os.listdir(new_path):
            item_path = os.path.join(refacto_path, item)
            if os.path.isfile(item_path):
                os.remove(item_path)
            else:
                shutil.rmtree(item_path)
            print(f"Suppression de {item_path}")

    for item in os.listdir(new_path):
        old_item_path = os.path.join(old_path, item)
        new_item_path = os.path.join(new_path, item)
        refacto_item_path = os.path.join(refacto_path, item)

        # Modification pour gérer les sous-dossiers dans user_modifications_folder
        relative_path = os.path.relpath(old_item_path, old_path)
        user_modified_path = os.path.join(user_modifications_folder, relative_path)

        if os.path.isfile(new_item_path):
            if os.path.exists(user_modified_path):
                shutil.copy2(user_modified_path, refacto_item_path)
                print(
                    f"Copie des modifications de l'utilisateur de {user_modified_path} vers {refacto_item_path}"
                )
                # Pause pour informer l'utilisateur
                input("Appuyez sur Entrée pour continuer...")
            elif not os.path.exists(old_item_path) or os.path.getmtime(
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
