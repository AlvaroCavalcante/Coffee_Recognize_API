const spawn = require("child_process").spawn;
const fs = require('fs');
const path = require('path');
var nodemailer = require('nodemailer');

const key = process.env.EMAIL_API_KEY;

var files;

const transporter = nodemailer.createTransport({
    host: 'smtp.sendgrid.net',
    port: 587,
    auth: {
        user: 'apikey',
        pass: key
    }
});

exports.uploadGallery = (req, res, next) => {
    if (!req.file) {
        return res.status(500).send({
            error: 'Arquivo não informado'
        })
    } else {
        return res.status(200).send({
            message: 'file arrived!'
        })
    }
};

exports.upload = (req, res, next) => {
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

            console.log(`--------------- SERVIÇO INICIADO ---------------------\n`);

            pythonProcess.stdout.on('data', (data) => {
                console.log(`${data}`);
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

    next();
}

exports.deleteQuantifyFile = (req, res, next) => {
    const directory = 'img_hsv';

    fs.readdir(directory, (err, files) => {
        if (err) throw err;

        for (const file of files) {
            fs.unlink(path.join(directory, file), err => {
                if (err) throw err;
            });
        }
    });
    
    return res.status(201).json({ message: 'sucess'})
}

exports.getImagesPath = (req, res, next) => {
    files = fs.readdirSync('./results');
    return res.status(201).json({ imagens: files });
}

// exports.quantify = (req, res, next) => {
//     processQuantify().then(() => {
//         next();
//     }).catch(error => {
//         return res.status(500).json({ message: error });
//     });
// }

exports.quantify = (req, res, next) => {
    const promise = new Promise((resolve, reject) => {
        try {
            const pythonProcess = spawn('python3', ["scripts/kmeans.py"]);

            console.log(`--------------- SERVIÇO INICIADO ---------------------\n`);

            pythonProcess.stdout.on('data', (data) => {
                var dados = `${data}`
                return res.status(200).json({ message:  dados})
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

exports.moveToDatabase = (req, res, next) => {
    var newPath = '/home/alvaro/Coffee_Recognize_API/database'
    var oldPath = '/home/alvaro/Coffee_Recognize_API/results'

    fileList = fs.readdirSync(oldPath)

    fileList.forEach(file => {
        filePath = oldPath + '/' + file
        newFile = newPath + '/' + file
        fs.rename(filePath, newFile, function (err) {
            if (err) throw err
        })
    });

    return res.status(201).json({ imagens: files });
}

exports.sendEmail = (req, res, next, ) => {
    // const directory = 'results';

    // fs.readdir(directory, (err, files) => {

    //     email_content = `Olá Álvaro tudo bem? <br><br>
    //             Segue abaixo o resultado da analise foliar<br><br>
    //             Atenciosamente,<br>
    //             Álvaro Leandro e Lucas Brito `;

    //     const attach = [];

    //     for (const file of files) {
    //         let content = path.join(directory, file);

    //         email_content += "<img style='display:none' src=" + file + "/><br><br>";

    //         attach.push({
    //             filename: file,
    //             path: './' + content,
    //             cid: file
    //         })
    //     }

    //     var mailOptions = {
    //         from: 'no-reply<geral@nkodontologia.com.br>',
    //         // to: req.body.email,
    //         to: 'leandro0807@live.com',
    //         subject: 'Resultado da análise foliar',
    //         html: email_content,
    //         attachments: attach
    //     };

    //     transporter.sendMail(mailOptions, function (error, info) {
    //         if (error) {
    //             console.log(error);
    //         }
    //     });
    // });

    // return res.status(201).json({
    //     error: null,
    //     response: {
    //         message: 'Relatório enviado',
    //         // email: req.body.email,
    //     }
    // });
    next();    
}
