import paramiko
import os

# === Dossier local
dossier_client = "serveur_sftp"
os.makedirs(dossier_client, exist_ok=True)
os.makedirs("PasswordFolder", exist_ok=True)

# === Chemin parent sur le serveur distant
parent_folder = "/home/myvcarh/www/"

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def list_files_on_sftp_folder(sftp, path):
    """
    Liste et affiche les dossiers et fichiers du serveur SFTP.
    """
    try:
        items = sftp.listdir_attr(path)
        for item in items:
            file_type = "Dossier" if item.st_mode & 0o40000 else "Fichier"  # vérifie si c'est un dossier
            print(f"{file_type}: {item.filename}")
    except Exception as e:
        print(f"Erreur lors de la liste des fichiers SFTP : {e}")

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
        print(f"---------------------------- Dossier distant: {parent_folder} ----------------------------")
        list_files_on_sftp_folder(sftp, parent_folder)
        
        # Fermer la connexion SFTP
        sftp.close()
    else:
        print("La connexion SFTP a échoué.")

if __name__ == "__main__":
    main()
