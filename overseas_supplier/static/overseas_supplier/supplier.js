document_flag = document.getElementById('id_document_flag');
document.getElementById('register-file').addEventListener('click', e => {
    const fileInput = document.getElementById('id_document');
    console.log('ok');
    if (fileInput.files.length > 0) {

        document_flag.checked = true;
    } else {
        document_flag.checked = false;
    }
});
document.getElementById('cancellation-file').addEventListener('click', e => {
    console.log('deswlwct');
    document_flag.checked = false;
});


