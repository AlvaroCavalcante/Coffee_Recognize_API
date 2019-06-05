const express = require('express');
const router = express.Router();
const multer = require('multer');
const pictureController = require('../controllers/picture-controller');

const storage = multer.diskStorage({
    destination: function (req, file, cb) {
        cb(null, 'uploads/');
    },
    filename: function (req, file, cb) {
        var ext = file.originalname.substr(file.originalname.lastIndexOf('.') + 1);
        cb(null, file.fieldname + '-' + new Date().toISOString() + '.' + ext);
    }
});

const fileFilter = (req, file, cb) => {
    if (['image/png', 'image/jpeg'].indexOf(file.mimetype) >= 0) {
        cb(null, true)
    } else {
        cb(new Error('Formato do arquivo inválido, permitido apenas jpg ou png'), false)
    }
};
const upload = multer({
    storage: storage,
    fileFilter: fileFilter
  });


router.post('/upload', upload.single('file'), pictureController.uploadAnexo);
router.post('/process', pictureController.processImage);

module.exports = router;