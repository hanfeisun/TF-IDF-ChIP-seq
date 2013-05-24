/*
 * GET home page.
 */

var fs = require('fs');
var spawn = require('child_process').spawn
var python3 = "/Library/Frameworks/Python.framework/Versions/3.2/bin/python3"
exports.index = function (req, res) {
    res.render('index', { title: 'TF-IDF' });
};

exports.modal_target = function(req, res) {
    res.render('modal-target');
}

exports.uploaded = function (req, res) {
    fs.readFile(req.files.bed_file.path, function (err, data) {
            var newPath = "/Users/ad9075/Desktop/tfidf/new.bed";
            fs.writeFile(newPath, data, function (err) {
                var idf_run = spawn(python3, ["/Users/ad9075/Downloads/Sandbox/tfidf/idf/idf.py", newPath]);
                var idf_result = "";
                idf_run.stdout.on('data', function (data) {
                    idf_result += data;
                })

                idf_run.stderr.on('data', function (data) {
                    console.log('stderr: ' + data);
                });

                idf_run.on('close', function (code) {
                    var result = JSON.parse(idf_result);
                    console.log(result)
                    res.render("result", {title: "finish", result: result});
                    console.log('child process exited with code ' + code);
                });


            })
        }
    )
}


exports.fake_uploaded = function (req, res) {
    var idf_run = spawn(python3, ["/Users/ad9075/Downloads/Sandbox/tfidf/idf/idf.py", "/Users/ad9075/Downloads/Sandbox/tfidf/idf/Data/Juan_H3K27me3/4250_summits.bed"]);
    var idf_result = "";
    idf_run.stdout.on('data', function (data) {
        idf_result += data;
    })

    idf_run.stderr.on('data', function (data) {
        console.log('stderr: ' + data);
    });

    idf_run.on('close', function (code) {
        var result = JSON.parse(idf_result);
        console.log(result)
        res.render("result", {title: "finish", result: result});
        console.log('child process exited with code ' + code);
    })

}