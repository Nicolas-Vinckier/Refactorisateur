import paramiko
import os

# === Dossier local
dossier_client = os.path.abspath("serveur_sftp")

os.makedirs(dossier_client, exist_ok=True)
os.makedirs("PasswordFolder", exist_ok=True)

# === Chemin parent sur le serveur distant
parent_folder = "/home/myvcarh/www/"


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def compare_files_folders(local_files, local_folders, sftp_files, sftp_folders):
    missing_files = [f for f in sftp_files if f not in local_files]
    missing_folders = [f for f in sftp_folders if f not in local_folders]

    # Ici, nous supposons que vous avez toujours la version la plus récente des fichiers.
    # Vous pouvez ajouter une vérification des dates de modification si nécessaire.
    updated_files = local_files

    return missing_files, missing_folders, updated_files


def download_missing_items(sftp, missing_files, missing_folders):
    for folder in missing_folders:
        local_path = os.path.join(dossier_client, folder)
        os.makedirs(local_path, exist_ok=True)

    for file in missing_files:
        local_path = os.path.join(dossier_client, file)
        remote_path = os.path.join(parent_folder, file)
        sftp.get(remote_path, local_path)


def upload_updated_files(sftp, updated_files):
    for file in updated_files:
        local_path = os.path.join(dossier_client, file)
        remote_path = os.path.join(parent_folder, file)
        sftp.put(local_path, remote_path)


def list_files_on_sftp_folder(sftp, path):
    """
    Liste les dossiers et fichiers du serveur SFTP et les renvoie sous forme de deux listes.
    """
    files_list = []
    folders_list = []
    try:
        items = sftp.listdir_attr(path)
        for item in items:
            if item.st_mode & 0o40000:  # C'est un dossier
                folders_list.append(f"{item.filename}")
            else:
                files_list.append(f"{item.filename}")
    except Exception as e:
        print(f"Erreur lors de la liste des fichiers SFTP : {e}")
    return files_list, folders_list


def connect_to_sftp(host, port, username, password):
    try:
        transport = paramiko.Transport((host, port))
        transport.connect(username=username, password=password)
        sftp = paramiko.SFTPClient.from_transport(transport)
        return sftp
    except Exception as e:
        print(f"Erreur de connexion SFTP : {e}")
        return None


def main():
    clear_screen()

    # Informations de connexion SFTP
    host = "ftp.cluster028.hosting.ovh.net"
    port = 22
    username = "myvcarh"

    # Lire le mot de passe depuis le fichier 'myvcardpro.txt'
    with open("PasswordFolder/myvcardpro.txt", "r") as f:
        password = f.read().strip()

    sftp = connect_to_sftp(host, port, username, password)

    print(f"---------------------------- Connexion SFTP ----------------------------")
    print(f"Connexion au serveur SFTP {host}:{port} avec l'utilisateur {username}.\n")

    if sftp:
        print(
            f"---------------------------- Dossier distant: {parent_folder} ----------------------------"
        )
        files_list, folders_list = list_files_on_sftp_folder(sftp, parent_folder)

        print("Fichiers:")
        print(files_list)

        print("Dossiers:")
        print(folders_list)

        # Récupérer la liste des fichiers et dossiers locaux
        local_files = os.listdir(dossier_client)
        local_folders = [
            f for f in local_files if os.path.isdir(os.path.join(dossier_client, f))
        ]
        local_files = [f for f in local_files if f not in local_folders]

        # Comparer les fichiers et dossiers
        missing_files, missing_folders, updated_files = compare_files_folders(
            local_files, local_folders, files_list, folders_list
        )

        # Télécharger les fichiers/dossiers manquants
        download_missing_items(sftp, missing_files, missing_folders)

        # Envoyer les fichiers mis à jour
        upload_updated_files(sftp, updated_files)

        # Fermer la connexion SFTP
        sftp.close()
    else:
        print("La connexion SFTP a échoué.")


if __name__ == "__main__":
    main()
