param(
    [string]$RemoteUrl
)

if (-not $RemoteUrl) {
    $RemoteUrl = Read-Host "Enter the GitHub remote URL (HTTPS) e.g. https://github.com/you/AutoDeployLR-modified.git"
}

Write-Host "Initializing git repository and pushing to $RemoteUrl"

git init
git add .
git commit -m "Initial commit: CRISP-DM linear regression Streamlit app"
git branch -M main
git remote add origin $RemoteUrl
git push -u origin main

Write-Host "Done. If push failed, check your credentials and remote URL."
