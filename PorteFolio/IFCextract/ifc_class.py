import re
from collections import defaultdict


class IFCObjectAnalyzer:
    def __init__(self, ifc_obj):
        self.ifc_obj = ifc_obj

    def get_all_entities(self):
        return self.ifc_obj.by_type("IFCROOT")

    def uniq_type_list(self):
        entities = self.get_all_entities()
        entity_types = [entity.is_a() for entity in entities]
        return list(dict.fromkeys(entity_types))

    def count_entity_types(self):
        entities = self.get_all_entities()
        entity_counts = defaultdict(int)

        for entity in entities:
            entity_type = entity.is_a()
            entity_counts[entity_type] += 1

        sorted_entity_counts = dict(sorted(entity_counts.items()))
        return sorted_entity_counts

    def get_entities_by_type(self):
        entities = self.get_all_entities()
        entities_by_type = {}

        for entity in entities:
            entity_type = entity.is_a()
            if entity_type not in entities_by_type:
                entities_by_type[entity_type] = []
            entities_by_type[entity_type].append(entity)

        return entities_by_type
