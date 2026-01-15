import express from 'express';
const router = express.Router();

// use this idea later in a project
router.get('/neopixels', async (req, res) => {
  // const dataPython = (await fetch(`${process.env.API_IP}:${process.env.API_PORT}/`)).json();

  // technicaly I can get last data from database making a request
  const data = {
    robotCode: req.robotCode.toUpperCase(),
    robotName: req.robotName,
    a0: 0,
    a1: 0,
    a2: 0,
    a3: 0,
    a4: 0,
    a5: 0,
    a6: 0,
    a7: 0,
    currentStatus: '00000000'
  }

  // push to reflective sensor array every sensor data
  const reflective_sensor_values = [];
  for (let index = 0; index < 8; index++) {
    reflective_sensor_values.push(data[`a${index}`]);
  }

  // console.log(data.currentStatus[0]);

  const isLayout = req.query.partials == 'true' ? false : 'layouts/layout';

  // console.log(data);
  return res.render('./partials/robot/Neopixels/neopixels', {
    layout: isLayout,
    title: 'Neopixels',
    page: isLayout ? "Neopixels" : "",
    sensors: reflective_sensor_values,
    currentStatus: data.currentStatus,
    data: data
  })
});

export { router };
