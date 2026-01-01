import './robot.sass'
import { createGraphic } from './Sensors/Reflective/reflective.js';

export async function getStatus() {
  const id16 = document.getElementById("robots__status_BB016");
  const id11 = document.getElementById("robots__status_BB011");
  const id46 = document.getElementById("robots__status_BB046");

  console.log('asdfasdfasdf')
  const test = await (await fetch("http://localhost:3000/robot/bb016/sensors/reflective?html=true")).text()
  const test1 = await (await fetch("http://localhost:3000/robot/bb011/sensors/reflective?html=true")).text()
  const test2 = await (await fetch("http://localhost:3000/robot/bb046/sensors/reflective?html=true")).text()

  id16.innerHTML = test;
  id11.innerHTML = test1;
  id46.innerHTML = test2;

  // when fetch robots create graphics (use loop)
  createGraphic('BB016');
  createGraphic('BB046');
  createGraphic('BB011');
}