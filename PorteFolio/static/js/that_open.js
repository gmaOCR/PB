import { Manager } from '@thatopen/ui';

Manager.init();

import * as BUI from "@thatopen/ui";

const panel = BUI.Component.create<BUI.Panel>(() => {
    let counter = 0;
    const onUpdateBtnClick = () => {
      counter++;
      if (counter >= 5) {
        updateStatefullPanelSection({
          label: "Powered Statefull Panel Section 💪",
          counter,
        });
      } else {
        updateStatefullPanelSection({ counter });
      }
    };
  
    return BUI.html`
      <bim-panel label="My Panel">
        <bim-panel-section label="Update Functions">
          <bim-button @click=${onUpdateBtnClick} label="Update Statefull Section"></bim-button>
        </bim-panel-section>
        ${statelessPanelSection}
        ${statefullPanelSection}
      </bim-panel>
    `;
  });
  
document.body.append(panel);
export { panel };