export let isOrbiting = false;
let mouseMoved = false;

export function setupPreselection(viewer) {
  let mouseDown = false;
  const container = document.getElementById('three-container');

  window.addEventListener('mousemove', () => {
    if (mouseDown) {
      isOrbiting = true;
      mouseMoved = true; // Définissez ce drapeau si la souris est déplacée
    } else {
      viewer.IFC.selector.prePickIfcItem(); // Gérez la pré-sélection ici
    }
  });

  container.addEventListener('mousedown', () => {
    mouseDown = true;
    mouseMoved = false; // Réinitialisez le drapeau ici
  });

  container.addEventListener('mouseup', () => {
    mouseDown = false;
    isOrbiting = false;
  });

  //Pre-selection color
  const preselectColor = viewer.IFC.selector.defPreselectMat.color;
  preselectColor.r = 0;
  preselectColor.g = 0;
  preselectColor.b = 0.66;

  //Selection color
  const selectColor = viewer.IFC.selector.defSelectMat.color;
  selectColor.r = 0.5;
  selectColor.g = 0.5;
  selectColor.b = 0;

  //Highlight color
  const highlightColor = viewer.IFC.selector.defHighlightMat.color;
  highlightColor.r = selectColor.r;
  highlightColor.g = selectColor.g;
  highlightColor.b = selectColor.b;

  // Color opacity
  viewer.IFC.selector.defHighlightMat.opacity = 0.5;
  //Material opacity
  viewer.IFC.selector.defHighlightMat.transparent = true;

}

export function shouldIgnoreSelection() {
  return mouseMoved;
}
