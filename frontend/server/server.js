const express = require("express");
require("dotenv").config();
const path = require("path");

const app = express();

const PORT = 3000;

// console.log(process.env.DB_USERNAME);



app.use(express.static(path.join(__dirname, "../dist")));

app.listen(PORT, () => {
  console.log(`Server running at http://localhost:${PORT}`);
});
