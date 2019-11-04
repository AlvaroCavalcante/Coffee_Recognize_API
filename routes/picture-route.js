const express = require('express');
const router = express.Router();
const multer = require('multer');
const pictureController = require('../controllers/picture-controller');

const storage = multer.diskStorage({
    destination: function (req, file, cb) {
        cb(null, 'uploads/');
    },
    filename: function (req, file, cb) {
        cb(null, file.fieldname + '-' + new Date().toISOString() + '.' + 'jpg');
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

// router.post('/process-and-send-email', pictureController.processImage, pictureController.sendEmail, pictureController.getImagesPath);
router.post('/process-and-send-email', pictureController.processImage, pictureController.getImagesPath, pictureController.moveToDatabase);

router.post('/upload-gallery', upload.single('file'), pictureController.uploadGallery);

router.post('/upload', upload.single('file'), pictureController.uploadAnexo, pictureController.processImage, pictureController.deleteFiles, pictureController.getImagesPath);

module.exports = router;
