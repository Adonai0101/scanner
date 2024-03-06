

const CLOUDINARY_URL = `https://api.cloudinary.com/v1_1/adonai0101/image/upload`
const CLOUDINARY_UPLOAD_PRESET = 'xn5pdxm9';


var data = {
    'foto': '',
    'fotoKey': ''
}


// Obtenemos los elementos de la imagen y el input
const imagenCargar = document.getElementById('imagen-cargar');
const inputCargar = document.getElementById('input-cargar');

// Agregamos un evento clic a la imagen
imagenCargar.addEventListener('click', function () {
    // Simulamos un clic en el input oculto
    inputCargar.click();
});

// Agregamos un evento change al input para manejar el archivo seleccionado
inputCargar.addEventListener('change', function () {
    
    //funcion para mostrar pantalla de carga
    pantallaCarga()
    
    const file = inputCargar.files[0];
    console.log(file)

    const formData = new FormData();
    formData.append("file", inputCargar.files[0]);

    // Subir la imagen
    fetch("/fileserver/upload", {
        method: "POST",
        body: formData
    })
        .then(response => response.json())
        .then(data => {
            // Puedes recargar la lista de imágenes después de una subida exitosa
            console.log(data)
            update(data)
        })
        .catch(error => console.error(error))
});



function update(data) {
    const url = '/cuenta//updatefoto'
    axios.post(url, data)
        .then(response => {
            // La solicitud fue exitosa, aquí puedes manejar la respuesta del servidor
            console.log('Respuesta del servidor:', response.data);
            location.reload();
        })
        .catch(error => {
            // Hubo un error en la solicitud, aquí puedes manejar el error
            console.error('Error al enviar la solicitud:', error);
        });
}


//Subiendo el archivo a cloudinary
/* codigo fuera de uso actualmente

function upload_cloudinary(file) {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('upload_preset', CLOUDINARY_UPLOAD_PRESET);

    return axios({
        method: "post",
        url: CLOUDINARY_URL,
        data: formData,
        headers: { "Content-Type": "multipart/form-data" },
    })
        .then(function (response) {
            console.log(response)
            data.foto = response.data.secure_url
            data.fotoKey = response.data.public_id

            update(data)

        })
        .catch(function (response) {
            //handle error
            console.log(response);
        });

}

*/