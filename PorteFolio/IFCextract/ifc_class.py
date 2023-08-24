import os
import zipfile

from contextlib import contextmanager
from .src.ifccsv import IfcCsv
import ifcopenshell
import ifcopenshell.geom
import ifcopenshell.util.element as Element
import pandas as pd


@contextmanager
def delete_file_after_use(file_path):
    try:
        yield file_path
    finally:
        # Supprimer le fichier après avoir quitté le contexte
        os.remove(file_path)


def get_entities_by_type(entities_list):
    entities_by_type = {}

    for entity in entities_list:
        entity_type = entity.is_a()
        if entity_type not in entities_by_type:
            entities_by_type[entity_type] = []
        entities_by_type[entity_type].append(entity)

    return entities_by_type


def get_attribute_value(object_data, attribute):
    if "." not in attribute:
        return object_data[attribute]
    elif "." in attribute:
        pset_name = attribute.split(".", 1)[0]
        prop_name = attribute.split(".", 1)[1]
        if pset_name in object_data["PropertySets"].keys():
            if prop_name in object_data["PropertySets"][pset_name].keys():
                return object_data["PropertySets"][pset_name][prop_name]
            else:
                return None
        if pset_name in object_data["QuantitiySets"].keys():
            if prop_name in object_data["QuantitiySets"][pset_name].keys():
                return object_data["QuantitiySets"][pset_name][prop_name]
            else:
                return None
        else:
            return None


def compress_to_zip_file(path_to_csv, path_to_zip):
    with zipfile.ZipFile(path_to_zip, 'a') as zipf:  # Open the zip file in append mode
        zipf.write(path_to_csv, arcname=os.path.basename(path_to_csv))  # Add the CSV file to the zip file


class IFCObjectAnalyzer:
    """
    is_element = True : Give all geometric elements
    is_element = False : Give all non geometric elements
    """

    def __init__(self, ifc_path, is_element=True):
        self.ifc_path = ifc_path
        self.ifc_model = ifcopenshell.open(self.ifc_path)
        self.is_element = is_element
        if self.is_element:
            self.filtered_entities = self.ifc_model.by_type('IfcElement')
        else:
            self.filtered_entities = [e for e in self.ifc_model.by_type('IFCROOT') if not e.is_a('IfcElement')]
        self.all_element_types = self.get_all_element_types()

    def get_all_element_types(self):
        list_of_element_types = list(set(element.is_a() for element in self.filtered_entities))
        return list_of_element_types

    def get_spatial_info(self, element):
        level_name = ""
        building_name = ""
        site_name = ""

        # Parcourir la structure spatiale pour obtenir les informations hiérarchiques
        spatial_element = element
        while spatial_element:
            print(spatial_element)
            if spatial_element.is_a("IfcBuildingStorey"):
                level_name = spatial_element.Name or ""
            elif spatial_element.is_a("IfcBuilding"):
                building_name = spatial_element.Name or ""
            elif spatial_element.is_a("IfcSite"):
                site_name = spatial_element.Name or ""

            spatial_element = Element.get_container(spatial_element)

        return level_name, building_name, site_name

    def extract_data(self, element_type):
        def add_pset_attributes(psets):
            for pset_name, pset_data in psets.items():
                for property_name in pset_data.keys():
                    pset_attributes.add(f'{pset_name}.{property_name}')

        pset_attributes = set()
        elements = self.ifc_model.by_type(element_type)
        datas = []

        for element in elements:
            container = Element.get_container(element)
            container_name = container.Name if container else ""
            psets = Element.get_psets(element, psets_only=True)
            add_pset_attributes(psets)
            qtos = Element.get_psets(element, qtos_only=True)
            add_pset_attributes(qtos)

            level_name, building_name, site_name = self.get_spatial_info(element)

            datas.append({
                "ExpressID": element.id(),
                "GlobalID": element.GlobalId,
                "Class": element.is_a(),
                "PredefinedType": Element.get_predefined_type(element),
                "Name": container_name,
                "Level": level_name,
                "Building": building_name,
                "Site": site_name,
                "ObjectType": Element.get_type(element).Name
                if Element.get_type(element)
                else "",
                "QuantitiySets": qtos,
                "PropertySets": psets,
            })
        return datas, list(pset_attributes)

    def export_ifc_to_csv(self):
        all_types = self.get_all_element_types()
        csv_files = []
        zip_path = 'media/zip/output.zip'

        for element_type in all_types:
            # Sélectionner les éléments de ce type
            elements = ifcopenshell.util.selector.Selector.parse(self.ifc_model, f".{element_type}")

            # Spécifier les attributs à exporter (adaptez cela selon vos besoins)
            attributes = ["ExpressID", "GlobalID", "Class", "PredefinedType", "Name", "Level", "ObjectType"]

            # Créer un objet IfcCsv et exporter vers CSV
            ifc_csv = IfcCsv()
            csv_path = f'media/csv/{element_type}.csv'
            ifc_csv.export(self.ifc_model, elements, attributes, output=csv_path, format="csv", delimiter=",", null="-")

            # Ajouter le chemin du fichier CSV à la liste pour la compression
            csv_files.append(csv_path)

        # Compresser les fichiers CSV dans un fichier ZIP
        for csv_file in csv_files:
            compress_to_zip_file(csv_file, zip_path)
            with delete_file_after_use(csv_file):
                pass  # Le fichier CSV sera supprimé après ce contexte

        return zip_path

    # def export_ifc_to_csv(self):
    #     all_types = self.get_all_element_types()
    #     csv_files = []
    #     for type in all_types:
    #         data, pset_attributes = self.extract_data(type)
    #         attributes = ["ExpressID", "GlobalID", "Class", "PredefinedType", "Name", "Level",
    #                       "ObjectType"] + pset_attributes
    #         pandas_data = []
    #         for obj_data in data:
    #             row = []
    #             for attribute in attributes:
    #                 value = get_attribute_value(obj_data, attribute)
    #                 row.append(value)
    #             pandas_data.append(row)
    #         dataframe = pd.DataFrame.from_records(pandas_data, columns=attributes)
    #         csv_path = f'media/csv/{type}.csv'
    #         dataframe.to_csv(csv_path)
    #         csv_files.append(csv_path)
    #     zip_path = 'media/zip/output.zip'
    #     for csv_file in csv_files:
    #         compress_to_zip_file(csv_file, zip_path)
    #         with delete_file_after_use(csv_file):
    #             pass  # Le fichier CSV sera supprimé après ce contexte
    #     return zip_path
