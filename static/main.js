var PATH_TO_STATIC = '../static/images/';

var app = new Vue({
    el: '#app',
    delimiters: ['[[', ']]'],
    data: {
        selectedModelPic: null,
        selectedModel: null,
        models: [],
        result: null,
        isReady: false,
        
        // Start Service
        // visiblePrepareBtn: true,
        // error: ''
        isLoading: false,
        visiblePrepareBtn: false,
        error: 'Sorry, server is not available now. Thank you!'
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
                    app.result = data['data'];
                    app.isReady = true;
                    app.visiblePrepareBtn = true;

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