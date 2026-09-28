# Sobe para o GitHub (como repositórios PRIVADOS) todas as pastas de trabalho do seu computador,
# para o Claude conseguir ler: análises de VSL, criativos, copy etc.
#
# Uso (PowerShell, uma linha):
#   powershell -ExecutionPolicy Bypass -File "$HOME\boa\ademicon\ferramentas\subir_tudo_github.ps1"
#
# Opcional: informar pastas específicas (separadas por vírgula):
#   powershell -ExecutionPolicy Bypass -File "$HOME\boa\ademicon\ferramentas\subir_tudo_github.ps1" -Pastas "C:\Users\fecoe\Documents\Claude,C:\Users\fecoe\Desktop\VSL"
#
# O que ele faz:
#   1. Instala o GitHub CLI (gh) se faltar e faz login (abre o navegador uma vez).
#   2. Procura na sua pasta de usuário: repositórios git e pastas com nomes de trabalho
#      (claude, vsl, criativo, copy, ademicon, analise, funil, anuncio, marketing).
#   3. Para cada uma: se não é git, inicializa; se não tem GitHub, cria repositório PRIVADO; envia tudo.
#   4. Mostra a lista final. Mande essa lista para o Claude.

param([string]$Pastas = "")

$ErrorActionPreference = "Continue"

function Garantir-Gh {
    if (-not (Get-Command gh -ErrorAction SilentlyContinue)) {
        Write-Host "Instalando GitHub CLI..." -ForegroundColor Yellow
        winget install --id GitHub.cli -e --accept-source-agreements --accept-package-agreements
        $env:Path = [System.Environment]::GetEnvironmentVariable("Path", "Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path", "User")
    }
    gh auth status 2>$null | Out-Null
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Faça login no GitHub no navegador (conta FeCoelho73)..." -ForegroundColor Yellow
        gh auth login -w -p https
    }
    gh auth setup-git | Out-Null
}

function Nome-Repo($caminho) {
    $n = (Split-Path $caminho -Leaf).ToLower() -replace '[^a-z0-9._-]', '-'
    return ($n -replace '-+', '-').Trim('-')
}

function Enviar-Pasta($caminho) {
    Push-Location $caminho
    try {
        if (-not (Test-Path ".git")) {
            git init -q
            git branch -M main
        }
        # Nunca subir segredos e lixo comum
        if (-not (Test-Path ".gitignore")) {
            "node_modules/`n.env`n*.env`n__pycache__/`n.venv/`n*.mp4`n*.mov`n*.zip`n.perfil-navegador/`nademicon-dados/" | Out-File -Encoding utf8 .gitignore
        }
        git add -A
        git -c user.name="Fernando" -c user.email="ricapelmkt@gmail.com" commit -q -m "Envio automático para o GitHub" 2>$null | Out-Null

        $remoto = git remote get-url origin 2>$null
        if (-not $remoto) {
            $nome = Nome-Repo $caminho
            gh repo create $nome --private --source . --push 2>&1 | Out-Host
            $remoto = git remote get-url origin 2>$null
        } else {
            $ramo = git rev-parse --abbrev-ref HEAD
            git push -u origin $ramo 2>&1 | Out-Host
        }
        return $remoto
    } finally {
        Pop-Location
    }
}

Garantir-Gh

$alvos = @()
if ($Pastas) {
    $alvos = $Pastas.Split(",") | ForEach-Object { $_.Trim() } | Where-Object { Test-Path $_ }
} else {
    Write-Host "Procurando pastas de trabalho em $HOME ..." -ForegroundColor Cyan
    $ignorar = 'AppData|node_modules|\\\.|OneDrive\\Imagens|Program Files|ademicon-dados|\\boa$'
    $repos = Get-ChildItem $HOME -Directory -Recurse -Depth 4 -Force -Filter ".git" -ErrorAction SilentlyContinue |
        ForEach-Object { $_.Parent.FullName }
    $porNome = Get-ChildItem $HOME -Directory -Recurse -Depth 3 -ErrorAction SilentlyContinue |
        Where-Object { $_.Name -match '(?i)claude|vsl|criativ|copy|ademicon|analise|análise|funil|anuncio|anúncio|marketing' } |
        ForEach-Object { $_.FullName }
    $alvos = ($repos + $porNome) | Where-Object { $_ -notmatch $ignorar } | Sort-Object -Unique
    # remove subpastas de pastas já incluídas
    $alvos = $alvos | Where-Object { $atual = $_; -not ($alvos | Where-Object { $_ -ne $atual -and $atual.StartsWith($_ + "\") }) }
}

if (-not $alvos) {
    Write-Host "Nenhuma pasta encontrada. Rode de novo com -Pastas ""C:\caminho\da\pasta""" -ForegroundColor Red
    exit 1
}

Write-Host "`nPastas que serão enviadas (PRIVADAS):" -ForegroundColor Cyan
$alvos | ForEach-Object { Write-Host "  - $_" }
$ok = Read-Host "`nEnviar todas? (S/N)"
if ($ok -notmatch '^[sS]') { exit 0 }

$resultado = @()
foreach ($p in $alvos) {
    Write-Host "`n>>> $p" -ForegroundColor Yellow
    $url = Enviar-Pasta $p
    $resultado += "$p  ->  $url"
}

Write-Host "`n==================== RESULTADO ====================" -ForegroundColor Green
$resultado | ForEach-Object { Write-Host $_ }
Write-Host "`nÚltimo passo (1 clique): libere os repositórios para o Claude:" -ForegroundColor Green
Write-Host "  https://github.com/apps/claude/installations/select_target  -> sua conta -> 'All repositories' -> Save"
Start-Process "https://github.com/apps/claude/installations/select_target"
Write-Host "`nDepois copie a lista RESULTADO acima e mande para o Claude."
