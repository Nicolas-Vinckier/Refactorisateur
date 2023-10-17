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


def sftp_join(*args):
    """Une version simple de os.path.join pour les chemins SFTP."""
    return "/".join(arg.strip("/") for arg in args)


def connect_to_sftp(host, port, username, password):
    try:
        transport = paramiko.Transport((host, port))
        transport.connect(username=username, password=password)
        sftp = paramiko.SFTPClient.from_transport(transport)
        return sftp
    except Exception as e:
        print(f"Erreur de connexion SFTP : {e}")
        return None


def download_recursive(sftp, remote_path, local_path):
    # Vérification d'existence du chemin distant
    try:
        sftp.stat(remote_path)
    except FileNotFoundError:
        print(f"Chemin distant introuvable: {remote_path}")
        return

    # Créer le dossier local si ce n'est pas déjà fait
    if not os.path.exists(local_path):
        os.makedirs(local_path)

    # Lister les fichiers/dossiers à cet emplacement
    files, folders = list_files_on_sftp_folder(sftp, remote_path)

    # Télécharger chaque fichier
    for file in files:
        remote_file_path = sftp_join(remote_path, file)
        local_file_path = os.path.join(local_path, file)
        try:
            sftp.get(remote_file_path, local_file_path)
        except Exception as e:
            print(f"Erreur lors du téléchargement de {remote_file_path}: {e}")

    # Récursion dans chaque sous-dossier
    for folder in folders:
        remote_folder_path = sftp_join(remote_path, folder)
        local_folder_path = os.path.join(local_path, folder)
        try:
            download_recursive(sftp, remote_folder_path, local_folder_path)
        except Exception as e:
            print(f"Erreur lors de la navigation dans {remote_folder_path}: {e}")


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
    if not sftp:
        print("Impossible de se connecter au serveur SFTP.")
        return

    print(f"---------------------------- Connexion SFTP ----------------------------")
    print(f"Connexion au serveur SFTP {host}:{port} avec l'utilisateur {username}.\n")

    download_recursive(sftp, parent_folder, dossier_client)

    print(
        f"---------------------------- Dossier distant: {parent_folder} ----------------------------"
    )
    files_list, folders_list = list_files_on_sftp_folder(sftp, parent_folder)

    print("Fichiers:")
    print(files_list)

    print("Dossiers:")
    print(folders_list)

    # Fermer la connexion SFTP
    sftp.close()


if __name__ == "__main__":
    main()
