     var documents = {{ scanned_documents | safe }};
        var noOfDocuments = documents.length;
        var document_barcodes  = {{ digital_documents | safe }};
        var document_types = {{ document_type | safe }};
        var doctypes = [];

        for(let i = 0; i < document_types.length; i++){
            let value = i;
            let label = document_types[i].document_name;
            let dict = {'value':value, 'label':label};
            doctypes.push(dict)
        }
        var document_type = '';
        var document = '';

        {#jquery code#}
         $(function(){
         let count = 0;
         let uri = "http://127.0.0.1:9000/media/" + documents[count].filepond + "#toolbar=0";
         let url = encodeURI(uri);

        $('#pdf').append("<embed id='pdf' src=" + url +"  width= '100%' height= '800'>");


         $('#states').append("<div class='progress'>\n" +
        "  <div class='progress-bar progress-bar-striped' role='progressbar' style='width:30%' aria-valuenow='10' aria-valuemin='0' aria-valuemax='100'></div>\n" +
        "</div>\n");

        $('#barcode').popSelectOptions({
            'options':document_barcodes
        });
        $('#barcode').change(function(){
            document_id = $('#barcode option:selected').val();
            console.log(document_id)
        });
        $('#documenttype').popSelectOptions({
            'options': doctypes
        });
        $('#documenttype').change(function(){
            document_type = $('#barcode option:selected').val()
        });


        $('#clicky').click(function(){
            count = count + 1;
             let uri = "http://127.0.0.1:9000/media/" + documents[count].filepond + "#toolbar=0";
             let url = encodeURI(uri);
            $('#pdf').empty();
            $('#pdf').append("<embed id='pdf' src= "+ url +" width= '100%' height= '800'>")
        });


        $('#updatedoc').click(function(){
            let document_id = $('#barcode option:selected').val();
            console.log(document_id);
            let data = {
                document_path: documents[count].filepond,
                document_type: $('#documenttype option:selected').text()
            };
            let urlMask = "{% url 'update_document_file_detail' 87 %}".replace(/87/, document_id.toString());
            console.log(urlMask);
           $.ajax({
              type: "POST",
              url: urlMask,
              data: data,
              success: console.log('received a result'),
              dataType: 'json'
            });
        })
    })