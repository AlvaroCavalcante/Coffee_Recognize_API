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
