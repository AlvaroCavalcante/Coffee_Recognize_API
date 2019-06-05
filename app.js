const express = require('express');
const app = express();

app.use((error, req, res, next) => {
    res.status(error.status || 500);
    res.json({
      error: error.message
    });
  });
  
module.exports = app;
