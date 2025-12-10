<#
Helper script to push local commits to the fork using HTTPS and a PAT.
This script will temporarily set the 'fork' remote to the HTTPS URL and push.
It will prompt for GitHub username and a Personal Access Token (PAT) which is used as password.
Do NOT paste PAT into chat. Run this locally in a secure environment.

Usage: .\tools\push_via_https.ps1 -RepoUrl 'https://github.com/ungke/adi.git' -Branch 'ci/docker-setup-rebased'
#>

param(
    [string]$RepoUrl = 'https://github.com/ungke/adi.git',
    [string]$Branch = 'ci/docker-setup-rebased'
)

Write-Host "This will push the current HEAD to remote branch $Branch on $RepoUrl"
Write-Host "You will be prompted for GitHub username and a Personal Access Token (PAT)."

 $username = Read-Host "GitHub username"
 $pat = Read-Host -AsSecureString "Personal Access Token (PAT)"
 $bstr = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($pat)
 $plainPat = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto($bstr)

# Save current fork URL so we can restore
$currentFork = git remote get-url fork 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "Remote 'fork' not configured - adding 'fork' pointing to $RepoUrl"
    git remote add fork $RepoUrl
    $currentFork = $null
}

try {
    git remote set-url fork $RepoUrl
    # Use basic auth with username:pat in URL for a single push only
    # construct authenticated URL safely
    $authPrefix = 'https://' + $username + ':' + $plainPat + '@'
    $authUrl = $RepoUrl -replace '^https://', $authPrefix
    Write-Host "Pushing to $authUrl (remote branch: $Branch)"
    git push $authUrl HEAD:`$Branch
    if ($LASTEXITCODE -eq 0) { Write-Host 'Push succeeded' } else { Write-Error 'Push failed' }
} finally {
    # restore original fork remote
    if ($null -ne $currentFork) { git remote set-url fork $currentFork } else { git remote remove fork }
    # clear plainPat in memory
    $plainPat = $null
}
