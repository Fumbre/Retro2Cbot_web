require("dotenv").config();
const express = require("express");
const path = require("path");

const app = express();

const PORT = process.env.PORT || 3000;

// console.log(process.env.DB_USERNAME);

app.get('/robot', async (req, res) => {
  const robots = await (await fetch('http://localhost:8080/robots')).json();
  console.log(robots);
  return res.json(robots)
})

app.get('/robot/status/:id', async (req, res) => {
  try {
    let robots = await (await fetch('http://localhost:8080/robots')).json();

    const test = robots.data.filter((item) => item.robotCode.toLowerCase() == req.params.id.toLowerCase())[0]
    console.log(test)
    return res.json(test)
  } catch (e) {
    return res.redirect('/')
  }

})


app.use(express.static(path.join(__dirname, "../dist")));

app.listen(PORT, () => {
  console.log(`Server running at http://localhost:${PORT}`);
});

