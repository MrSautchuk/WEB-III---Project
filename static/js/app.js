/* Os códigos foram gerados com auxilio de I.A. */
/*
 * static/js/app.js
 * Scripts estÃ¡ticos do Hub Central de Marketplaces â€” FOKUS
 * CompatÃ­vel com CSP estrita: sem scripts inline e sem eval.
 */

(() => {
    'use strict';

    // -------------------------------------------------------------------------
    // UTILITÃRIO: LEITURA DE COOKIES (CSRF E PREFERÃŠNCIAS)
    // -------------------------------------------------------------------------

    const getCookie = name => {
        let cookieValue = null;

        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');

            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();

                if (cookie.substring(0, name.length + 1) === `${name}=`) {
                    cookieValue = decodeURIComponent(
                        cookie.substring(name.length + 1)
                    );
                    break;
                }
            }
        }

        return cookieValue;
    };

    // -------------------------------------------------------------------------
    // TEMA: PREFERÃŠNCIA DE ILUMINAÃ‡ÃƒO
    // -------------------------------------------------------------------------

    const getStoredTheme = () => {
        const stored = localStorage.getItem('theme');

        if (stored) {
            return stored;
        }

        return getCookie('hub_iluminacao') || null;
    };

    const setStoredTheme = theme => {
        localStorage.setItem('theme', theme);

        document.cookie =
            `hub_iluminacao=${encodeURIComponent(theme)}; ` +
            'path=/; max-age=31536000; samesite=lax';
    };

    const updateThemeIndicators = effectiveTheme => {
        const label = document.getElementById('fokus-theme-label');
        const icon = document.getElementById('fokus-theme-icon');
        if (label) {
            label.textContent = effectiveTheme === 'light' ? 'Tema: Claro' : 'Tema: Escuro';
        }
        if (icon) {
            icon.className = effectiveTheme === 'light'
                ? 'bi bi-sun-fill text-warning'
                : 'bi bi-moon-stars-fill text-info';
        }
    };

    // Aplica o tema na tag <html>.
    const applyTheme = theme => {
        let effectiveTheme = 'dark';
        if (theme === 'auto') {
            const systemDark = window.matchMedia(
                '(prefers-color-scheme: dark)'
            ).matches;
            effectiveTheme = systemDark ? 'dark' : 'light';
        } else if (theme === 'light' || theme === 'dark') {
            effectiveTheme = theme;
        }
        document.documentElement.setAttribute('data-bs-theme', effectiveTheme);
        updateThemeIndicators(effectiveTheme);
    };

    // Atualiza o estado visual dos botÃµes de tema.
    const updateActiveButton = theme => {
        const active = theme || 'light';

        document.querySelectorAll('[data-bs-theme-value]').forEach(button => {
            const isMatch =
                button.getAttribute('data-bs-theme-value') === active;

            button.classList.toggle('active', isMatch);
            button.setAttribute(
                'aria-pressed',
                isMatch ? 'true' : 'false'
            );
        });
    };

    // Salva a preferÃªncia de iluminaÃ§Ã£o no backend.
    const saveIluminacaoToServer = theme => {
        const csrfToken = getCookie('csrftoken');

        if (!csrfToken) {
            return;
        }

        fetch('/tema/alternar/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': csrfToken
            },
            body: new URLSearchParams({
                iluminacao: theme
            })
        }).catch(() => {
            // Falha silenciosa: as preferÃªncias locais continuam disponÃ­veis.
        });
    };

    // Aplica imediatamente o tema jÃ¡ salvo.
    const initialTheme = getStoredTheme();

    if (initialTheme) {
        applyTheme(initialTheme);
    }

    // -------------------------------------------------------------------------
    // SELETORES DE CORES: SINCRONIZAÃ‡ÃƒO ENTRE COLOR E HEX
    // -------------------------------------------------------------------------

    const syncPair = (pickerId, textId) => {
        const picker = document.getElementById(pickerId);
        const text = document.getElementById(textId);

        if (!picker || !text) {
            return;
        }

        const fromPicker = () => {
            text.value = picker.value.toUpperCase();
        };

        const fromText = () => {
            let value = text.value.trim();

            if (
                value &&
                !value.startsWith('#') &&
                /^[0-9A-Fa-f]{6}$/.test(value)
            ) {
                value = `#${value}`;
                text.value = value.toUpperCase();
            }

            if (/^#[0-9A-Fa-f]{6}$/.test(value)) {
                picker.value = value;
            }
        };

        picker.addEventListener('input', fromPicker);
        picker.addEventListener('change', fromPicker);

        text.addEventListener('input', fromText);
        text.addEventListener('change', fromText);
        text.addEventListener('blur', fromText);
    };

    const setupAllPickers = () => {
        syncPair('picker_fundos', 'cor_fundos');
        syncPair('picker_destaques', 'cor_destaques');
        syncPair('picker_escritas', 'cor_escritas');
    };

    // -------------------------------------------------------------------------
    // WHATSAPP: FORMATAÃ‡ÃƒO DO TELEFONE
    // -------------------------------------------------------------------------

    const configurarTelefone = () => {
        const campoTelefone = document.getElementById('telefone');

        if (!campoTelefone) {
            return;
        }

        campoTelefone.addEventListener('input', function () {
            const numero = this.value
                .replace(/\D/g, '')
                .slice(0, 11);

            const ddd = numero.slice(0, 2);
            const restante = numero.slice(2);

            if (numero.length <= 2) {
                this.value = numero.length ? `(${numero}` : '';
            } else if (numero.length <= 6) {
                this.value = `(${ddd}) ${restante}`;
            } else if (numero.length <= 10) {
                this.value =
                    `(${ddd}) ${restante.slice(0, 4)}-${restante.slice(4)}`;
            } else {
                this.value =
                    `(${ddd}) ${restante.slice(0, 5)}-${restante.slice(5)}`;
            }
        });
    };

    // -------------------------------------------------------------------------
    // WHATSAPP: ABERTURA E FECHAMENTO DO WIDGET
    // -------------------------------------------------------------------------

    const configurarWidgetWhatsApp = () => {
        const botaoAbrir = document.getElementById('wppOpen');
        const botaoFechar = document.getElementById('wppClose');
        const janela = document.getElementById('wppToggle');
        const formulario = document.getElementById('wppForm');
        const feedback = document.getElementById('wppFeedback');

        // Se o widget nÃ£o estiver presente nesta pÃ¡gina, nÃ£o faz nada.
        if (
            !botaoAbrir ||
            !botaoFechar ||
            !janela ||
            !formulario ||
            !feedback
        ) {
            return;
        }

        // Garante que a janela comece fechada.
        janela.hidden = true;
        botaoAbrir.setAttribute('aria-expanded', 'false');

        const abrirJanela = () => {
            janela.hidden = false;
            botaoAbrir.setAttribute('aria-expanded', 'true');
            feedback.textContent = '';
        };

        const fecharJanela = () => {
            janela.hidden = true;
            botaoAbrir.setAttribute('aria-expanded', 'false');
            botaoAbrir.focus();
        };

        // Abre ou fecha ao clicar no botÃ£o flutuante.
        botaoAbrir.addEventListener('click', () => {
            if (janela.hidden) {
                abrirJanela();
            } else {
                fecharJanela();
            }
        });

        // Fecha ao clicar no botÃ£o Ã—.
        botaoFechar.addEventListener('click', fecharJanela);

        // Fecha ao pressionar Escape.
        document.addEventListener('keydown', evento => {
            if (evento.key === 'Escape' && !janela.hidden) {
                fecharJanela();
            }
        });

        // ---------------------------------------------------------------------
        // WHATSAPP: VALIDAÃ‡ÃƒO E ENVIO DO FORMULÃRIO
        // ---------------------------------------------------------------------

        formulario.addEventListener('submit', evento => {
            evento.preventDefault();
            feedback.textContent = '';

            // Verifica os campos obrigatÃ³rios e o formato do e-mail.
            if (!formulario.reportValidity()) {
                return;
            }

            const campoNome = document.getElementById('nome');
            const campoEmail = document.getElementById('email');
            const campoTelefone = document.getElementById('telefone');
            const campoEmpresa = document.getElementById('empresa');

            if (!campoNome || !campoEmail || !campoTelefone || !campoEmpresa) {
                feedback.textContent =
                    'NÃ£o foi possÃ­vel localizar todos os campos do formulÃ¡rio.';
                return;
            }

            const nome = campoNome.value.trim();
            const email = campoEmail.value.trim();
            const telefone = campoTelefone.value.trim();
            const empresa = campoEmpresa.value.trim();

            // Valida o celular brasileiro com DDD.
            const digitos = telefone.replace(/\D/g, '');

            if (digitos.length !== 11 || digitos[2] !== '9') {
                feedback.textContent =
                    'Informe um celular vÃ¡lido com DDD. Ex.: (17) 99999-9999.';

                campoTelefone.focus();
                return;
            }

            // IMPORTANTE: substitua pelo nÃºmero real do FOKUS.
            // Use cÃ³digo do paÃ­s + DDD + nÃºmero, sem espaÃ§os ou sÃ­mbolos.
            const numeroComercial = '5517981507301';

            const mensagem = [
                'OlÃ¡! Gostaria de entrar em contato com o FOKUS.',
                '',
                `Nome: ${nome}`,
                `E-mail: ${email}`,
                `Telefone: ${telefone}`,
                `Empresa: ${empresa}`
            ].join('\n');

            const url =
                `https://wa.me/${numeroComercial}?text=${encodeURIComponent(mensagem)}`;

            // Abre a conversa com a mensagem preenchida.
            window.location.href = url;
        });
    };

    // -------------------------------------------------------------------------
    // INICIALIZAÃ‡ÃƒO DOS RECURSOS QUANDO O DOM ESTIVER PRONTO
    // -------------------------------------------------------------------------

    const inicializarAplicacao = () => {
        // FormataÃ§Ã£o do telefone e widget do WhatsApp.
        configurarTelefone();
        configurarWidgetWhatsApp();

        // Tooltips do Bootstrap.
        if (typeof bootstrap !== 'undefined' && bootstrap.Tooltip) {
            const tooltipTriggerList = document.querySelectorAll(
                '[data-bs-toggle="tooltip"]'
            );

            tooltipTriggerList.forEach(elemento => {
                bootstrap.Tooltip.getOrCreateInstance(elemento);
            });
        }

        // BotÃµes de tema.
        const currentTheme = initialTheme || 'dark';
        applyTheme(currentTheme);
        updateActiveButton(currentTheme);

        // Seletores de cores.
        setupAllPickers();

        // Re-sincroniza os seletores quando o modal for aberto.
        const modalEl = document.getElementById('modalTemaPersonalizado');

        if (modalEl) {
            modalEl.addEventListener('show.bs.modal', setupAllPickers);
        }

        // ValidaÃ§Ã£o defensiva do formulÃ¡rio do modal de tema personalizado.
        const formT10 = document.querySelector(
            '#modalTemaPersonalizado form'
        );

        if (formT10) {
            formT10.addEventListener('submit', () => {
                ['fundos', 'destaques', 'escritas'].forEach(tipo => {
                    const picker = document.getElementById(`picker_${tipo}`);
                    const text = document.getElementById(`cor_${tipo}`);

                    if (picker && text) {
                        const value = text.value.trim();

                        if (!value || !/^#[0-9A-Fa-f]{6}$/.test(value)) {
                            text.value = picker.value.toUpperCase();
                        }
                    }
                });
            });
        }
    };

    if (document.readyState === 'loading') {
        document.addEventListener(
            'DOMContentLoaded',
            inicializarAplicacao,
            { once: true }
        );
    } else {
        inicializarAplicacao();
    }

    // -------------------------------------------------------------------------
    // EVENTOS GLOBAIS: TEMA E PALETAS SUGERIDAS
    // -------------------------------------------------------------------------

    document.addEventListener('click', evento => {
        const alvo = evento.target;

        if (!(alvo instanceof Element)) {
            return;
        }

        // AlternÃ¢ncia de tema: Claro, Escuro ou AutomÃ¡tico.
        const openWppBtn = alvo.closest('[data-open-wpp]');

        if (openWppBtn) {
            evento.preventDefault();
            const wppOpenBtn = document.getElementById('wppOpen');
            const wppWindow = document.getElementById('wppToggle');
            if (wppOpenBtn && wppWindow && wppWindow.hidden) {
                wppOpenBtn.click();
            } else if (wppOpenBtn) {
                wppOpenBtn.focus();
            }
            return;
        }

        // Alternar visibilidade da senha na tela de login.
        const togglePassBtn = alvo.closest('[data-toggle-password]');

        if (togglePassBtn) {
            evento.preventDefault();
            const inputId = togglePassBtn.getAttribute('data-toggle-password');
            const passInput = document.getElementById(inputId);
            const icon = togglePassBtn.querySelector('i');
            if (passInput) {
                const isPassword = passInput.type === 'password';
                passInput.type = isPassword ? 'text' : 'password';
                if (icon) {
                    icon.className = isPassword ? 'bi bi-eye' : 'bi bi-eye-slash';
                }
            }
            return;
        }

        // Alternar abertura/fechamento da sidebar no dashboard administrativo.
        const toggleSidebarBtn = alvo.closest('[data-toggle-sidebar]');

        if (toggleSidebarBtn) {
            evento.preventDefault();
            const layout = document.querySelector('.fokus-admin-layout');
            if (layout) {
                if (window.innerWidth <= 991.98) {
                    layout.classList.toggle('sidebar-mobile-open');
                } else {
                    layout.classList.toggle('sidebar-collapsed');
                }
            }
            return;
        }

        // Fechar sidebar no modo mobile/minimizado ao clicar no backdrop ou botÃ£o fechar.
        const closeSidebarBtn = alvo.closest('[data-close-sidebar]');

        if (closeSidebarBtn) {
            evento.preventDefault();
            const layout = document.querySelector('.fokus-admin-layout');
            if (layout) {
                layout.classList.remove('sidebar-mobile-open');
                if (window.innerWidth > 991.98) {
                    layout.classList.add('sidebar-collapsed');
                }
            }
            return;
        }

        // Marcar notificaÃ§Ãµes do sistema como lidas no menu dropdown do sino.
        const clearNotifsBtn = alvo.closest('[data-clear-notifs]');

        if (clearNotifsBtn) {
            evento.preventDefault();
            evento.stopPropagation();
            const dot = document.getElementById('fokusNotifDot');
            if (dot) {
                dot.style.display = 'none';
            }
            document.querySelectorAll('.fokus-notif-item').forEach((item) => {
                item.classList.add('notif-read');
            });
            clearNotifsBtn.textContent = 'Todas lidas';
            return;
        }

        // NavegaÃ§Ã£o SPA suave dentro do painel administrativo (troca de telas sem recarregar a pÃ¡gina).
        const spaLink = alvo.closest('.fokus-admin-layout a[href]');

        if (spaLink && !evento.ctrlKey && !evento.metaKey && !evento.shiftKey && !evento.altKey) {
            const href = spaLink.getAttribute('href') || '';
            const isToggle = spaLink.hasAttribute('data-bs-toggle');
            const isExternal = spaLink.target === '_blank' || href.startsWith('http') || href.startsWith('//');
            const isHash = href === '' || href.startsWith('#') || href.startsWith('javascript:');
            const isBypass = href.startsWith('/admin/') || href.startsWith('/auth/');

            if (!isToggle && !isExternal && !isHash && !isBypass) {
                evento.preventDefault();
                navigateFokusPage(href, true);
                return;
            }
        }

        const themeBtn = alvo.closest('[data-bs-theme-value]');

        if (themeBtn) {
            evento.preventDefault();

            const selected = themeBtn.getAttribute('data-bs-theme-value');

            setStoredTheme(selected);
            applyTheme(selected);
            updateActiveButton(selected);
            saveIluminacaoToServer(selected);

            return;
        }

        // Paletas sugeridas de um clique no modal de personalizaÃ§Ã£o.
        const paletteBtn = alvo.closest('.btn-paleta-rapida');

        if (paletteBtn) {
            evento.preventDefault();

            const fundo = (
                paletteBtn.getAttribute('data-fundo') || ''
            ).toUpperCase();

            const destaque = (
                paletteBtn.getAttribute('data-destaque') || ''
            ).toUpperCase();

            const escrita = (
                paletteBtn.getAttribute('data-escrita') || ''
            ).toUpperCase();

            const pickerFundo = document.getElementById('picker_fundos');
            const textFundo = document.getElementById('cor_fundos');

            const pickerDestaque = document.getElementById('picker_destaques');
            const textDestaque = document.getElementById('cor_destaques');

            const pickerEscrita = document.getElementById('picker_escritas');
            const textEscrita = document.getElementById('cor_escritas');

            if (pickerFundo && textFundo) {
                pickerFundo.value = fundo;
                textFundo.value = fundo;
            }

            if (pickerDestaque && textDestaque) {
                pickerDestaque.value = destaque;
                textDestaque.value = destaque;
            }

            if (pickerEscrita && textEscrita) {
                pickerEscrita.value = escrita;
                textEscrita.value = escrita;
            }

            document.querySelectorAll('.btn-paleta-rapida').forEach(botao => {
                botao.classList.remove(
                    'active',
                    'border-primary',
                    'bg-light',
                    'shadow-sm'
                );
            });

            paletteBtn.classList.add(
                'active',
                'border-primary',
                'bg-light',
                'shadow-sm'
            );
        }
    });

    // -------------------------------------------------------------------------
    // TRANSIÃ‡ÃƒO DE PÃGINAS NO MESMO LUGAR (SPA NAVIGATION NO DASHBOARD)
    // -------------------------------------------------------------------------

    const updateSidebarActiveState = targetUrl => {
        const navContainer = document.getElementById('fokusSidebarNav');
        if (!navContainer) {
            return;
        }
        const path = new URL(targetUrl, window.location.origin).pathname;

        navContainer.querySelectorAll('.fokus-nav-link, .fokus-subnav a').forEach(link => {
            link.classList.remove('active');
        });

        navContainer.querySelectorAll('a[href]').forEach(link => {
            const href = link.getAttribute('href') || '';
            if (!href || href.startsWith('#')) {
                return;
            }
            const linkPath = new URL(href, window.location.origin).pathname;
            const isHome = linkPath === '/dashboard/';
            const matches = isHome
                ? path === '/dashboard/'
                : (path === linkPath || (linkPath !== '/' && path.startsWith(linkPath)));

            if (matches) {
                link.classList.add('active');
                const parentCollapse = link.closest('.collapse');
                if (parentCollapse) {
                    parentCollapse.classList.add('show');
                    const toggleTrigger = navContainer.querySelector(`[href="#${parentCollapse.id}"]`);
                    if (toggleTrigger) {
                        toggleTrigger.classList.add('active');
                    }
                }
            }
        });
    };

    const navigateFokusPage = async (url, pushHistory = true) => {
        const dynamicView = document.getElementById('fokus-dynamic-view');
        if (!dynamicView) {
            window.location.href = url;
            return;
        }

        dynamicView.classList.remove('fokus-view-enter');
        dynamicView.classList.add('fokus-view-loading');

        try {
            const response = await fetch(url, {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                },
                credentials: 'same-origin'
            });

            if (!response.ok) {
                window.location.href = url;
                return;
            }

            const htmlText = await response.text();
            const parser = new DOMParser();
            const doc = parser.parseFromString(htmlText, 'text/html');
            const newView = doc.getElementById('fokus-dynamic-view');

            if (!newView) {
                window.location.href = url;
                return;
            }

            // Atualiza estilos especÃ­ficos da pÃ¡gina (extra_head)
            const currentExtraHead = document.getElementById('fokus-extra-head-slot');
            const newExtraHead = doc.getElementById('fokus-extra-head-slot');
            if (currentExtraHead && newExtraHead) {
                currentExtraHead.innerHTML = newExtraHead.innerHTML;
            }

            // Troca o conteÃºdo principal no mesmo lugar com transiÃ§Ã£o suave
            dynamicView.innerHTML = newView.innerHTML;
            dynamicView.classList.remove('fokus-view-loading');
            void dynamicView.offsetWidth; // Reflow para reiniciar animaÃ§Ã£o
            dynamicView.classList.add('fokus-view-enter');

            if (doc.title) {
                document.title = doc.title;
            }

            const finalUrl = response.url || url;
            if (pushHistory) {
                window.history.pushState({ fokusSpa: true }, doc.title || '', finalUrl);
            }

            updateSidebarActiveState(finalUrl);

            // Fecha a gaveta lateral automaticamente em telas menores apÃ³s clicar
            const layout = document.querySelector('.fokus-admin-layout');
            if (layout && window.innerWidth <= 991.98) {
                layout.classList.remove('sidebar-mobile-open');
            }

            // FunÃ§Ã£o auxiliar para reexecutar scripts inline/externos apÃ³s troca SPA
            const runScriptsInContainer = container => {
                if (!container) {
                    return;
                }
                container.querySelectorAll('script').forEach(oldScript => {
                    const scriptType = (oldScript.getAttribute('type') || '').toLowerCase();
                    if (scriptType === 'application/json') {
                        return;
                    }
                    const newScript = document.createElement('script');
                    Array.from(oldScript.attributes).forEach(attr => {
                        newScript.setAttribute(attr.name, attr.value);
                    });
                    // Se o script registrava DOMContentLoaded, executa imediatamente pois o DOM jÃ¡ carregou
                    let code = oldScript.textContent || '';
                    code = code.replace(
                        /document\.addEventListener\(\s*['"]DOMContentLoaded['"]\s*,\s*/g,
                        '((fn) => { fn(); })('
                    );
                    newScript.textContent = code;
                    oldScript.parentNode.replaceChild(newScript, oldScript);
                });
            };

            // Reexecuta scripts dentro de #fokus-dynamic-view e de #fokus-extra-js-slot
            runScriptsInContainer(dynamicView);

            const currentExtraJs = document.getElementById('fokus-extra-js-slot');
            const newExtraJs = doc.getElementById('fokus-extra-js-slot');
            if (currentExtraJs && newExtraJs) {
                currentExtraJs.innerHTML = newExtraJs.innerHTML;
                runScriptsInContainer(currentExtraJs);
            }

            window.scrollTo({ top: 0, behavior: 'smooth' });
        } catch (err) {
            window.location.href = url;
        }
    };

    // Intercepta formulÃ¡rios GET (filtros e buscas) dentro do painel para transicionar sem recarregar
    document.addEventListener('submit', evento => {
        const form = evento.target;
        if (!(form instanceof HTMLFormElement)) {
            return;
        }
        const insideLayout = form.closest('#fokus-dynamic-view');
        const method = (form.getAttribute('method') || 'get').toLowerCase();
        if (insideLayout && method === 'get') {
            evento.preventDefault();
            const action = form.getAttribute('action') || window.location.pathname;
            const params = new URLSearchParams(new FormData(form)).toString();
            const targetUrl = params ? `${action}?${params}` : action;
            navigateFokusPage(targetUrl, true);
        }
    });

    // Suporte aos botÃµes Voltar / AvanÃ§ar do navegador sem recarregar a pÃ¡gina
    window.addEventListener('popstate', () => {
        if (document.getElementById('fokus-dynamic-view')) {
            navigateFokusPage(window.location.href, false);
        }
    });

    // -------------------------------------------------------------------------
    // TEMA AUTOMÃTICO: ACOMPANHA ALTERAÃ‡Ã•ES DO SISTEMA OPERACIONAL
    // -------------------------------------------------------------------------

    const mediaTemaSistema = window.matchMedia(
        '(prefers-color-scheme: dark)'
    );

    mediaTemaSistema.addEventListener('change', () => {
        const storedTheme = getStoredTheme();

        if (storedTheme === 'auto') {
            applyTheme('auto');
        }
    });

})();
