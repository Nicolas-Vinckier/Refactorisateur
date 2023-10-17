import paramiko
import re
import time
import os

# === Dossier
dossier_client = "serveur_sftp"
local_path = os.path.join(os.getcwd(), dossier_client)

# === Chemin parent
parent_folder = "/"

# Créer le dossier client s'il n'existe pas
os.makedirs(dossier_client, exist_ok=True)
os.makedirs("PasswordFolder", exist_ok=True)


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def connect_to_sftp(host, port, username, password):
    try:
        transport = paramiko.Transport((host, port))
        transport.connect(username=username, password=password)
        sftp = paramiko.SFTPClient.from_transport(transport)
        return sftp
    except Exception as e:
        print(f"Erreur de connexion SFTP : {e}")
        return None


# Fonction qui affiche les dossiers et fichiers dans le dossier_client EN LOCAL
def list_files_in_client_folder():
    folders = [
        item
        for item in os.listdir(dossier_client)
        if os.path.isdir(os.path.join(dossier_client, item))
    ]
    folders.sort()

    print("Dossiers locaux dans le dossier client :")
    for entry in os.scandir(dossier_client):
        if entry.is_dir():
            print(entry.name)


def main():
    clear_screen()

    # Informations de connexion SFTP
    host = "ftp.cluster028.hosting.ovh.net"
    port = 22
    username = "myvcarh"

    # Lire le mot de passe depuis le fichier 'pass_ohmarket.txt'
    with open("PasswordFolder/myvcardpro.txt", "r") as f:
        password = f.read().strip()

    sftp = connect_to_sftp(host, port, username, password)

    print("---------------------------- Connexion SFTP ----------------------------")
    print(f"Connexion au serveur SFTP {host}:{port} avec l'utilisateur {username}.")

    if sftp:
        # print("Connexion SFTP réussie.")
        # Chemin du dossier à vérifier sur le serveur SFTP

        print("---------------------------- Dossier distant ----------------------------")
        print(f"Recherche dans le dossier distant suivant : {parent_folder}")

        pattern = re.compile(r"^\d{2}_\d{4}$")

        # Ajout d'une fonction pour voir le temps d'exécution de la fonction list_files_in_folders_with_pattern

        # ---------------------- Afficher les dossiers ----------------------
        list_files_in_client_folder()

        # Fermer la connexion SFTP
        sftp.close()
    else:
        print("La connexion SFTP a échoué.")


if __name__ == "__main__":
    main()
