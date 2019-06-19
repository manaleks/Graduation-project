var PATH_TO_STATIC = '../static/images/';

var app = new Vue({
    el: '#app',
    delimiters: ['[[', ']]'],
    data: {
        selectedModelPic: null,
        selectedModel: null,
        models: [],
        error: '',
        result: null,
        isReady: false,
        visiblePrepareBtn: true
    },
    filters: {
    },
    methods: {
        uploadPhoto: function() {
            var file_input = document.getElementById('file');

            file_input.onchange = e => { 
                var file = e.target.files[0];

                if (file) {
                    var reader = new FileReader();
                    $(reader).load(function(e) { 
                        $('#upload-photo').attr('src', e.target.result);
                    });
                    reader.readAsDataURL(file);
                }
            }

            file_input.click();
        },
        changeModel: function() {
            var modelObj = app.models.find(model => { 
                return model.model == app.selectedModel 
            });

            if (modelObj) {
                app.selectedModelPic = PATH_TO_STATIC + modelObj.jpg;
            }
        },
        checkForm: function(event, form) {
            event.preventDefault();
            var formFile = document.getElementById('file').files[0];
            var form = new FormData(document.getElementById('mainform'));
            app.error = '';
            app.visiblePrepareBtn = false;
            app.isReady = false;
            fetch("/", {
                method: "POST",
                body: form
            }).then(function(response) {
                return response.json();
            }).then(function(data) {
                if (data && !data['error']) {
                    fetch('/uploads/' + data['model'] + '/' + data['image_number'] + '/' + data['filename']).then(responce1 => {
                        return responce1.json()
                    }).then(function(data1) {
                        if (data1 && !data1['error']) {
                            app.result = data1['data'];
                            app.isReady = true;
                            app.visiblePrepareBtn = true;
                        } else {
                            app.error = data1['error'];
                            app.visiblePrepareBtn = true;
                        }
                    });

                } else {
                    app.error = data['error'];
                    app.visiblePrepareBtn = true;
                }
            });
        }
    }
});


fetch('/models').then(responce => {
    return responce.json()
}).then(data => {  
    app.models = data;
    var selected = data[0];
    app.selectedModel = selected.model;
    app.selectedModelPic = PATH_TO_STATIC + selected.jpg;
});