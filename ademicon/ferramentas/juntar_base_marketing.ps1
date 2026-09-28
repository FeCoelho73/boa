# Junta as análises de VSL, copy e criativos do computador num único repositório PRIVADO
# no GitHub (FeCoelho73/base-marketing), SEM vídeos, para o Claude conseguir ler.
#
# Uso (PowerShell):
#   powershell -ExecutionPolicy Bypass -File "$HOME\boa\ademicon\ferramentas\juntar_base_marketing.ps1"
#
# Pode rodar de novo sempre que quiser atualizar: ele copia o que mudou e envia.

$ErrorActionPreference = "Continue"
$Destino = Join-Path $HOME "base-marketing"
$Doc = Join-Path $HOME "OneDrive\Documentos"

# Pasta de origem  =>  nome da subpasta no repositório
$Pastas = [ordered]@{
    (Join-Path $Doc "Claude")                                      = "claude"
    (Join-Path $HOME "Downloads\Marketing_VSL")                    = "marketing-vsl"
    (Join-Path $Doc "Bloco de notas\Marketing_Copy_VSL")           = "marketing-copy-vsl"
    (Join-Path $HOME "Videos\copy-base")                           = "copy-base"
    (Join-Path $Doc "VF3\Copy VSL")                                = "vf3-copy-vsl"
    (Join-Path $Doc "VF3\CRIATIVOS")                               = "vf3-criativos"
    (Join-Path $Doc "CURSOS\VSL")                                  = "cursos-vsl"
    (Join-Path $Doc "CONTEÚDO PENDRIVE ANTIGO\VSL")                = "pendrive-vsl"
    (Join-Path $Doc "SUPERPALETEIRA\CRIATIVOS")                    = "superpaleteira-criativos"
    (Join-Path $Doc "VILA AMERICO BAR E RESTAURANTE\CRIATIVOS VILA AMERICO") = "vila-americo-criativos"
    (Join-Path $HOME "OneDrive\Área de Trabalho\BOA\Criativos")    = "boa-criativos"
    (Join-Path $HOME "OneDrive\Área de Trabalho\BOA\CRIATIVOS  II") = "boa-criativos-2"
    (Join-Path $HOME "OneDrive\Área de Trabalho\BOA\VSL longa")    = "boa-vsl-longa"
    (Join-Path $HOME "Videos\BOA\_ORGANIZADO\1-VSL-CURTA")          = "boa-vsl-curta"
    (Join-Path $HOME "Videos\BOA\_ORGANIZADO\2-VSL-LONGA")          = "boa-vsl-longa-2"
    (Join-Path $HOME "Videos\criativos")                           = "videos-criativos"
}

# Só documentos, código e imagens (nada de vídeo/áudio); arquivos até 5 MB.
$Tipos = @("*.md","*.txt","*.pdf","*.doc","*.docx","*.rtf","*.odt","*.xlsx","*.xls","*.csv","*.pptx",
           "*.json","*.html","*.htm","*.js","*.ts","*.tsx","*.py","*.yml","*.yaml","*.srt","*.vtt",
           "*.png","*.jpg","*.jpeg","*.webp","*.gif","*.svg")

# 1. GitHub CLI e login
if (-not (Get-Command gh -ErrorAction SilentlyContinue)) {
    winget install --id GitHub.cli -e --accept-source-agreements --accept-package-agreements
    $env:Path = [Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [Environment]::GetEnvironmentVariable("Path","User")
}
gh auth status 2>$null | Out-Null
if ($LASTEXITCODE -ne 0) { gh auth login -w -p https }
gh auth setup-git | Out-Null

# 2. Copiar (sem vídeos)
New-Item -ItemType Directory -Force -Path $Destino | Out-Null
foreach ($origem in $Pastas.Keys) {
    if (-not (Test-Path -LiteralPath $origem)) { Write-Host "  (não existe) $origem" -ForegroundColor DarkGray; continue }
    $alvo = Join-Path $Destino $Pastas[$origem]
    Write-Host "Copiando $origem -> $($Pastas[$origem])" -ForegroundColor Cyan
    robocopy "$origem" "$alvo" $Tipos /S /MAX:5242880 /XD node_modules .git .venv __pycache__ /R:0 /W:0 /NFL /NDL /NJH /NJS /NP | Out-Null
}

# 3. Enviar para o GitHub como PRIVADO
Set-Location $Destino
if (-not (Test-Path ".git")) { git init -q; git branch -M main }
"# Base de marketing do Fernando (VSL, copy, criativos)`n`nCopiado automaticamente por juntar_base_marketing.ps1 (sem vídeos)." | Out-File -Encoding utf8 README.md
".env`n*.env`nnode_modules/`n.venv/" | Out-File -Encoding utf8 .gitignore
git add -A
git -c user.name="Fernando" -c user.email="ricapelmkt@gmail.com" commit -q -m "Atualiza base de marketing" 2>$null | Out-Null

$remoto = git remote get-url origin 2>$null
if (-not $remoto) {
    gh repo create base-marketing --private --source . --push
} else {
    git push -u origin main
}

Write-Host "`n==================== RESULTADO ====================" -ForegroundColor Green
gh repo view FeCoelho73/base-marketing --json name,visibility,diskUsage,url
$qtd = (git ls-files | Measure-Object).Count
Write-Host "Arquivos enviados: $qtd"
Write-Host "Mande 'pronto' para o Claude."
