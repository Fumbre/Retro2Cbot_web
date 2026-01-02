import express from 'express';
const router = express.Router();

router.get('/robots', async (req, res) => {
  const data = await getRobots()
  console.log('this is from api/robots node', data);
  return res.json(data);
})

async function getRobots() {
  try {
    const robots = await (await fetch(`http://${process.env.API_IP}:${process.env.API_PORT}/robots`)).json();

    if (robots.code != 200) {
      console.error('Get robots code is not 200')
      return robots
    }

    return robots;
  } catch (e) {
    return e
  }
}

export { router, getRobots };
