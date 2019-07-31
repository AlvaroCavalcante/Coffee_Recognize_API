const spawn = require("child_process").spawn;
const fs = require('fs');
const path = require('path');
var nodemailer = require('nodemailer');

const key = process.env.EMAIL_API_KEY;

const transporter = nodemailer.createTransport({
    host: 'smtp.sendgrid.net',
    port: 587,
    auth: {
        user: 'apikey',
        pass: key
    }
});

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

    next();
}

exports.getImagesPath = (req, res, next) => {
    var files = fs.readdirSync('./resultados');

    return res.status(201).json({ imagens: files });
}

exports.sendEmail = (req, res, next, ) => {   
    var files = fs.readdirSync('./resultados');
    const directory = 'resultados';

    email_content = `Olá Álvaro tudo bem? <br><br>
                Segue abaixo o resultado da analise foliar<br><br>
                Atenciosamente,<br>
                Álvaro Leandro e Lucas Brito `;

    const attach = [];

    //Embedded image: <img src="cid:imagem primeira"/><br><br>

    fs.readdir(directory, (err, files) => {
        if (err) throw err;
        let count = 0;
        const html = [];

        for (const file of files) {
            let content = path.join(directory, file);
            let name = 'image' + count + 'jpg';
            html.push("Embedded image: <img src="+ name + "/><br><br>")

            attach.push({
                filename: name,
                content: content,
                cid: 'cid:logo'
            })
            count ++;
        }
        console.log(html);

    });

    var mailOptions = {
        from: 'no-reply<geral@nkodontologia.com.br>',
        to: req.body.email,
        subject: 'Resultado da análise foliar',
        html: email_content,
        attachments: [{ 
            filename: 'image.jpg',
            content: fs.createReadStream('./resultados/resultado0.png'),
            cid: 'cid:imagem primeira'
        },{
        filename: 'image2.jpg',
        content: fs.createReadStream('./resultados/resultado1.png'),
        cid: 'cid:imagem segunda'
        }]
    };

    transporter.sendMail(mailOptions, function (error, info) {
        if (error) {
            console.log(error);
        }
    });

    return res.status(201).json({
        error: null,
        response: {
            message: 'Relatório enviado',
            email: req.body.email,
        }
    });
}
