const express = require('express');
const app = express();
const bodyParser = require('body-parser');
var cors = require('cors')

app.use(cors())

const pictureRoute = require('./routes/picture-route');

app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());

app.use('/picture', pictureRoute);

app.use((error, req, res, next) => {
    res.status(error.status || 500);
    res.json({
      error: error.message
    });
  });

module.exports = app;
