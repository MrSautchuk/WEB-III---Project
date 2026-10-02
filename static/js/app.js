// static/js/app.js — Scripts Estáticos do Hub Central de Marketplaces (Doc ① §11.4)
// Totalmente compatível com CSP estrita (sem inline scripts e sem eval)

document.addEventListener('DOMContentLoaded', function () {
    // Inicialização segura de tooltips do Bootstrap caso existam
    if (typeof bootstrap !== 'undefined' && bootstrap.Tooltip) {
        var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.forEach(function (tooltipTriggerEl) {
            new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }
});
