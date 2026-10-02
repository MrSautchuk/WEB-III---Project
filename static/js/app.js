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

        // Configuração do seletor rápido de tema claro/escuro
        updateActiveButton(initialTheme || 'default');

        document.querySelectorAll('[data-bs-theme-value]').forEach(btn => {
            btn.addEventListener('click', () => {
                const selected = btn.getAttribute('data-bs-theme-value');
                setStoredTheme(selected);
                applyTheme(selected);
                updateActiveButton(selected);
            });
        });

        // Sincronização dos seletores de cor do Modal T10
        const setupColorSync = (pickerId, textId) => {
            const picker = document.getElementById(pickerId);
            const text = document.getElementById(textId);
            if (!picker || !text) return;

            picker.addEventListener('input', () => {
                text.value = picker.value.toUpperCase();
            });

            text.addEventListener('input', () => {
                const val = text.value.trim();
                if (/^#[0-9A-Fa-f]{6}$/.test(val)) {
                    picker.value = val.toUpperCase();
                }
            });
        };

        setupColorSync('picker_fundos', 'cor_fundos');
        setupColorSync('picker_destaques', 'cor_destaques');
        setupColorSync('picker_escritas', 'cor_escritas');

        // Paletas Rápidas de 1 Clique no Modal T10
        document.querySelectorAll('.btn-paleta-rapida').forEach(btn => {
            btn.addEventListener('click', () => {
                const f = btn.getAttribute('data-fundo');
                const d = btn.getAttribute('data-destaque');
                const e = btn.getAttribute('data-escrita');

                const pF = document.getElementById('picker_fundos');
                const tF = document.getElementById('cor_fundos');
                const pD = document.getElementById('picker_destaques');
                const tD = document.getElementById('cor_destaques');
                const pE = document.getElementById('picker_escritas');
                const tE = document.getElementById('cor_escritas');

                if (pF && tF) { pF.value = f; tF.value = f; }
                if (pD && tD) { pD.value = d; tD.value = d; }
                if (pE && tE) { pE.value = e; tE.value = e; }
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
