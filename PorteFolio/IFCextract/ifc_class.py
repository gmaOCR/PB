import ifcopenshell
import ifcopenshell.geom
import ifcopenshell.util.element as Element
import pandas as pd


def get_entities_by_type(entities_list):
    entities_by_type = {}

    for entity in entities_list:
        entity_type = entity.is_a()
        if entity_type not in entities_by_type:
            entities_by_type[entity_type] = []
        entities_by_type[entity_type].append(entity)

    return entities_by_type


def get_properties_and_quantities(element):
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


def get_attributes_value(object_data, attribute):
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


class IFCObjectAnalyzer:
    """
    is_element = True : Give all geometric elements
    is_element = False : Give all non geometric elements
    """

    def __init__(self, ifc_path, is_element=True):
        self.ifc_path = ifc_path
        self.ifc_model = self.open_ifc_file()
        self.is_element = is_element
        if self.is_element:
            self.filtered_entities = self.ifc_model.by_type('IfcElement')
        else:
            self.filtered_entities = [e for e in self.ifc_model.by_type('IFCROOT') if not e.is_a('IfcElement')]
        self.all_element_types = self.get_all_element_types()

    def open_ifc_file(self):
        try:
            return ifcopenshell.open(self.ifc_path)
        except ifcopenshell.Error as e:
            raise ValueError(str(e))

    def get_filtered_entities(self):
        """a refactoriser"""
        return [e for e in self.all_entities if e.is_a('IfcElement') == self.is_element]

    def get_elements_structure(self):
        """A refactoriser"""
        filtered_entities = self.get_filtered_entities()
        elements_structure = {}

        for element in filtered_entities:
            element_type = element.is_a()
            if element_type not in elements_structure:
                elements_structure[element_type] = []

            elements_structure[element_type].append({
                "id": element.id(),
                "properties": get_properties_and_quantities(element),
            })

        return elements_structure

    def get_project_hierarchy(self):
        project = self.ifc_model.by_type("IfcProject")[0]
        site = project.IsDecomposedBy[0].RelatedObjects[0]
        building = site.IsDecomposedBy[0].RelatedObjects[0]

        return {
            "project": project.Name,
            "site": site.Name,
            "building": building.Name,
            "storeys": [
                {"name": storey.Name, "elements": self.get_elements_structure()}
                for storey in building.IsDecomposedBy[0].RelatedObjects
            ],
        }

    def get_all_element_types(self):
        list_of_element_types = list(set(element.is_a() for element in self.filtered_entities))
        return list_of_element_types

    # def extract_data(self, element_type):
    #
    #     elements = self.ifc_model.by_type(element_type)
    #     datas = {}
    #
    #     for element in elements:
    #         data_id = element.id()
    #         container = Element.get_container(element)
    #         container_name = container.Name if container else ""
    #         type_element = Element.get_type(element)
    #         type_name = type_element.Name if type_element else ""
    #         datas[data_id] = {
    #             "ExpressID": element.id(),
    #             "GlobalID": element.GlobalId,
    #             "Class": element.is_a(),
    #             "PredefinedType": container_name,
    #             "ObjectType": type_name,
    #             "QuantitiySets": Element.get_psets(element, qtos_only=True),
    #             "PropertySets": Element.get_psets(element, psets_only=True),
    #         }
    #     return datas

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

    # def export_ifc_to_CSV(self):
    #     data, pset_attributes = self.extract_data(self.get_all_element_types())
    #     attributes = ["ExpressID", "GlobalID", "Class", "PredefinedType", "Name", "Level", "ObjectType",
    #                   "QuantitiySets", "PropertySets"] + pset_attributes
    #     pandas_data = []
    #     for object_data in data:
    #         row = []
    #         for attribute in attributes:
    #             value = get_attributes_value(object_data, attribute)
    #             row.append(value)
    #         pandas_data.append(tuple(row))
    #     data_frame = pd.DataFrame.from_records(pandas_data, columns=attributes)
    #     data_frame.to_csv('csv/test')

    def export_ifc_to_csv(self):
        data, pset_attributes = self.extract_data(self.get_all_element_types())
        attributes = ["ExpressID", "GlobalID", "Class", "PredefinedType", "Name", "Level", "ObjectType"]

        # Créer un DataFrame à partir des données extraites
        df = pd.DataFrame(data)

        # S'assurer que les colonnes "PropertySets" et "QuantitiySets" contiennent bien des dictionnaires
        df['PropertySets'] = df['PropertySets'].apply(lambda x: x if isinstance(x, dict) else {})
        df['QuantitiySets'] = df['QuantitiySets'].apply(lambda x: x if isinstance(x, dict) else {})

        # Créer une nouvelle colonne pour chaque clé dans les dictionnaires "PropertySets"
        for key in pset_attributes:
            if f'PropertySets_{key}' not in df.columns:
                df[f'PropertySets_{key}'] = df['PropertySets'].apply(lambda x: x.get(key, None))

        # Créer une nouvelle colonne pour chaque clé dans les sous-dictionnaires "QuantitiySets"
        for sub_dict_name in df['QuantitiySets'].iloc[
            0].keys():  # Assumons que tous les éléments ont les mêmes sous-dictionnaires
            for key in pset_attributes:
                if f'QuantitiySets_{sub_dict_name}_{key}' not in df.columns:
                    df[f'QuantitiySets_{sub_dict_name}_{key}'] = df['QuantitiySets'].apply(
                        lambda x: x[sub_dict_name].get(key, None) if sub_dict_name in x else None)

        # Supprimer les colonnes 'PropertySets' et 'QuantitiySets' originales
        df = df.drop(columns=['PropertySets', 'QuantitiySets'])

        # Écrire le DataFrame dans un fichier CSV
        df.to_csv('csv/test.csv', index=False)

