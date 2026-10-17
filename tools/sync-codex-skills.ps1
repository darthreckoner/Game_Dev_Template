<#
.SYNOPSIS
Mirror the coder skills from .claude/skills into .agents/skills for Codex.

.DESCRIPTION
Claude Code reads project skills from .claude/skills only; Codex reads
.agents/skills and invokes them as $<name>. This copies every skill except the
Director's (game-director, art-direction, retro) so a Codex session can use
$build-check and the engine skill. Rerun after changing a skill. Safe to repeat:
each mirrored skill folder is replaced whole. Works in Windows PowerShell 5.1
and PowerShell 7.

.PARAMETER ProjectRoot
The project folder. Defaults to the parent of this script's folder.

.EXAMPLE
.\tools\sync-codex-skills.ps1
#>
[CmdletBinding()]
param(
    [string]$ProjectRoot = (Split-Path -Parent $PSScriptRoot)
)

$ErrorActionPreference = 'Stop'
$from = Join-Path $ProjectRoot '.claude\skills'
$to = Join-Path $ProjectRoot '.agents\skills'
$directorOnly = @('game-director', 'art-direction', 'retro')

if (-not (Test-Path -LiteralPath $from)) { throw "No skills folder at $from" }
New-Item -ItemType Directory -Force -Path $to | Out-Null

$mirrored = @()
foreach ($skill in Get-ChildItem -LiteralPath $from -Directory) {
    if ($directorOnly -contains $skill.Name) { continue }
    $target = Join-Path $to $skill.Name
    & robocopy $skill.FullName $target /MIR /NFL /NDL /NJH /NJS /NP /R:1 /W:1 | Out-Null
    if ($LASTEXITCODE -ge 8) { throw "robocopy failed for $($skill.Name) with exit code $LASTEXITCODE" }
    $mirrored += $skill.Name
}

Write-Host ("Mirrored into {0}: {1}" -f $to, ($mirrored -join ', '))
Write-Host 'Codex invokes them as $<name>, for example $build-check.'
