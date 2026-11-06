# Probabilidades no Futebol: guia de publicação

Arquivos: `index.html` (site), `data.json` (todos os dados), `privacidade.html`, `termos.html`,
`scripts/update.py` + `.github/workflows/update.yml` (robô de atualização), `robots.txt`, `sitemap.xml`.

## 1. Publicar (grátis, ~10 min)
1. Crie conta em github.com e um repositório novo (público), por exemplo `futebol`.
2. Envie todos os arquivos desta pasta (botão "Add file → Upload files"; inclua as pastas `scripts` e `.github`).
3. No repositório: **Settings → Pages → Branch: main / root → Save**. O site abre em `https://SEU-USUARIO.github.io/futebol/`.
   (Alternativa: Netlify → "Add new site → Import from Git" ou arraste a pasta em app.netlify.com/drop.)

## 2. Domínio próprio
Registre um domínio (Registro.br, para .com.br). Em **Settings → Pages → Custom domain** coloque o domínio e siga as instruções de DNS.
Depois troque `SEU-DOMINIO.com.br` em `index.html`, `robots.txt` e `sitemap.xml`.

## 3. Atualização automática (Série A e Premier League)
1. Crie uma chave grátis em football-data.org/client/register.
2. No repositório: **Settings → Secrets and variables → Actions → New repository secret**, nome `FOOTBALL_DATA_KEY`, valor = sua chave.
3. Aba **Actions → Atualizar dados → Run workflow** para testar. Depois roda sozinho a cada 3 horas.
4. Confira na 1ª execução: a coluna "Últimos 5" da Série A deve terminar no jogo mais recente. Se estiver invertida, mude `FORM_NEWEST_LAST` para `False` em `scripts/update.py`.

Limites: não testei a chamada real à API (só com dados simulados). Confira se seu plano grátis cobre as competições e se permite uso comercial.
**Série B e Libertadores não têm robô**: edite `data.json` à mão (ou me peça).

## 4. Anúncios e métricas
Em `index.html`, no bloco `SITE`, preencha `adsenseId` (ex.: `ca-pub-123...`, depois da aprovação do Google AdSense) e/ou `gaId` (Google Analytics, `G-XXXX`).
Os scripts só carregam depois do aceite no aviso de cookies. Preencha `[SEU NOME]`, `[SEU E-MAIL]` e `[DATA]` nas páginas de privacidade e termos.

## 5. Antes de monetizar
Use dados de uma fonte que permita uso comercial e peça revisão jurídica das páginas legais, principalmente se for divulgar casas de apostas (regulamentadas no Brasil; só maiores de 18).
