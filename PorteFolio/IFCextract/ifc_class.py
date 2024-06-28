import os
import zipfile
from contextlib import contextmanager
from .src.ifccsv import IfcCsv
import ifcopenshell
import pandas as pd


@contextmanager
def delete_file_after_use(file_path):
    """Context manager to delete a file after use."""
    try:
        yield file_path
    finally:
        os.remove(file_path)


def compress_to_zip_file(path_to_csv, path_to_zip):
    """Compress a CSV file into a ZIP file."""
    with zipfile.ZipFile(path_to_zip, 'a') as zipf:
        zipf.write(path_to_csv, arcname=os.path.basename(path_to_csv))


class IFCObjectAnalyzer:
    """
    Analyzes IFC objects and exports them to CSV.

    Attributes:
        is_element (bool): Whether to analyze geometric elements or non-geometric elements.
    """

    def __init__(self, ifc_path, is_element=True):
        """Initialize with IFC path and element type."""
        self.ifc_path = ifc_path
        self.ifc_model = ifcopenshell.open(self.ifc_path)
        self.is_element = is_element
        self.filtered_entities = self._filter_entities()
        self.all_element_types = self._get_all_element_types()

    def get_entities_by_type(self, entities_list):
        entities_by_type = {}

        for entity in entities_list:
            entity_type = entity.is_a()
            if entity_type not in entities_by_type:
                entities_by_type[entity_type] = []
            entities_by_type[entity_type].append(entity)
        return entities_by_type

    def _filter_entities(self):
        """Filter entities based on their type."""
        if self.is_element:
            return self.ifc_model.by_type('IfcElement')
        return [e for e in self.ifc_model.by_type('IFCROOT') if not e.is_a('IfcElement')]

    def _get_all_element_types(self):
        """Get a list of all element types."""
        return list(set(element.is_a() for element in self.filtered_entities))

    def _get_spatial_info(self, element):
        """Get spatial information for the given element."""
        spatial_info = {"IfcBuildingStorey": "", "IfcBuilding": "", "IfcSite": ""}
        spatial_element = element.ObjectPlacement
        while spatial_element:
            if spatial_element.is_a("IfcLocalPlacement"):
                relative_to = spatial_element.PlacementRelTo
                if relative_to:
                    relative_to_element = relative_to.PlacesObject[0]
                    element_type = relative_to_element.is_a()
                    if element_type in spatial_info:
                        spatial_info[element_type] = relative_to_element.Name or ""
                    spatial_element = relative_to
                else:
                    spatial_element = None
            else:
                spatial_element = None
        return spatial_info["IfcBuildingStorey"], spatial_info["IfcBuilding"], spatial_info["IfcSite"]

    def _add_information(self, csv_path):
        """Add spatial information to the CSV file."""
        dataframe = pd.read_csv(csv_path)
        dataframe["Level"] = ""
        dataframe["Building"] = ""
        dataframe["Site"] = ""
        dataframe["ObjectType"] = ""
        for index, row in dataframe.iterrows():
            try:
                express_id = int(row["ExpressID"])
                element = self.ifc_model.by_id(express_id)
                if element:
                    object_type = element.ObjectType if element.ObjectType else "-"
                    level_name, building_name, site_name = self._get_spatial_info(element)
                    dataframe.at[index, "Level"] = level_name
                    dataframe.at[index, "Building"] = building_name
                    dataframe.at[index, "Site"] = site_name
                    dataframe.at[index, "ObjectType"] = object_type
            except ValueError:
                print(f"Invalid ExpressID at row {index}: {row['ExpressID']}")
        dataframe.to_csv(csv_path, index=False)

    def export_ifc_to_csv(self):
        """Export IFC data to CSV and compress into a ZIP file."""
        csv_files = []
        zip_path = 'media/zip/output.zip'
        for element_type in self.all_element_types:
            elements = ifcopenshell.util.selector.Selector.parse(self.ifc_model, f".{element_type}")
            attributes = ["PredefinedType", "Name", "Level", "ObjectType"]
            ifc_csv = IfcCsv()
            csv_path = f'media/csv/{element_type}.csv'
            ifc_csv.export(self.ifc_model, elements, attributes, output=csv_path, format="csv", delimiter=",", null="-")
            dataframe = pd.read_csv(csv_path)
            dataframe['ExpressID'] = [element.id() for element in elements]
            dataframe.to_csv(csv_path, index=False)
            self._add_information(csv_path)
            csv_files.append(csv_path)

        for csv_file in csv_files:
            compress_to_zip_file(csv_file, zip_path)
            with delete_file_after_use(csv_file):
                pass

        return zip_path
