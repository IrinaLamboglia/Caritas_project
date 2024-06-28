function confirmarCanje(event) {
    console.log("ENTRE");

    event.preventDefault(); 
    if (confirm("¿Estás seguro de que deseas canjear este producto?")) {
        event.target.closest('form').submit(); 
    }
}
