// better to use database, but I don't want to make a lot of requests
const VALID_ROBOTS = { 'bb016': "Lady Maria", 'bb046': "Diamond Dog", 'bb011': "Habibi" }

export function validateRobot(req, res, next) {

  const robotId = req.params['id'].toLowerCase();

  if (!VALID_ROBOTS.hasOwnProperty(robotId)) {
    console.error(`There's no robot with id ${robotId}`)
    return res.redirect('/')
  }

  req.robotCode = robotId;
  req.robotName = VALID_ROBOTS[robotId];

  next();
}