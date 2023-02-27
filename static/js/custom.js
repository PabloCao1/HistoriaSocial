
// se agrrega la clase en filas <tr> de un table para que sean links a la vista de detalle del elemento
$(".clickable-row").click(function() {
    window.location = $(this).data("href");
    });

// desaparecer los Success messages
setTimeout(function () {
$(".alert").alert('close');
}, 3000);