import csv
import os
import zipfile

import ifcopenshell


def get_entities_by_type(entities_list):
    entities_by_type = {}

    for entity in entities_list:
        entity_type = entity.is_a()
        if entity_type not in entities_by_type:
            entities_by_type[entity_type] = []
        entities_by_type[entity_type].append(entity)

    return entities_by_type


class IFCObjectAnalyzer:
    def __init__(self, ifc_path):
        self.ifc_path = ifc_path
        self.ifc_model = self.open_ifc_file()
        self.element_obj = self.get_element_ent()
        self.non_element_obj = self.get_non_element_ent()

    def open_ifc_file(self):
        try:
            return ifcopenshell.open(self.ifc_path)
        except ifcopenshell.Error as e:
            raise ValueError(str(e))

    def get_all_entities(self):
        all_entities = self.ifc_model.by_type("IFCROOT")
        return all_entities

    def get_element_ent(self):
        entities = self.get_all_entities()
        elements_entities = []
        for e in entities:
            if e.is_a('IfcElement'):
                elements_entities.append(e)
        return elements_entities

    def get_non_element_ent(self):
        entities = self.get_all_entities()
        non_elements_entities = []
        for e in entities:
            if not e.is_a('IfcElement'):
                non_elements_entities.append(e)
        return non_elements_entities

    def export_all_to_csv(self):
        csv_files = []
        elements_by_type = self.extract_geometry_from_elements()

        for element_type, elements in elements_by_type.items():
            filename = f'{element_type}_output.csv'
            with open(filename, 'w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=elements[0].keys())
                writer.writeheader()
                for element in elements:
                    writer.writerow(element)
            csv_files.append(filename)

        return csv_files

    @staticmethod
    def compress_files(file_names, zip_name):
        with zipfile.ZipFile(zip_name, 'w') as zipf:
            for file in file_names:
                if os.path.exists(file):  # Add this
                    zipf.write(file)
                    print(f"Added {file} to {zip_name}")  # Add this
                else:
                    print(f"File {file} does not exist")  # Add this

    def resolve_ifc_id(self, ifc_id_str):
        """Résout un identifiant IFC en une valeur lisible """
        if ifc_id_str.startswith("#"):
            id_num = int(ifc_id_str[1:])
            entity = self.ifc_model.by_id(id_num)
            return entity.Name if hasattr(entity, "Name") else str(entity)
        else:
            return ifc_id_str

    def extract_geometry_from_elements(self):
        elements_by_type = {}
        elements_entities = self.get_element_ent()

        for element in elements_entities:
            if element.is_a('IfcElement'):
                element_type = element.is_a()
                if element_type not in elements_by_type:
                    elements_by_type[element_type] = []
                element_details = self.get_element_attributes(element)  # Get the attributes of the element
                # Resolve IFC IDs in the element details
                for key, value in element_details.items():
                    if isinstance(value, str):
                        element_details[key] = self.resolve_ifc_id(value)
                elements_by_type[element_type].append(element_details)

        return elements_by_type

    def get_element_attributes(self, element):
        element_dict = {}
        for attr_name in element.get_info():
            attr_value = element.get_info()[attr_name]
            if isinstance(attr_value, ifcopenshell.entity_instance):
                attr_value = self.get_element_attributes(attr_value)  # Recursive call for nested entities
            elif isinstance(attr_value, str) and attr_value.startswith('#'):
                try:
                    id = int(attr_value[1:])  # Strip off the '#' and convert to integer
                    ref_entity = self.ifc_model.by_id(id)
                    attr_value = self.get_element_attributes(ref_entity)  # Recursive call for referenced entities
                except (ValueError, RuntimeError):
                    pass  # If conversion to integer fails or entity not found, ignore this value
            element_dict[attr_name] = attr_value

        # Add properties and quantities to the element dictionary if it is an IfcElement
        if element.is_a("IfcElement"):
            properties_and_quantities = self.get_properties_and_quantities(element)
            element_dict.update(properties_and_quantities)

        return element_dict

    def get_properties_and_quantities(self, element):
        properties = {}
        quantities = {}

        is_defined_by = element.IsDefinedBy
        for rel_defines_by_property in is_defined_by:
            if rel_defines_by_property.is_a("IfcRelDefinesByProperties"):
                property_set = rel_defines_by_property.RelatingPropertyDefinition
                if property_set.is_a("IfcPropertySet"):
                    for property in property_set.HasProperties:
                        if property.is_a("IfcPropertySingleValue"):
                            properties[property.Name] = property.NominalValue.wrappedValue
                elif property_set.is_a("IfcElementQuantity"):
                    for quantity in property_set.Quantities:
                        if quantity.is_a("IfcPhysicalSimpleQuantity"):
                            quantities[quantity.Name] = quantity[0]
        return {"properties": properties, "quantities": quantities}

