import express from 'express';
const router = express.Router();

router.get('/reflective', async (req, res) => {
  // const data = (await fetch(`${process.env.API_IP}:${process.env.API_PORT}/`)).json();
  const data = {
    id: '',
    robotId: 'BB016',
    a0: 174,
    a1: 209,
    a2: 201,
    a3: 204,
    a4: 194,
    a5: 214,
    a6: 214,
    a7: 244,
    currentStatus: '10000000'
  }

  // push to reflective sensor array every sensor data
  const reflective_sensor_values = [];
  for (let index = 0; index < 8; index++) {
    reflective_sensor_values.push(data[`a${index}`]);
  }

  // console.log(data.currentStatus[0]);

  // console.log(data);
  return res.render('./Robot/Sensors/Reflective/reflective', {
    title: 'Reflective Sensor',
    sensors: reflective_sensor_values,
    currentStatus: data.currentStatus,
    data: data
  })
});

export { router };
