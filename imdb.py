# Author: Paul M. Nakasone
# Descrição: Este script, permite buscar automaticamente filmes no IMDb (Internet Movie Database) com base em arquivos ".mkv" e incluir tags relevantes. O script utiliza a API do OMDB para obter dados de filmes do IMDb e realiza as operações necessárias de tagging.

# ATENÇÂO: Certifique-se de alterar os campos "OMDB_API_KEY" e "Encoder field" antes de iniciar o script.

import requests
import re
import xml.etree.ElementTree as ET
import os
import subprocess

OMDB_API_KEY = "XXXXXXXX" # Cole sua chave API aqui!
VERSION = "0.09 (Whatever Will Be, Will Be)"

def search_imdb(filename, output_dir):
    filename = os.path.basename(filename)
    filename = filename.replace(".", " ")

    pattern = r"(.+?) (\d{4})"
    match = re.search(pattern, filename)
    if match:
        title = match.group(1)
        release_year = match.group(2)
    else:
        print("Formato de nome de arquivo inválido. Por favor, certifique-se de que segue as regras exigidas.")
        return

    print(f"Buscando por `{title}` ({release_year})")

    imdb_movie_data = search_imdb_api(title)

    if imdb_movie_data:
        aka_movie = find_movie_in_aka(imdb_movie_data, title, release_year)
        if aka_movie:
            save_to_file("IMDB", aka_movie, output_dir, title, release_year)  # Include title and release_year arguments
            print("Filme encontrado no IMDb.")
        else:
            imdb_movie = find_movie_by_year(imdb_movie_data, release_year)
            if imdb_movie:
                save_to_file("IMDB", imdb_movie, output_dir, title, release_year)  # Include title and release_year arguments
                print("Filme encontrado no IMDb.")
            else:
                print("Filme não encontrado no IMDb.")
    else:
        print("Filme não encontrado no IMDb.")

def search_imdb_api(title):
    url = f"http://www.omdbapi.com/?s={title}&apikey={OMDB_API_KEY}"
    try:
        response = requests.get(url)
        data = response.json()

        if data["Response"] == "True":
            return data["Search"]
        else:
            return None
    except requests.exceptions.RequestException as e:
        print(f"Ocorreu um erro ao buscar dados na API do OMDB: {e}")
        return None

def find_movie_by_year(movies, release_year):
    for movie in movies:
        if movie.get("Year") == release_year:
            return movie
    return None

def find_movie_in_aka(movies, title, release_year):
    for movie in movies:
        if movie.get("Title") == title and movie.get("Year") == release_year:
            return movie
    return None

def save_to_file(service, movie_data, output_dir, title, release_year):
    root = ET.Element("Tags")
    tag_element = ET.SubElement(root, "Tag")
    targets_element = ET.SubElement(tag_element, "Targets")
    target_type_value_element = ET.SubElement(targets_element, "TargetTypeValue")
    target_type_value_element.text = "50"

    if movie_data:
        service_element = ET.SubElement(tag_element, "Simple")
        service_name_element = ET.SubElement(service_element, "Name")
        service_name_element.text = service
        service_id_element = ET.SubElement(service_element, "String")
        service_id_element.text = str(movie_data["imdbID"])

        # Add the new Encoder field
        encoder_element = ET.SubElement(tag_element, "Simple")
        encoder_name_element = ET.SubElement(encoder_element, "Name")
        encoder_name_element.text = "Encoder"
        encoder_value_element = ET.SubElement(encoder_element, "String")
        encoder_value_element.text = "Meu_Nick"

        # Add the new Movie Name field
        movie_name_element = ET.SubElement(tag_element, "Simple")
        movie_name_name_element = ET.SubElement(movie_name_element, "Name")
        movie_name_name_element.text = "Movie Name"
        movie_name_value_element = ET.SubElement(movie_name_element, "String")
        movie_name_value_element.text = f"{title} ({release_year})"

    xml_file_path = os.path.join(output_dir, "imdb_info.xml")
    tree = ET.ElementTree(root)
    tree.write(xml_file_path, encoding="utf-8", xml_declaration=True)
    with open(xml_file_path, "r+") as file:
        content = file.read()
        file.seek(0, 0)
        file.write('<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE Tags SYSTEM "matroskatags.dtd">\n' + content)

def add_tags_to_mkv(mkv_file):
    try:
        xml_file_path = os.path.abspath("imdb_info.xml")
        subprocess.run(["mkvpropedit", mkv_file, "--tags", f"global:{xml_file_path}"])
        print(f"Tags globais adicionados ao {mkv_file}")
    except subprocess.CalledProcessError as e:
        print(f"Ocorreu um erro ao adicionar as tags globais ao {mkv_file}: {e}")

def remove_encoded_date(mkv_file_path):
    command = f"mkvpropedit {mkv_file_path} --delete date"
    subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

folder_location = input("Digite a localização da pasta: ")
output_dir = folder_location

print(f"Versão do script em execução: {VERSION}")

for file_name in os.listdir(folder_location):
    if file_name.endswith(".mkv"):
        file_path = os.path.join(folder_location, file_name)
        search_imdb(file_path, output_dir)
        add_tags_to_mkv(file_path)
        remove_encoded_date(file_path)
