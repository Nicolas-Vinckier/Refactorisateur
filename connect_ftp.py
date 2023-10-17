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


def connect_to_sftp(host, port, username, password):
    try:
        transport = paramiko.Transport((host, port))
        transport.connect(username=username, password=password)
        sftp = paramiko.SFTPClient.from_transport(transport)
        return sftp
    except Exception as e:
        print(f"Erreur de connexion SFTP : {e}")
        return None


# Fonction qui affiche les dossier et fichier dans le dossier_client EN LOCAL
def list_files_in_client_folder():
    folders = [
        item
        for item in os.listdir(dossier_client)
        if os.path.isdir(os.path.join(dossier_client, item))
    ]
    folders.sort()

    # Affiche les dossiers trouvés
    if len(folders) > 0:
        print("-------------- Dossier local --------------")
        print(f"Dossiers trouvés : {folders}")
    else:
        print("-------------- Dossier local --------------")
        print("Aucun dossier n'a été trouvé.")


def main():
    # Informations de connexion SFTP
    host = ""
    port = 22
    username = ""

    # Lire le mot de passe depuis le fichier 'pass_ohmarket.txt'
    with open("PasswordFolder\pass_ohmarket.txt", "r") as f:
        password = f.read().strip()

    sftp = connect_to_sftp(host, port, username, password)

    print("-------------- Connexion SFTP --------------")
    print(f"Connexion au serveur SFTP {host}:{port} avec l'utilisateur {username}.")

    if sftp:
        print("Connexion SFTP réussie.")
        # Chemin du dossier à vérifier sur le serveur SFTP
        parent_folder = "/www.optimhome-market.com/wp-content/uploads/"

        print("-------------- Dossier distant --------------")
        print(f"Recherche dans le dossier distant suivant : {parent_folder}")

        pattern = re.compile(r"^\d{2}_\d{4}$")

        # Ajout d'une fonction pour voir le temps d'exécution de la fonction list_files_in_folders_with_pattern

        # ---------------------- Reche662it [00:38, 15.48it/s]rche des fichiers ----------------------
        start_time = time.time()
        print("Recherche des fichiers en cours...")

        # =================================== Décommenter pour rechercher les fichiers sur le serveur SFTP ===================================
        list_files_in_folders_with_pattern(sftp, parent_folder, pattern, output_file)

        temps_execution = time.time() - start_time
        temps_execution = round(temps_execution, 2)
        print(f"Temps d'exécution : {temps_execution} secondes")

        # ---------------------- Formatage du fichier texte ----------------------
        formatage_fichier_texte(output_file)

        list_files_in_client_folder()

        formatage_fichier_texte_local(already_downloaded)

        fichier_a_telecharger()

        # ---------------------- Téléchargement des fichiers ----------------------
        start_time = time.time()
        with open(to_download, "r") as f:
            file_list = f.readlines()

        # ====================== Téléchargement des fichiers sur le serveur SFTP ======================
        download_files(sftp, to_download, local_path)

        temps_execution = time.time() - start_time
        temps_execution = round(temps_execution, 2)
        print(f"Temps d'exécution : {temps_execution} secondes")

        # Fermer la connexion SFTP
        sftp.close()
    else:
        print("La connexion SFTP a échoué.")


if __name__ == "__main__":
    main()
