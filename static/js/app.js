// static/js/app.js — Scripts Estáticos do Hub Central de Marketplaces (Doc ① §11.4)
// Totalmente compatível com CSP estrita (sem inline scripts e sem eval)

(() => {
    'use strict';

    const getStoredTheme = () => localStorage.getItem('theme');
    const setStoredTheme = theme => localStorage.setItem('theme', theme);

    const getPreferredTheme = () => {
        const storedTheme = getStoredTheme();
        if (storedTheme) {
            return storedTheme;
        }
        return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    };

    const applyTheme = theme => {
        if (theme === 'auto') {
            document.documentElement.setAttribute('data-bs-theme', (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'));
        } else if (theme === 'default') {
            document.documentElement.removeAttribute('data-bs-theme');
        } else {
            document.documentElement.setAttribute('data-bs-theme', theme);
        }
    };

    const updateActiveButton = theme => {
        const activeTheme = theme || 'default';
        document.querySelectorAll('[data-bs-theme-value]').forEach(button => {
            const isMatch = button.getAttribute('data-bs-theme-value') === activeTheme;
            button.classList.toggle('active', isMatch);
            button.setAttribute('aria-pressed', isMatch ? 'true' : 'false');
            const check = button.querySelector('.check-icon');
            if (check) {
                check.classList.toggle('d-none', !isMatch);
            }
        });
    };

    // Aplicação inicial imediata
    const initialTheme = getStoredTheme();
    if (initialTheme) {
        applyTheme(initialTheme);
    }

    document.addEventListener('DOMContentLoaded', () => {
        // Inicialização de tooltips do Bootstrap
        if (typeof bootstrap !== 'undefined' && bootstrap.Tooltip) {
            const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
            tooltipTriggerList.forEach(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));
        }

        // Configuração do seletor de tema
        updateActiveButton(initialTheme || 'default');

        document.querySelectorAll('[data-bs-theme-value]').forEach(btn => {
            btn.addEventListener('click', () => {
                const selected = btn.getAttribute('data-bs-theme-value');
                setStoredTheme(selected);
                applyTheme(selected);
                updateActiveButton(selected);
            });
        });
    });

    // Reação à mudança de tema do sistema operacional
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', () => {
        const storedTheme = getStoredTheme();
        if (storedTheme === 'auto') {
            applyTheme('auto');
        }
    });
})();
