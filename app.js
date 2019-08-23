const express = require('express');
const app = express();
var cors = require('cors')

app.use(cors())

const pictureRoute = require('./routes/picture-route');

app.use(express.urlencoded({
  limit: '50mb',
  parameterLimit: 100000,
  extended: false 
}));

app.use(express.json({
  limit: '50mb'
}));

app.use('/picture', pictureRoute);

app.use('/resultados', express.static('resultados/'));

app.use((error, req, res, next) => {
    res.status(error.status || 500);
    res.json({
      error: error.message
    });
  });

module.exports = app;
