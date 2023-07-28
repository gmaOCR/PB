  document.addEventListener("DOMContentLoaded", function () {
    const mainEntities = document.querySelectorAll(".main-entity");
    let shiftKeyActive = false;

    mainEntities.forEach((dataItem, index) => {
      dataItem.addEventListener("click", (event) => {
        if (shiftKeyActive) {
          const lastSelectedIndex = getLastSelectedIndex();
          if (lastSelectedIndex !== null) {
            selectItemsBetween(mainEntities, lastSelectedIndex, index);
          }
        } else {
          clearSelection(mainEntities);
          dataItem.classList.add("selected");
        }
      });
    });

    document.addEventListener("keydown", (event) => {
      if (event.key === "Shift") {
        shiftKeyActive = true;
      }
    });

    document.addEventListener("keyup", (event) => {
      if (event.key === "Shift") {
        shiftKeyActive = false;
      }
    });

    function clearSelection(items) {
      items.forEach((item) => {
        item.classList.remove("selected");
      });
    }

    function getLastSelectedIndex() {
      const selectedItems = document.querySelectorAll(".data-item.selected");
      if (selectedItems.length === 0) {
        return null;
      }
      return Array.from(mainEntities).indexOf(selectedItems[selectedItems.length - 1]);
    }

    const toggleIcons = document.querySelectorAll(".toggle-icon");

    toggleIcons.forEach((toggleIcon) => {
      const parentEntity = toggleIcon.closest(".entity-container");
      const childTree = parentEntity.querySelector("ul");

      toggleIcon.addEventListener("click", (event) => {
        childTree.classList.toggle("expanded");
        toggleIcon.textContent = childTree.classList.contains("expanded") ? "-" : "+";
        event.stopPropagation();

        // Ajouter la classe "selected" au span lorsque le sous-menu est déployé/réduit
        if (childTree.classList.contains("expanded")) {
          toggleIcon.classList.add("selected");
        } else {
          toggleIcon.classList.remove("selected");
        }
      });
    });
  });