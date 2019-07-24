const spawn = require("child_process").spawn;
const fs = require('fs');
const path = require('path');

exports.uploadAnexo = (req, res, next) => {
    if (!req.file) {
        return res.status(500).send({
            error: 'Arquivo não informado'
        })
    }
    else {
        next();
    }
};

exports.processImage = (req, res, next) => {
    processRecognition().then(() => {
        next();
    }).catch(error => {
        return res.status(500).json({ message: error });
    });
};

function processRecognition() {
    const promise = new Promise((resolve, reject) => {
        try {
            const pythonProcess = spawn('python3', ["scripts/detection_images.py"]);
            //result.pid = pythonProcess.pid

            console.log(`--------------- SERVIÇO INICIADO ---------------------\n`);

            pythonProcess.stdout.on('data', (data) => {
                console.log(`${data}`);
                // reject();
            });


            pythonProcess.on('close', (code) => {
                console.log(`--------------- SERVIÇO CONCLUÍDO ---------------------\nCÓDIGO: ${code}`);
                resolve();
            });

        } catch (error) {
            console.log(`-------------- ERRO -----------------\n${error}`);
            reject();
        };
    });
    return promise;
}

exports.deleteFiles = (req, res, next) => {
    const directory = 'uploads';
    
    fs.readdir(directory, (err, files) => {
        if (err) throw err;
      
        for (const file of files) {
          fs.unlink(path.join(directory, file), err => {
            if (err) throw err;
          });
        }
      });

    return res.status(201).json({ message: 'success' });
}