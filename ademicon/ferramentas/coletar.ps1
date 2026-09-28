# Coleta automática de pesquisa (YouTube, site Ademicon, Instagram, Facebook) e envio para o GitHub.
#
# Primeira vez (faz login e agenda a coleta semanal):
#   powershell -ExecutionPolicy Bypass -File "$HOME\boa\ademicon\ferramentas\coletar.ps1" -Instalar
#
# Depois disso roda sozinho toda segunda às 9h (Agendador de Tarefas do Windows, tarefa "Ademicon-Coleta").

param([switch]$Instalar)

$ErrorActionPreference = "Continue"
$Repo = Join-Path $HOME "boa"
$Branch = "claude/fervent-ramanujan-m05uby"

if (-not (Test-Path $Repo)) {
    git clone https://github.com/FeCoelho73/boa.git $Repo
}
Set-Location $Repo
git checkout $Branch
git pull --no-rebase --no-edit origin $Branch

py -m pip install -q -U yt-dlp youtube-comment-downloader requests beautifulsoup4 playwright
py -m playwright install chromium

if ($Instalar) {
    # Primeiro uso: abre o navegador para você logar no Instagram e no Facebook (uma vez só).
    py ademicon/ferramentas/raspar_social.py

    $Acao = New-ScheduledTaskAction -Execute "powershell.exe" `
        -Argument "-ExecutionPolicy Bypass -WindowStyle Hidden -File `"$Repo\ademicon\ferramentas\coletar.ps1`""
    $Quando = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Monday -At 9am
    Register-ScheduledTask -TaskName "Ademicon-Coleta" -Action $Acao -Trigger $Quando -Force | Out-Null
    Write-Host "Coleta semanal agendada (segunda-feira, 9h)."
} else {
    py ademicon/ferramentas/raspar_social.py --automatico
}

py ademicon/ferramentas/raspar.py

git add -A ademicon/pesquisa/raw
git commit -m "coleta automatica $(Get-Date -Format 'yyyy-MM-dd')"
git push origin $Branch
Write-Host "Coleta enviada para o GitHub."
