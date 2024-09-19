import requests
import os
import platform
from bs4 import BeautifulSoup

import datetime
import locale

locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')

# Color constants
Bl = '\033[30m'
Re = '\033[1;31m'
Gr = '\033[1;32m'
Ye = '\033[1;33m'
Blu = '\033[1;34m'
Mage = '\033[1;35m'
Cy = '\033[1;36m'
Wh = '\033[1;37m'

def lire_texte_depuis_url(url):
    """Fetch text content from the given URL."""
    response = requests.get(url)
    response.raise_for_status()
    return response.text

def get_instagram_profile_picture(username):
    """Retrieve the Instagram profile picture URL for the given username."""
    url = f'https://www.instagram.com/{username}/'
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        meta_tag = soup.find('meta', property='og:image')
        if meta_tag:
            image_url = meta_tag.get('content')
            return image_url if image_url else "https://static.xx.fbcdn.net/rsrc.php/v1/ys/r/sflX1flVtBf.jpg"
        else:
            print(f"\n{Wh}[ {Re}- {Wh}] {Re}Photo de profil non trouvée")
            return None
    else:
        print(f"\n{Wh}[ {Re}- {Wh}] {Re}Erreur lors de la récupération de la page")
        return None

def remplacer_placeholders(texte, placeholders):
    """Replace placeholders in the text with values provided by the user."""
    valeurs = {}

    # Ask for values for each placeholder
    for placeholder in placeholders:
        valeur = input(f"Entrez la valeur pour '{placeholder}': ")
        valeurs[placeholder] = valeur

    # Get the pseudo and email from values
    pseudo = valeurs.get('PSEUDO', None)
    email = valeurs.get('EMAILVICTIM', None)

    if pseudo:
        # Get Instagram profile picture for the given pseudo
        image_url = get_instagram_profile_picture(pseudo)
        if image_url:
            # Replace 'PP' with the profile picture URL
            texte = texte.replace('PP', image_url)

    date_actuelle = datetime.datetime.now()
    date_future = date_actuelle + datetime.timedelta(days=1)

    texte = texte.replace('JOUR', f"{date_future.day}")
    texte = texte.replace('MOIS', f"{date_actuelle.strftime('%B')}")
    texte = texte.replace('ANNEE', f"{date_actuelle.year}")

    # Replace 'PSEUDO' with the pseudo and 'EMAILVICTIM' with the email
    if pseudo:
        texte = texte.replace('PSEUDO', pseudo)
    if email:
        texte = texte.replace('EMAILVICTIM', email)

    return texte

def ecrire_texte_dans_fichier(nom_fichier, texte):
    """Write the modified text into an HTML file and open it."""
    with open(nom_fichier, 'w', encoding='utf-8') as fichier:
        fichier.write(texte)

    # Open the file based on the operating system
    if platform.system() == 'Windows':
        os.system(f'start {nom_fichier}')
    elif platform.system() == 'Darwin':
        os.system(f'open {nom_fichier}')
    elif platform.system() == 'Linux':
        os.system(f'xdg-open {nom_fichier}')

# URL of the template
url_fichier = "https://raw.githubusercontent.com/GGamesDev/MailInsta/refs/heads/main/Mail3.html"

# Fetch the text from the URL
texte = lire_texte_depuis_url(url_fichier)

# Define the placeholders
placeholders = ["PSEUDO", "EMAILVICTIM"]

# Replace placeholders with values and profile picture
texte_modifie = remplacer_placeholders(texte, placeholders)

# Name for the modified HTML file
nom_fichier_modifie = "index.html"

# Write the modified text into the file and open it
ecrire_texte_dans_fichier(nom_fichier_modifie, texte_modifie)