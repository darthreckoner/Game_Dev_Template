<#
.SYNOPSIS
Start a new game project from this template.

.DESCRIPTION
Copies the starter into an empty destination folder, leaving out the template's
own maintenance material (.git, work/, docs/research/, local settings, and this
script), writes the game name into DESIGN.md and BUILD_PROMPT.md, and makes the
first commit on main. Works in Windows PowerShell 5.1 and PowerShell 7.

.PARAMETER Name
The game's name, as it should appear in DESIGN.md.

.PARAMETER Dest
Destination folder. Must not exist or must be empty. Defaults to a sibling of
the template folder named after the game.

.PARAMETER NoGit
Skip git init and the first commit.

.EXAMPLE
.\tools\new-game.ps1 -Name "My Game" -Dest C:\Dev\My_Game
#>
[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)][string]$Name,
    [string]$Dest,
    [switch]$NoGit
)

$ErrorActionPreference = 'Stop'
$source = Split-Path -Parent $PSScriptRoot

if (-not $Dest) {
    $folder = $Name -replace '[^A-Za-z0-9._-]', '_'
    $Dest = Join-Path (Split-Path -Parent $source) $folder
}

if (Test-Path -LiteralPath $Dest) {
    if (@(Get-ChildItem -LiteralPath $Dest -Force).Count -gt 0) {
        throw "Destination exists and is not empty: $Dest"
    }
} else {
    New-Item -ItemType Directory -Path $Dest | Out-Null
}
$Dest = (Resolve-Path -LiteralPath $Dest).Path

# Maintenance material that stays in the template source.
$excludeDirs = @(
    (Join-Path $source '.git'),
    (Join-Path $source 'work'),
    (Join-Path $source '.agent'),
    (Join-Path $source '.workflow'),
    (Join-Path $source 'docs\research')
)
$excludeFiles = @('new-game.ps1', 'settings.local.json')

$robocopyArgs = @($source, $Dest, '/E', '/XD') + $excludeDirs + @('/XF') + $excludeFiles +
    @('/NFL', '/NDL', '/NJH', '/NJS', '/NP', '/R:1', '/W:1')
& robocopy @robocopyArgs | Out-Null
if ($LASTEXITCODE -ge 8) { throw "robocopy failed with exit code $LASTEXITCODE" }

# Fill in the game name (UTF-8 without BOM, line endings untouched).
$utf8 = New-Object System.Text.UTF8Encoding $false
foreach ($rel in @('DESIGN.md', 'BUILD_PROMPT.md')) {
    $path = Join-Path $Dest $rel
    $text = [System.IO.File]::ReadAllText($path)
    [System.IO.File]::WriteAllText($path, $text.Replace('[Game Name]', $Name), $utf8)
}

$templateRef = 'unversioned template'
if (Test-Path -LiteralPath (Join-Path $source '.git')) {
    $sha = & git -C $source rev-parse --short HEAD
    if ($sha) { $templateRef = "Game_Dev_Template $sha" }
}

if (-not $NoGit) {
    & git -C $Dest -c init.defaultBranch=main init | Out-Null
    # safecrlf=false only quiets the "LF will be replaced by CRLF" notices;
    # .gitattributes still normalizes line endings as usual.
    & git -C $Dest -c core.safecrlf=false add -A
    & git -C $Dest commit -q -m "Start $Name from $templateRef"
    if ($LASTEXITCODE -ne 0) {
        Write-Warning "git commit failed; the files are in place, commit them yourself."
    }
}

Write-Host ""
Write-Host "Created $Dest from $templateRef."
Write-Host "Next:"
Write-Host "  1. Open it in Claude Code and ask for the design interview (Claude is the Director)."
Write-Host "  2. For coder steps, open a fresh session with the model the prompt names"
Write-Host "     and paste the prompt from CODER_PROMPTS.md."
Write-Host "  3. Using Codex for tickets? Run tools\sync-codex-skills.ps1 there once."
