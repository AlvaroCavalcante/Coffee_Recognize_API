const spawn = require("child_process").spawn;


exports.uploadAnexo = (req, res, next) => {
    if (!req.file) {
        return res.status(500).send({
            error: 'Arquivo não informado'
        })
    }
    else {
        res.status(201).send({
            message: 'Anexo incluído com sucesso.'
        })
    }
};

exports.processImage = (req, res, next) => {
    try {
        const pythonProcess = spawn('python3', ["scripts/detection_images.py", req.params.id_screening]);
        //result.pid = pythonProcess.pid

        console.log(`--------------- SERVIÇO INICIADO ---------------------\n`);

        pythonProcess.stdout.on('data', (data) => {
            console.log(`${data}`);
        });


        pythonProcess.on('close', (code) => {
            console.log(`--------------- SERVIÇO CONCLUÍDO ---------------------\nCÓDIGO: ${code}`);

        });

    } catch (error) {
        console.log(`-------------- ERRO -----------------\n${error}`);
    }

    return res.status(201).json({
        message: 'sucess',
    });
};