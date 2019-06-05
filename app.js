const express = require('express');
const app = express();

const pictureRoute = require('./routes/picture-route');

app.use('/picture', pictureRoute);

app.use((error, req, res, next) => {
    res.status(error.status || 500);
    res.json({
      error: error.message
    });
  });

module.exports = app;
