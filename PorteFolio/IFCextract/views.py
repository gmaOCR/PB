from django.shortcuts import render, redirect
from .forms import IfcFileForm
from .ifc_class import IFCObjectAnalyzer

import ifcopenshell


def upload_ifc(request):
    form = IfcFileForm()

    if request.method == 'POST':
        form = IfcFileForm(request.POST, request.FILES)
        if form.is_valid():
            ifc_file = form.save()
            ifc_path = ifc_file.file.path
            ifc_model = ifcopenshell.open(ifc_path)
            analyzer = IFCObjectAnalyzer(ifc_model)

            entities_by_type = analyzer.get_entities_by_type()
            # Créez une liste de dictionnaires pour chaque type d'entité avec des clés 'type' et 'entities'
            entity_data = [{'type': entity_type, 'entities': entities} for entity_type, entities in entities_by_type.items()]

            context = {
                'entity_data': entity_data,
            }
            print(context)
            return render(request, 'result.html', context=context)

    return render(request, 'upload.html', {'form': form})

