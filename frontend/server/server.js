import dotenv from 'dotenv';
dotenv.config();
import express from 'express'
import expressLayouts from 'express-ejs-layouts'
import path from 'node:path'
import { fileURLToPath } from 'url';
import fs from 'fs/promises';

import { connectToRobotApi } from "./webSocket/wsClient.js"

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const manifestPath = path.join(__dirname, '..', 'dist', 'manifest.json');

// style and script

const data = await fs.readFile(manifestPath, 'utf-8');
const manifest = JSON.parse(data);


//api
const reflectiveRouter = (await import('./api/sensors/reflective.js')).router;
const robotRouter = (await import('./routes/robot/robot.js')).router;

// console.log(process.env.DB_USERNAME);
const PORT = process.env.PORT || 3000;
const app = express();
app.locals.assets = manifest;

// static files
app.use(express.static(path.join(__dirname, "../dist")));

// view engine ejs
app.set('view engine', 'ejs');

// middleware for engine layout
app.use(expressLayouts);
app.set('layout', 'layout');


app.get('/', (req, res) => {
  res.render('index', {
    title: "Retro2Cbot"
  });
});

// use api
app.use('/', robotRouter);
app.use('/sensors', reflectiveRouter);

// const WebSocket = require('ws');
// const ws = new WebSocket('wss://${process.env.API_IP}:${process.env.API_PORT}/rs');

// webSocket connection
connectToRobotApi();

app.listen(PORT, () => {
  console.log(`Server running at http://localhost:${PORT}`);
});