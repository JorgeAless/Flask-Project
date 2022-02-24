const btnDelete = document.querySelectorAll('.btn-delete')
const btnGuardar = document.querySelectorAll('.btn-primary')


if(btnDelete){
    const btnArray = Array.from(btnDelete);
    btnArray.forEach((btn) => {
        btn.addEventListener('click', (e) => {
            console.log('Click en el boton');
            if(!confirm('¿Estas seguro de querer eliminar el registro?')){
                e.preventDefault();
            }
        });
    });
}

/*if(btnGuardar){
    const btnArrayG = Array.from(btnGuardar);
    btnArrayG.forEach((btn) => {
        btn.addEventListener('click', (e) => {
            if(!confirm('Se actualizaran los datos ¿Deseas continuar?')){
                e.preventDefault();
            }
        });
    });
}*/
function alerta(){
    swal({
        title: '¿Estas seguro?',
        text: "Registrar nueva escuela",
        type: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Registrar',
        cancelButtonText: 'Cancelar'
      }).then((result) => {
        if (result.value) {
          swal(
            'Registro',
            'El registro la escuela correctamente.',
            'success'
          )
        }
      })
}