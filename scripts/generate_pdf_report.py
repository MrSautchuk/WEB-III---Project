# Os códigos foram gerados com auxilio de I.A.
import subprocess
import os

HTML_CONTENT = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<title>Relatório de Conformidade - Template Web III</title>
<style>
  @page {
    size: A4;
    margin: 15mm 15mm 15mm 15mm;
  }
  * {
    box-sizing: border-box;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }
  body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    color: #1e293b;
    line-height: 1.55;
    font-size: 10pt;
    margin: 0;
    padding: 0;
    background: #ffffff;
  }
  .header-card {
    border-left: 5px solid #2563eb;
    background: #f8fafc;
    padding: 16px 20px;
    border-radius: 4px;
    margin-bottom: 20px;
  }
  .header-card h1 {
    font-size: 17pt;
    margin: 0 0 6px 0;
    color: #0f172a;
    font-weight: 700;
  }
  .header-card .meta {
    font-size: 9pt;
    color: #64748b;
    display: flex;
    flex-wrap: wrap;
    gap: 16px;
    margin-top: 6px;
  }
  .meta-item strong {
    color: #334155;
  }
  h2 {
    font-size: 13pt;
    color: #0f172a;
    border-bottom: 2px solid #e2e8f0;
    padding-bottom: 6px;
    margin-top: 24px;
    margin-bottom: 12px;
    page-break-after: avoid;
    display: flex;
    align-items: center;
    gap: 8px;
  }
  h3 {
    font-size: 11pt;
    color: #1e293b;
    margin-top: 14px;
    margin-bottom: 6px;
    page-break-after: avoid;
  }
  p {
    margin: 0 0 10px 0;
  }
  .badge {
    display: inline-block;
    padding: 3px 8px;
    font-size: 8pt;
    font-weight: 600;
    border-radius: 9999px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }
  .badge-success {
    background-color: #dcfce7;
    color: #15803d;
    border: 1px solid #bbf7d0;
  }
  .badge-danger {
    background-color: #fee2e2;
    color: #b91c1c;
    border: 1px solid #fecaca;
  }
  .badge-info {
    background-color: #e0f2fe;
    color: #0369a1;
    border: 1px solid #bae6fd;
  }
  .card-item {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 6px;
    padding: 12px 14px;
    margin-bottom: 10px;
    page-break-inside: avoid;
  }
  .card-item.conforme {
    border-left: 4px solid #10b981;
  }
  .card-item.pendente {
    border-left: 4px solid #ef4444;
    background: #fffbfb;
  }
  .card-title {
    font-weight: 700;
    font-size: 10.5pt;
    color: #0f172a;
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 6px;
  }
  .card-desc {
    font-size: 9.5pt;
    color: #334155;
    margin: 0;
  }
  .card-desc strong {
    color: #0f172a;
  }
  .card-desc ul {
    margin: 6px 0 0 0;
    padding-left: 20px;
  }
  .card-desc li {
    margin-bottom: 3px;
  }
  table {
    width: 100%;
    border-collapse: collapse;
    margin: 14px 0;
    font-size: 9pt;
    page-break-inside: avoid;
  }
  th, td {
    padding: 8px 10px;
    border: 1px solid #e2e8f0;
    text-align: left;
  }
  th {
    background-color: #f1f5f9;
    color: #1e293b;
    font-weight: 600;
  }
  tr:nth-child(even) td {
    background-color: #f8fafc;
  }
  .summary-box {
    background: #eff6ff;
    border: 1px solid #bfdbfe;
    padding: 12px 16px;
    border-radius: 6px;
    margin-bottom: 18px;
    font-size: 9.5pt;
    color: #1e3a8a;
  }
  .roadmap-box {
    background: #f8fafc;
    border: 1px solid #cbd5e1;
    border-radius: 6px;
    padding: 14px;
    margin-top: 14px;
    page-break-inside: avoid;
  }
  .roadmap-step {
    margin-bottom: 10px;
    padding-left: 12px;
    border-left: 2px solid #3b82f6;
  }
  .roadmap-step:last-child {
    margin-bottom: 0;
  }
  .roadmap-step h4 {
    margin: 0 0 4px 0;
    font-size: 10pt;
    color: #1e40af;
  }
  .roadmap-step p {
    margin: 0;
    font-size: 9pt;
    color: #475569;
  }
  .page-break {
    page-break-before: always;
  }
  .footer-note {
    font-size: 8pt;
    color: #94a3b8;
    text-align: center;
    margin-top: 25px;
    padding-top: 8px;
    border-top: 1px solid #e2e8f0;
  }
</style>
</head>
<body>

<div class="header-card">
  <h1>Relatório de Conformidade & Gap Analysis</h1>
  <div style="font-size: 11pt; font-weight: 600; color: #1e40af; margin-top: 2px;">
    Comparativo do Hub Central vs. Repositório Template Oficial de Web III
  </div>
  <div class="meta">
    <div class="meta-item"><strong>Instituição:</strong> FATEC Olímpia — CST DSM</div>
    <div class="meta-item"><strong>Disciplina:</strong> Desenvolvimento Web III (2026/2)</div>
    <div class="meta-item"><strong>Template Base:</strong> <code>web3-fatec-olimpia-2026-2/template-projeto</code></div>
    <div class="meta-item"><strong>Data:</strong> 25/10/2026</div>
  </div>
</div>

<div class="summary-box">
  <strong>Visão Executiva:</strong> O nosso projeto já atingiu um nível de excelência muito acima da média acadêmica em arquitetura de backend, isolamento multi-tenant, segurança criptográfica e testes (213 testes 100% verdes). No entanto, o repositório base da disciplina impõe <strong>artefatos obrigatórios de governança</strong>, <strong>CI/CD no GitHub</strong>, <strong>dependências curriculares (DRF, NoSQL, Pytest, Ruff)</strong> e <strong>formato estrito de README</strong> que ainda precisam ser incorporados para a entrega oficial.
</div>

<h2><span class="badge badge-success">1ª LISTA</span> O que está CONFORME (ou supera) o Template</h2>

<div class="card-item conforme">
  <div class="card-title">
    <span>1. Arquitetura Modular Django e Bounded Contexts</span>
    <span class="badge badge-success">Supera</span>
  </div>
  <div class="card-desc">
    O projeto está estruturado em apps independentes sob <code>apps/</code> (<code>accounts</code>, <code>anuncios</code>, <code>catalogo</code>, <code>core</code>, <code>financeiro</code>, <code>marketplaces</code>, <code>pedidos</code>, <code>site</code>, <code>tenancy</code>), com domínio modelado e desacoplado, superando amplamente o monólito tradicional.
  </div>
</div>

<div class="card-item conforme">
  <div class="card-title">
    <span>2. Isolamento Multi-Tenant e Matriz RBAC Completa</span>
    <span class="badge badge-success">Supera</span>
  </div>
  <div class="card-desc">
    Isolamento total de banco por Loja (tenant), com hierarquia estrita de 4 perfis (<code>DEV</code>, <code>ADMIN</code>, <code>SUPERVISOR</code>, <code>USUARIO</code>), consultas blindadas por tenant e testes validando bloqueio com <code>403 Forbidden</code> para perfis não autorizados.
  </div>
</div>

<div class="card-item conforme">
  <div class="card-title">
    <span>3. Segurança Defensiva, Criptografia e Webhooks Blindados</span>
    <span class="badge badge-success">Supera</span>
  </div>
  <div class="card-desc">
    Tokens OAuth protegidos com criptografia Fernet em repouso no banco; webhook do Mercado Livre blindado com validação de assinatura criptográfica HMAC, proteção anti-replay, chaves por UUID e proteção contra IDOR/BOLA.
  </div>
</div>

<div class="card-item conforme">
  <div class="card-title">
    <span>4. Volume e Cobertura de Testes Automatizados</span>
    <span class="badge badge-success">Conforme</span>
  </div>
  <div class="card-desc">
    Suíte com <strong>213 testes automatizados</strong> passando com <strong>100% de sucesso</strong>, cobrindo testes unitários, testes de integração, controle de concorrência com locks pessimistas (<code>select_for_update</code>), resiliência de webhooks e isolamento multi-tenant.
  </div>
</div>

<div class="card-item conforme">
  <div class="card-title">
    <span>5. Caderno de Decisões Técnicas (ADRs Fundamentadas)</span>
    <span class="badge badge-success">Supera</span>
  </div>
  <div class="card-desc">
    Possuímos <strong>14 ADRs</strong> completas em <code>docs/design/</code> documentando escolhas arquiteturais, padrões GoF (Strategy, Observer, State), concorrência e governança, atendendo ao mais alto padrão de engenharia.
  </div>
</div>

<div class="card-item conforme">
  <div class="card-title">
    <span>6. Convenção de Commits e Rastreabilidade Git</span>
    <span class="badge badge-success">Conforme</span>
  </div>
  <div class="card-desc">
    O histórico do Git adota estritamente o padrão <strong>Conventional Commits</strong> (<code>feat</code>, <code>fix</code>, <code>chore</code>, <code>docs</code>, <code>test</code>, <code>refactor</code>), exatamente como exigido no guia de contribuição do template.
  </div>
</div>

<div class="card-item conforme">
  <div class="card-title">
    <span>7. Governança e Atribuição de I.A.</span>
    <span class="badge badge-success">Conforme</span>
  </div>
  <div class="card-desc">
    100% dos 162 arquivos do repositório contam com cabeçalho padronizado de atribuição de I.A., validado por script automatizado em conformidade com o contrato pedagógico da disciplina.
  </div>
</div>

<div class="card-item conforme">
  <div class="card-title">
    <span>8. Laboratório de Simulação e Mocks</span>
    <span class="badge badge-success">Supera</span>
  </div>
  <div class="card-desc">
    Módulo exclusivo <code>apps.mockar_dados</code> e feature flags que viabilizam demonstração completa de fluxos e webhooks sem dependência de credenciais externas em ambiente acadêmico.
  </div>
</div>

<div class="page-break"></div>

<h2><span class="badge badge-danger">2ª LISTA</span> O que NÃO ESTÁ CONFORME e Falta Implementar</h2>

<div class="card-item pendente">
  <div class="card-title">
    <span>1. Arquivos de Governança e Comunidade na Raiz</span>
    <span class="badge badge-danger">Ausente</span>
  </div>
  <div class="card-desc">
    O template exige três arquivos contratuais na raiz do repositório que atualmente não existem:
    <ul>
      <li><strong><code>CONTRIBUTING.md</code>:</strong> Guia de contribuição da equipe, definição do fluxo Git, regras de PR (1 aprovação obrigatória, CI verde, squash and merge), padrões de código (Ruff), papéis Scrum rotativos a cada sprint (PO, Scrum Master, Dev Team) e a Definition of Done.</li>
      <li><strong><code>SECURITY.md</code>:</strong> Política de segurança oficial da disciplina (procedimento para notificação ao professor e fluxo de emergência em caso de commit acidental de segredos).</li>
      <li><strong><code>LICENSE</code>:</strong> Arquivo de licença MIT com o nome do grupo e a identificação da FATEC Olímpia.</li>
    </ul>
  </div>
</div>

<div class="card-item pendente">
  <div class="card-title">
    <span>2. Automação de CI/CD e Segurança no GitHub (.github/)</span>
    <span class="badge badge-danger">Ausente</span>
  </div>
  <div class="card-desc">
    O diretório <code>.github/</code> está ausente e é avaliado pelo professor via GitHub Actions:
    <ul>
      <li><strong><code>.github/workflows/ci.yml</code>:</strong> Workflow de CI que executa a cada push/PR, roda o linter <strong>Ruff</strong>, executa os testes via <strong>Pytest</strong>, barra merges com cobertura inferior a <strong>40%</strong> e audita vulnerabilidades com <strong>pip-audit</strong>.</li>
      <li><strong><code>.github/workflows/secret-scan.yml</code>:</strong> Action com <strong>Gitleaks</strong> para detecção automática de credenciais ou chaves privadas vazadas no histórico.</li>
      <li><strong><code>.github/dependabot.yml</code>:</strong> Configuração semanal para abertura automática de PRs de correção de dependências vulneráveis.</li>
    </ul>
  </div>
</div>

<div class="card-item pendente">
  <div class="card-title">
    <span>3. README.md Acadêmico Oficial</span>
    <span class="badge badge-danger">Desatualizado</span>
  </div>
  <div class="card-desc">
    O nosso <code>README.md</code> tem apenas 3 linhas. O template exige a estrutura acadêmica completa:
    <ul>
      <li>Identificação formal: Grupo XX, Docente, FATEC Olímpia - CST DSM.</li>
      <li>Seção "Sobre o Projeto": Problema que resolve, Público-alvo e Organização parceira.</li>
      <li>Tabela da Equipe com nome completo, papel Scrum e link de GitHub de cada integrante.</li>
      <li>Instruções canônicas de execução local e comandos de teste com pytest.</li>
      <li>Quadro de Sprints (1 a 4) com status e links diretos para as User Stories no <strong>Taiga</strong>.</li>
      <li>Seção de entregas finais: URL em produção, Swagger (/api/docs/) e link do vídeo demo de 5 min.</li>
    </ul>
  </div>
</div>

<div class="card-item pendente">
  <div class="card-title">
    <span>4. Estrutura Canônica de Documentação em docs/</span>
    <span class="badge badge-danger">Incompleto</span>
  </div>
  <div class="card-desc">
    O README do template aponta para 4 arquivos canônicos que devem existir em <code>docs/</code>:
    <ul>
      <li><strong><code>docs/arquitetura.md</code>:</strong> Visão geral da arquitetura, C4 e topologia.</li>
      <li><strong><code>docs/requisitos.md</code>:</strong> Compilação de User Stories e Requisitos Funcionais.</li>
      <li><strong><code>docs/decisoes.md</code>:</strong> Documento-índice estruturado ligando e resumindo as nossas 14 ADRs.</li>
      <li><strong><code>docs/manual-usuario.md</code>:</strong> Passo a passo explicativo para o avaliador operar o sistema.</li>
    </ul>
  </div>
</div>

<div class="card-item pendente">
  <div class="card-title">
    <span>5. Dependências Curriculares do requirements.txt</span>
    <span class="badge badge-danger">Pendente</span>
  </div>
  <div class="card-desc">
    Nosso <code>requirements.txt</code> precisa incorporar os pacotes exigidos pelas aulas da disciplina:
    <ul>
      <li><strong>DRF e OpenAPI (Sprint 3):</strong> <code>djangorestframework</code>, <code>djangorestframework-simplejwt</code>, <code>drf-spectacular</code>, <code>django-cors-headers</code>, <code>django-filter</code>.</li>
      <li><strong>NoSQL (Sprint 2):</strong> <code>pymongo</code> (integração com MongoDB Atlas requerida na grade).</li>
      <li><strong>Deploy / Servidor Web:</strong> <code>gunicorn</code>, <code>whitenoise</code>, <code>psycopg2-binary</code>.</li>
      <li><strong>Testes e Qualidade:</strong> <code>pytest</code>, <code>pytest-django</code>, <code>pytest-cov</code>, <code>factory-boy</code>, <code>faker</code>, <code>ruff</code>.</li>
    </ul>
  </div>
</div>

<div class="card-item pendente">
  <div class="card-title">
    <span>6. Runner Pytest e Trava de Cobertura de Código</span>
    <span class="badge badge-danger">Pendente</span>
  </div>
  <div class="card-desc">
    Atualmente rodamos os testes via <code>python manage.py test</code>. Precisamos criar o arquivo de configuração <strong><code>pytest.ini</code></strong> para que o comando <code>pytest --cov=. --cov-report=xml</code> execute os 213 testes no Django e gere o relatório exigido pelo CI do GitHub Actions com cobertura superior a 40%.
  </div>
</div>

<div class="card-item pendente">
  <div class="card-title">
    <span>7. Alinhamento de .env.example e Expansão do .gitignore</span>
    <span class="badge badge-danger">Parcial</span>
  </div>
  <div class="card-desc">
    O <code>.env.example</code> precisa incluir as chaves padrão da disciplina (<code>DATABASE_URL</code>, <code>MONGODB_URI</code>, JWT e SMTP), e o <code>.gitignore</code> precisa ser ampliado para ignorar caches de testes (<code>.pytest_cache/</code>, <code>htmlcov/</code>, <code>.coverage</code>, <code>.ruff_cache/</code>), arquivos estáticos de produção e metadados de SO.
  </div>
</div>

<div class="roadmap-box">
  <h3 style="margin: 0 0 8px 0; color: #0f172a; font-size: 11pt;">🎯 Plano de Ação Recomendado para o Grupo</h3>
  <div class="roadmap-step">
    <h4>Fase 1: Governança e Repositório (Imediato)</h4>
    <p>Adicionar <code>CONTRIBUTING.md</code>, <code>SECURITY.md</code>, <code>LICENSE</code> e a pasta <code>.github/</code> com os workflows de CI, Gitleaks e Dependabot.</p>
  </div>
  <div class="roadmap-step">
    <h4>Fase 2: Dependências e Configurações de Ambiente</h4>
    <p>Expandir o <code>.gitignore</code>, atualizar o <code>.env.example</code> e sincronizar o <code>requirements.txt</code> com os pacotes oficiais.</p>
  </div>
  <div class="roadmap-step">
    <h4>Fase 3: Unificação dos Testes com Pytest</h4>
    <p>Criar o <code>pytest.ini</code> e rodar a suíte via <code>pytest --cov</code> garantindo que o CI no GitHub Actions execute 100% verde.</p>
  </div>
  <div class="roadmap-step">
    <h4>Fase 4: Documentação Canônica e README</h4>
    <p>Preencher o <code>README.md</code> oficial no padrão FATEC Olímpia com os dados dos integrantes e estruturar os 4 documentos em <code>docs/</code>.</p>
  </div>
</div>

<div class="footer-note">
  Documento gerado automaticamente para alinhamento interno da equipe. Hub Central de Marketplaces · Web III FATEC Olímpia.
</div>

</body>
</html>
"""

def generate_pdf():
    workspace = r"c:\Users\allan\OneDrive\Área de Trabalho\WEB-III---Project"
    temp_html = os.path.join(workspace, "scripts", "temp_relatorio.html")
    output_pdf = os.path.join(workspace, "relatorio-conformidade-template-web3.pdf")
    
    with open(temp_html, "w", encoding="utf-8") as f:
        f.write(HTML_CONTENT)
    
    edge_exe = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    if not os.path.exists(edge_exe):
        edge_exe = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
        
    cmd = [
        edge_exe,
        "--headless",
        "--disable-gpu",
        "--no-pdf-header-footer",
        f"--print-to-pdf={output_pdf}",
        temp_html
    ]
    
    print(f"Executando gerador de PDF...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if os.path.exists(temp_html):
        os.remove(temp_html)
        
    if os.path.exists(output_pdf):
        size_kb = os.path.getsize(output_pdf) / 1024
        print(f"[SUCESSO] PDF gerado em: {output_pdf} ({size_kb:.1f} KB)")
    else:
        print(f"[ERRO] Falha ao gerar PDF. Saída: {result.stderr}")

if __name__ == "__main__":
    generate_pdf()
