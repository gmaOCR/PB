import csv
import json
import pandas as pd
import os
import zipfile


def write_data_to_csv(data, filename):
    # Convertir les données en DataFrame
    df = pd.DataFrame(data)

    # Vérifier si 'properties' ou 'quantities' existent dans les données
    columns_to_check = ['properties', 'quantities']
    columns_to_drop = [col for col in columns_to_check if col in df.columns]
    dataframes = [df.drop(columns=columns_to_drop)]
    for sub_dict_name in columns_to_check:
        if sub_dict_name in df.columns:
            # Séparer les données en fonction de la présence de 'properties' ou 'quantities'
            df_with_sub_dict = df[df[sub_dict_name].apply(lambda x: isinstance(x, dict))]
            df_without_sub_dict = df[~df[sub_dict_name].apply(lambda x: isinstance(x, dict))]

            # Traiter les données avec 'properties' ou 'quantities'
            if not df_with_sub_dict.empty:
                try:
                    sub_data = pd.json_normalize(df_with_sub_dict[sub_dict_name].tolist(), errors='ignore')
                    sub_data.columns = [f'{sub_dict_name}_{col}' for col in sub_data.columns]
                    dataframes.append(sub_data)
                except Exception as e:
                    print(f"Erreur lors de la normalisation des données pour {sub_dict_name}: {e}. Les données ne sont peut-être pas correctement structurées.")

            # Traiter les données sans 'properties' ou 'quantities'
            if not df_without_sub_dict.empty:
                print(df_without_sub_dict.items())
                # Ici, vous pouvez choisir comment traiter ces données
                pass

    # Concaténer toutes les DataFrames ensemble
    df = pd.concat(dataframes, axis=1)

    # Écrire le DataFrame dans un fichier CSV
    df.to_csv(filename, index=False)



def create_csv_files(data, prefix):
    csv_files = []
    for element_type, elements in data.items():
        filename = f'{prefix}_{element_type}.csv'
        write_data_to_csv(elements, filename)
        csv_files.append(filename)
    return csv_files


def compress_files(file_names, zip_name):
    with zipfile.ZipFile(zip_name, 'w') as zipf:
        for file in file_names:
            if os.path.exists(file):
                zipf.write(file)
                print(f"Added {file} to {zip_name}")
            else:
                print(f"File {file} does not exist")
