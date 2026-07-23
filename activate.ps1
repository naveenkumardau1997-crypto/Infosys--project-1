# ============================================================
#  activate.ps1 - Universal venv activator
#  Usage: . .\activate.ps1   (note the leading dot-space)
# ============================================================

Write-Host ""
Write-Host " Online Exam Monitoring Platform" -ForegroundColor Cyan
Write-Host " =================================" -ForegroundColor Cyan

if (Test-Path ".\venv\Scripts\Activate.ps1") {
    Write-Host " [OK] Activating: venv\" -ForegroundColor Green
    & ".\venv\Scripts\Activate.ps1"
}
elseif (Test-Path ".\.venv\Scripts\Activate.ps1") {
    Write-Host " [OK] Activating: .venv\" -ForegroundColor Green
    & ".\.venv\Scripts\Activate.ps1"
}
else {
    Write-Host " [WARN] No virtual environment found. Run setup.ps1 first." -ForegroundColor Yellow
}

Write-Host ""
Write-Host " Commands:" -ForegroundColor White
Write-Host "   python app.py              # Start Flask on :5000" -ForegroundColor Gray
Write-Host "   streamlit run dashboard.py # Start Streamlit on :8501" -ForegroundColor Gray
Write-Host ""
