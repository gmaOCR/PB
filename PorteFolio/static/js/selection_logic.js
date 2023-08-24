import * as THREE from 'three';

let previousSelectedObject = null;
let originalMaterial = null;

const attributesToShow = [
  'ObjectType.value',
  'Name.value',
  'Description.value',
  'GlobalId.value',
  'expressID',
  // Ajoutez d'autres chemins d'attributs que vous souhaitez afficher ici
];

function findLevelAndBuilding(props) {
  let level = null;
  let building = null;

  function traverse(obj) {
    if (obj.hasOwnProperty('Level')) {
      level = obj['Level'].value; // ou simplement obj['Level'] selon la structure
    }
    if (obj.hasOwnProperty('Building')) {
      building = obj['Building'].value; // ou simplement obj['Building']
    }
    for (const key in obj) {
      if (typeof obj[key] === 'object' && obj[key] !== null) {
        traverse(obj[key]); // Parcours récursif des propriétés imbriquées
      }
    }
  }

  traverse(props);
  return { level, building };
}

function listAttributes(obj, prefix = '') {
  let attributes = [];
  for (const key in obj) {
    if (typeof obj[key] === 'object' && obj[key] !== null) {
      // Si la propriété est un objet, explorez récursivement ses attributs
      attributes = attributes.concat(listAttributes(obj[key], prefix + key + '.'));
    } else {
      // Sinon, ajoutez l'attribut à la liste
      attributes.push(prefix + key);
    }
  }
  return attributes;
}

function getNestedValue(obj, path) {
  const keys = path.split('.');
  let value = obj;
  for (const key of keys) {
    if (value && key in value) {
      value = value[key];
    } else {
      return null;
    }
  }
  return value;
}

function formatProperties(props) {
  let result = '';
  for (const path of attributesToShow) {
    const value = getNestedValue(props, path);
    if (value !== null) {
      result += `${path}: ${value}\n`;
    }
  }
  return result;
}

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
        const attributes = listAttributes(props);
        console.log("Attributs disponibles:", attributes);

        originalMaterial = pickedItem.material;  // Stockez le matériau original
        const material = new THREE.MeshBasicMaterial({ color: 0xff0000 });
        pickedItem.material = material;

        // Afficher les informations de l'objet dans un champ textuel
//        material + properties
//        textField.value = JSON.stringify(pickedItem, null, 2) + "\n\nProperties:\n" + JSON.stringify(props, null, 2);
//        textField.value = "Properties:\n" + JSON.stringify(props, null, 2);
  textField.value = "Properties:\n" + formatProperties(props);

        previousSelectedObject = pickedItem;
    } else {
        viewer.IFC.selector.unpickIfcItems();
        viewer.IFC.selector.unHighlightIfcItems();
        textField.value = "Aucun élément sélectionné";
        previousSelectedObject = null;
        originalMaterial = null;
    }
}
