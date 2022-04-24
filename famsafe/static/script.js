window.addEventListener('DOMContentLoaded', event => {
    // Simple-DataTables

    const datatable = document.getElementById('datatable');
    if (datatable) {
        new simpleDatatables.DataTable(datatable);
    }
});
