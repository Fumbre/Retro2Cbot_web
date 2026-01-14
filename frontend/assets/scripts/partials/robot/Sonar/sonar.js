import "./sonar.sass"
import wsBus from '@websocket/wsBus';

let sonarSubscribed = false;

export function wsSonarData() {
  // subscribe only once
  if (sonarSubscribed) return;
  sonarSubscribed = true;

  wsBus.on('sonar', (data) => {
    const dataParsed = JSON.parse(data);
    console.log("ws bus got sonar data", dataParsed);
    updateSonar(dataParsed.data)
  });
}

function updateSonar(data) {
  console.log(data);

  data.map((sonar) => {
    const sonarListEl = document.getElementById(`sonarList__${sonar.robotCode}`);

    if (!sonarListEl)
      return

    const sonarElValue = sonarListEl.querySelector(`[data-sonar-direction="${sonar.direction}"]`);

    sonarElValue.firstElementChild.textContent = sonar.sonarDistance
  })

}
