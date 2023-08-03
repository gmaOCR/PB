import os
import subprocess
import zipfile

from contextlib import contextmanager
from django.http import StreamingHttpResponse

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
            datas.append({
                "ExpressID": element.id(),
                "GlobalID": element.GlobalId,
                "Class": element.is_a(),
                "PredefinedType": Element.get_predefined_type(element),
                "Name": container_name,
                "Level": Element.get_container(element).Name
                if Element.get_container(element)
                else "",
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
        for type in all_types:
            data, pset_attributes = self.extract_data(type)
            attributes = ["ExpressID", "GlobalID", "Class", "PredefinedType", "Name", "Level",
                          "ObjectType"] + pset_attributes
            pandas_data = []
            for obj_data in data:
                row = []
                for attribute in attributes:
                    value = get_attribute_value(obj_data, attribute)
                    row.append(value)
                pandas_data.append(row)
            dataframe = pd.DataFrame.from_records(pandas_data, columns=attributes)
            csv_path = f'media/csv/{type}.csv'
            dataframe.to_csv(csv_path)
            csv_files.append(csv_path)
        zip_path = 'media/zip/output.zip'
        for csv_file in csv_files:
            compress_to_zip_file(csv_file, zip_path)
            with delete_file_after_use(csv_file):
                pass  # Le fichier CSV sera supprimé après ce contexte
        return zip_path

    def export_ifc_to_obj(self):
        obj_path = 'media/obj'
        dir_path = os.path.dirname(os.path.realpath(__file__))
        # Construisez le chemin vers IfcConvert
        ifc_convert_path = os.path.join(dir_path, 'IfcConvert-0.4.0-rc2-linux64/IfcConvert')
        command = f"{ifc_convert_path} {self.ifc_path} {obj_path}"
        process = subprocess.Popen(command, shell=True)
        process.wait()

        # Vérifiez le code de sortie
        if process.returncode != 0:
            raise Exception("Error: The IfcConvert command failed.")

        # Vérifiez que le fichier OBJ existe
        if os.path.exists(obj_path):
            return obj_path
        else:
            raise Exception("Error: The OBJ file was not created.")




# testing
def convert_ifc(request):
    def stream_response():
        obj_path = 'media/obj'
        dir_path = os.path.dirname(os.path.realpath(__file__))
        ifc_convert_path = os.path.join(dir_path, 'IfcConvert-0.4.0-rc2-linux64/IfcConvert')
        command = f"{ifc_convert_path} {request.FILES['ifc_file'].temporary_file_path()} {obj_path}"

        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        while True:
            output = process.stdout.readline()

            # Parse the output to get the progress
            # This will depend on what IfcConvert outputs
            progress = parse_progress(output)

            yield f"data: {progress}\n\n"

            if process.poll() is not None:
                break

    return StreamingHttpResponse(stream_response(), content_type='text/event-stream')
