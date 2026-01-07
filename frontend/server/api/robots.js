import express from 'express';
const router = express.Router();

router.get('/robots', async (req, res) => {
  const data = await getRobots()
  console.log('this is from api/robots node', data);
  return res.json(data);
})

async function getRobots() {
  try {
    const robots = await (await fetch(`${process.env.API_PROTOCOL}://${process.env.API_URL}/robots`)).json();

    if (robots.code != 200) {
      console.error('Get robots code is not 200')
      return robots
    }

    return robots;
  } catch (e) {
    return e
  }
}


async function getRSData(robotCode) {
  try {
    const robotSensor = await (await fetch(`${process.env.API_PROTOCOL}://${process.env.API_URL}/robots/${robotCode}/rs`)).json();

    if (robotSensor.code != 200) {
      console.error('Get robotSensor code is not 200')
      return robotSensor
    }

    return robotSensor.data;
  } catch (e) {
    return e
  }
}

async function getLastRSData(robotCode) {
  try {
    const robotSensor = await (await fetch(`${process.env.API_PROTOCOL}://${process.env.API_URL}/robots/${robotCode}/rs`)).json();

    if (robotSensor.code != 200) {
      console.error('Get robotSensor code is not 200')
      return robotSensor
    }

    const lastUpdatedSensor = robotSensor.data.length ? robotSensor.data[robotSensor.data.length - 1] : []

    return lastUpdatedSensor;
  } catch (e) {
    return e
  }
}

export { router, getRobots, getRSData, getLastRSData };
