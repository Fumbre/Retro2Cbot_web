import dotenv from 'dotenv';
dotenv.config();
import express from 'express'
import expressLayouts from 'express-ejs-layouts'
import path from 'node:path'
import { fileURLToPath } from 'url';
import fs from 'fs/promises';
import http from 'http';
import { connectToRobotApi } from "./ws/wsClient.js"
import { initWSS } from "./ws/wsServer.js"

import { validateRobot } from './middleware/validateRobot.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const manifestPath = path.join(__dirname, '..', 'dist', 'manifest.json');

// style and script json read
const data = await fs.readFile(manifestPath, 'utf-8');
const manifest = JSON.parse(data);


//api
const robotRouter = (await import('./routes/robot/robots.js')).router;
const reflectiveRouter = (await import('./routes/robot/sensors/reflective.js')).router;
const apiRobots = (await import('./api/robots.js')).router;


// console.log(process.env.DB_USERNAME);
const PORT = process.env.PORT || 3000;
const app = express();

// http server for websocket
const server = http.createServer(app);

// static files
app.locals.assets = manifest; // path to css and js
app.use(express.static(path.join(__dirname, "../dist")));

// view engine ejs
app.set('view engine', 'ejs');

// middleware for engine layout
app.use(expressLayouts);
app.set('layout', 'layouts/layout');


app.get('/', (req, res) => {
  res.render('index', {
    title: "Retro2Cbot",
    page: 'index',
  });
});

// use api
app.use('/', robotRouter);
app.use('/robot/:id/sensors', validateRobot, reflectiveRouter);

// get robots
app.use('/api/', apiRobots);

// webSocket connection
// connectToRobotApi(); // try with arduino without it
initWSS(server)

server.listen(PORT, () => {
  console.log(`Server running at http://localhost:${PORT}`);
});