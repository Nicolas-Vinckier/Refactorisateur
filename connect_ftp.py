import paramiko
import os
import time

# === Dossier local racine
local_folder = os.path.abspath("serveur_sftp")

# Assurez-vous que le dossier local existe
os.makedirs(local_folder, exist_ok=True)
os.makedirs("PasswordFolder", exist_ok=True)

# === Chemin parent sur le serveur distant
parent_folder = "/home/myvcarh/www/"


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def list_files_on_sftp_folder(sftp, path):
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


def download_recursive(sftp, remote_path, local_root):
    local_path = os.path.join(local_root, remote_path.lstrip("/"))
    if not os.path.exists(local_path):
        os.makedirs(local_path)

    # Vérification d'existence du chemin distant
    try:
        sftp.stat(remote_path)
    except FileNotFoundError:
        print(f"Chemin distant introuvable: {remote_path}")
        return

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
        download_recursive(sftp, remote_folder_path, local_folder_path)


def main():
    while True:
        clear_screen()
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

        print(
            f"Connexion au serveur SFTP {host}:{port} avec l'utilisateur {username}.\n"
        )
        download_recursive(sftp, parent_folder, local_folder)

        # Fermer la connexion SFTP
        sftp.close()

        # Attendez 10 minutes avant de resynchroniser
        time.sleep(600)


if __name__ == "__main__":
    main()
