import * as THREE from 'three';
import { shouldIgnoreSelection } from './preselection_logic.js';

let previousSelectedObject = null;
let originalMaterial = null;

export async function handleObjectSelection(event, viewer, textField) {
    if (shouldIgnoreSelection()) {
        return;
    }

    const pickedItem = await viewer.IFC.selector.pickIfcItem(true);

    // Si un objet a été sélectionné précédemment, réinitialisez sa couleur
    if (previousSelectedObject && originalMaterial) {
        previousSelectedObject.material = originalMaterial;
    }

    if (pickedItem) {
        console.log('Élément IFC sélectionné:', pickedItem);

        const props = await viewer.IFC.getProperties(pickedItem.modelID, pickedItem.id, true, false);
        console.log('Propriétés de l\'élément IFC:', props);

        // Afficher les informations de l'objet dans un champ textuel
        textField.value = "Properties:\n" + JSON.stringify(props, null, 2);

    } else {
        viewer.IFC.selector.unHighlightIfcItems();
        textField.value = "Aucun élément sélectionné";
        previousSelectedObject = null;
        originalMaterial = null;
    }
}
