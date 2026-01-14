import "./neopixels.sass"
import wsBus from '@websocket/wsBus';

let neopixelsSubscribed = false;

export function wsNeopixelsData() {
  // subscribe only once
  if (neopixelsSubscribed) return;
  neopixelsSubscribed = true;

  wsBus.on('neopixels', (data) => {
    const dataParsed = JSON.parse(data);
    console.log("ws bus got neopixels data", dataParsed);
    updateNeopixels(dataParsed.data)
  });
}

function updateNeopixels(data) {
  console.log(data);

  data.map((neo) => {
    const neopixelsListEl = document.getElementById(`neopixelsList__${neo.robotCode}`);
    console.log(neopixelsListEl);

    if (!neopixelsListEl)
      return

    const pixel = neopixelsListEl.querySelector(`[data-neopixel="${neo.neopixelIndex}"]`);

    pixel.firstElementChild.style.backgroundColor = `rgb(${neo.r},${neo.g},${neo.b})`;
  })


}
