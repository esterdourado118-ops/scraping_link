# ====================================================================
# Script para Resolver Problemas de SSL com Proxy
# ====================================================================
#
# Execute este script se estiver tendo erro:
# "SSL: CERTIFICATE_VERIFY_FAILED"
#
# ====================================================================

Write-Host ""
Write-Host "============================================================" -ForegroundColor Blue
Write-Host "           CORRIGINDO PROBLEMA DE SSL                       " -ForegroundColor Blue
Write-Host "============================================================" -ForegroundColor Blue
Write-Host ""

# Definir variável de ambiente para desabilitar verificação SSL
$env:WDM_SSL_VERIFY = '0'

Write-Host "Configurando variaveis de ambiente..." -ForegroundColor Yellow
Write-Host ""

# Definir permanentemente para o usuário
[System.Environment]::SetEnvironmentVariable('WDM_SSL_VERIFY','0','User')

Write-Host "Verificacao SSL desabilitada para WebDriver Manager" -ForegroundColor Green
Write-Host ""

Write-Host "Testando configuracao..." -ForegroundColor Yellow
Write-Host ""

# Tentar executar session novamente
Write-Host "Executando: .\run.ps1 session" -ForegroundColor Cyan
Write-Host ""

.\run.ps1 session


