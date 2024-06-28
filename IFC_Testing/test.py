# def extract_key_properties(element):
#     """Extraire les propriétés clés d'un élément."""
#     # Créer un dictionnaire vide pour stocker les données
#     data = {}
#     # Extraire les informations générales
#     data["Nom"] = element.Name if hasattr(element, 'Name') else None
#     data["Description"] = element.Description if hasattr(element, 'Description') else None
#     # Extraire les informations de géométrie
#     if hasattr(element, 'ObjectPlacement'):
#         placement = element.ObjectPlacement.RelativePlacement
#         if hasattr(placement, 'Location'):
#             data["Localisation"] = str(placement.Location.Coordinates)
#         if hasattr(placement, 'Axis'):
#             data["Orientation"] = str(placement.Axis.DirectionRatios)
#     # Extraire les informations sur le type de l'élément
#     data["Type"] = element.is_a()
#     # Extraire les informations sur les matériaux
#     if hasattr(element, 'HasAssociations'):
#         for association in element.HasAssociations:
#             if association.is_a("IfcRelAssociatesMaterial"):
#                 material_select = association.RelatingMaterial
#                 if material_select.is_a("IfcMaterial"):
#                     data["Material"] = material_select.Name
#     return data
#
# dataframes = {}
#
# # Parcourir tous les types d'élément dans le fichier IFC
# for element_type in model.by_type("IfcBuildingElement"):
#     # Extraire toutes les propriétés de l'élément
#     element_data = extract_key_properties(element_type)
#     # Si le type d'élément n'existe pas encore dans notre dictionnaire, créez-le avec une liste vide
#     if element_type.is_a() not in dataframes:
#         dataframes[element_type.is_a()] = []
#     # Ajoutez les données à notre liste pour ce type d'élément
#     dataframes[element_type.is_a()].append(pd.DataFrame(element_data, index=[0]))
#
# # Concaténer tous les dataframes et enregistrer chaque dataframe en tant que fichier CSV distinct
# for element_type, df_list in dataframes.items():
#     df = pd.concat(df_list, ignore_index=True)
#     df.to_csv(f"{element_type}.csv", index=False)


# def extract_geometry(element):
#     """Extraire les informations de géométrie d'un élément."""
#     data = {}
#     if hasattr(element, 'ObjectPlacement'):
#         placement = element.ObjectPlacement.RelativePlacement
#         if hasattr(placement, 'Location'):
#             data["Localisation"] = str(placement.Location.Coordinates)
#         if hasattr(placement, 'Axis'):
#             data["Orientation"] = str(placement.Axis.DirectionRatios)
#     return data
#
# # Parcourir tous les étages dans le fichier IFC
# for storey in model.by_type("IfcBuildingStorey"):
#     dataframes = []
#     # Vérifier si l'étage contient des éléments
#     if hasattr(storey, 'ContainsElements'):
#         # Parcourir tous les éléments de l'étage
#         for rel in storey.ContainsElements:
#             for element in rel.RelatedElements:
#                 # Extraire les informations de géométrie de l'élément
#                 element_data = extract_geometry(element)
#                 dataframes.append(pd.DataFrame(element_data, index=[0]))
#     # Concaténer tous les dataframes et enregistrer le dataframe en tant que fichier CSV
#     df = pd.concat(dataframes, ignore_index=True)
#     df.to_csv(f"{storey.Name}.csv", index=False)

# def extract_element_details(element):
#     """Extraire les détails de chaque élément"""
#     data = {}
#     data["Type"] = element.is_a()
#     data["Name"] = element.Name if hasattr(element, 'Name') else None
#     data["Description"] = element.Description if hasattr(element, 'Description') else None
#     data["Material"] = None
#     if hasattr(element, 'HasAssociations'):
#         for association in element.HasAssociations:
#             if association.is_a("IfcRelAssociatesMaterial"):
#                 material_select = association.RelatingMaterial
#                 if material_select.is_a("IfcMaterial"):
#                     data["Material"] = material_select.Name
#     # Extract geometry information
#     if hasattr(element, 'ObjectPlacement'):
#         placement = element.ObjectPlacement.RelativePlacement
#         if hasattr(placement, 'Location'):
#             data["Location"] = str(placement.Location.Coordinates)
#         if hasattr(placement, 'Axis'):
#             data["Orientation"] = str(placement.Axis.DirectionRatios)
#     return data

# Parcourir tous les étages dans le fichier IFC
# for storey in model.by_type("IfcBuildingStorey"):
#     dataframes = []
#     # Vérifier si l'étage contient des éléments
#     if hasattr(storey, 'ContainsElements'):
#         # Parcourir tous les éléments de l'étage
#         for rel in storey.ContainsElements:
#             for element in rel.RelatedElements:
#                 # Extraire les détails de l'élément
#                 element_data = extract_element_details(element)
#                 dataframes.append(pd.DataFrame(element_data, index=[0]))
#     # Concaténer tous les dataframes et enregistrer le dataframe en tant que fichier CSV
#     df = pd.concat(dataframes, ignore_index=True)
#     df.to_csv(f"{storey.Name}.csv", index=False)

# storeys = model.by_type("IfcBuildingStorey")
# for storey in storeys:
#     print(f"ID: {storey.id()}, Name: {storey.Name}, Description: {storey.Description}, Elevation: {storey.Elevation}")
#
# columns = model.by_type("IfcColumn")
# for column in columns:
#     print(f"ID: {column.id()}, Name: {column.Name}, Description: {column.Description}, Object Type: {column.ObjectType}")
#
# print(columns)
# def get_storey(element):
#     for rel in element.ContainedInStructure:
#         if rel.RelatingStructure.is_a("IfcBuildingStorey"):
#             return rel.RelatingStructure
#         else:
#             return get_storey(rel.RelatingStructure)
#
# columns = model.by_type("IfcColumn")
# for column in columns:
#     storey = get_storey(column)
#     print(f"ID: {column.id()}, Name: {column.Name}, Storey: {storey.Name if storey else 'N/A'}")