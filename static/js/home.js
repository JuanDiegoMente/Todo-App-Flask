let contenedor = document.getElementById('contenedor-tareas')

Sortable.create(contenedor, {
    animation: 200, // Le decimos cuanto debe durar la animacion de camnio
    chosenClass: "seleccionando", // Le decimos que haga una clase y luego con CSS aplicamos los estilos
    ghostClass: "ghost",
    dragClass: "arrastrando",

    onEnd: () => {

    },

    group: "lista-items",
});











