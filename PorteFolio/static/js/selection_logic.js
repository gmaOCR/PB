import * as THREE from 'three';

let previousSelectedObject = null;
let originalMaterial = null;

export async function handleObjectSelection(event, viewer, textField) {
    const pickedItem = await viewer.IFC.selector.pickIfcItem(true);

    // Si un objet a été sélectionné précédemment, réinitialisez sa couleur
    if (previousSelectedObject && originalMaterial) {
        previousSelectedObject.material = originalMaterial;
    }

    if (pickedItem) {
        console.log('Élément IFC sélectionné:', pickedItem);

        const props = await viewer.IFC.getProperties(pickedItem.modelID, pickedItem.id, true, false);
        console.log('Propriétés de l\'élément IFC:', props);

        originalMaterial = pickedItem.material;  // Stockez le matériau original
        const material = new THREE.MeshBasicMaterial({ color: 0xff0000 });
        pickedItem.material = material;

        // Afficher les informations de l'objet dans un champ textuel
//        material + properties
//        textField.value = JSON.stringify(pickedItem, null, 2) + "\n\nProperties:\n" + JSON.stringify(props, null, 2);
        textField.value = "Properties:\n" + JSON.stringify(props, null, 2);

        previousSelectedObject = pickedItem;
    } else {
        viewer.IFC.selector.unpickIfcItems();
        viewer.IFC.selector.unHighlightIfcItems();
        textField.value = "Aucun élément sélectionné";
        previousSelectedObject = null;
        originalMaterial = null;
    }
}
