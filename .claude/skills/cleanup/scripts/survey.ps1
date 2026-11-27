# Disk survey for the cleanup skill. Read-only: it deletes and changes nothing.
# Usage (from anywhere inside the repository):
#   powershell -NoProfile -ExecutionPolicy Bypass -File .claude\skills\cleanup\scripts\survey.ps1 [-OutDir work\cleanup-survey] [-SkipSizes]
# Writes worktrees.csv, branches.csv and folders.txt to OutDir and prints a summary.
param(
  [string]$OutDir = 'work\cleanup-survey',
  [switch]$SkipSizes
)
$ErrorActionPreference = 'SilentlyContinue'
$root = (git rev-parse --show-toplevel)
if (-not $root) { Write-Error 'Not inside a git repository.'; exit 1 }
Set-Location $root
$rootWin = (Get-Item -LiteralPath $root).FullName
if (-not [System.IO.Path]::IsPathRooted($OutDir)) { $OutDir = Join-Path $rootWin $OutDir }
New-Item -ItemType Directory -Force -Path $OutDir | Out-Null
$byproduct = '\.(import|uid|TMP)$|\.godot/'

function Get-SizeMB($p) {
  if ($SkipSizes) { return 0 }
  $s = (Get-ChildItem -LiteralPath $p -Recurse -Force -File -ErrorAction SilentlyContinue | Measure-Object Length -Sum).Sum
  if (-not $s) { $s = 0 }
  [math]::Round($s / 1MB, 0)
}
function Show-Children($p, $n) {
  if (-not (Test-Path -LiteralPath $p)) { return }
  "=== $p"
  Get-ChildItem -Force -LiteralPath $p | ForEach-Object {
    $s = if ($_.PSIsContainer) { Get-SizeMB $_.FullName } else { [math]::Round($_.Length / 1MB, 0) }
    [pscustomobject]@{ MB = $s; Name = $_.Name; Modified = $_.LastWriteTime.ToString('yyyy-MM-dd') }
  } | Sort-Object MB -Descending | Select-Object -First $n | Format-Table -AutoSize | Out-String -Width 200
}

git fetch --quiet
"main: " + (git rev-parse --short main) + "   free on drive: " + [math]::Round((Get-PSDrive ($rootWin.Substring(0, 1))).Free / 1GB, 0) + " GB"

# ---- worktrees
$wts = @(); $cur = $null
foreach ($l in (git worktree list --porcelain)) {
  if ($l -like 'worktree *') { $cur = [ordered]@{ Path = $l.Substring(9); Branch = '(detached)'; Head = '' }; $wts += , $cur }
  elseif ($l -like 'HEAD *') { $cur.Head = $l.Substring(5) }
  elseif ($l -like 'branch *') { $cur.Branch = $l.Substring(7) -replace '^refs/heads/', '' }
}
$rows = foreach ($w in $wts) {
  if ($w.Path -eq $root) { continue }
  $p = $w.Path
  git merge-base --is-ancestor $w.Head main 2>$null
  $merged = ($LASTEXITCODE -eq 0)
  $status = @(git -C $p status --porcelain 2>$null)
  $real = @($status | Where-Object { $_ -notmatch $byproduct })
  $newest = (Get-ChildItem -LiteralPath $p -Recurse -File -Force -ErrorAction SilentlyContinue |
      Where-Object { $_.FullName -notmatch '\\\.godot\\' } |
      Sort-Object LastWriteTime -Descending | Select-Object -First 1).LastWriteTime
  [pscustomobject]@{
    MB         = Get-SizeMB $p
    Dir        = Split-Path $p -Leaf
    Branch     = $w.Branch
    Head       = $w.Head.Substring(0, 9)
    Merged     = $merged                                         # HEAD is an ancestor of main
    Ahead      = (git rev-list --count "main..$($w.Head)")
    # commits whose change is not in main under any hash; 0 means the work is in main already
    NotInMain  = @(git cherry main $w.Head | Where-Object { $_ -like '+*' }).Count
    OnRemote   = ("" + (git branch -r --contains $w.Head | Where-Object { $_ -notmatch 'HEAD' } | Select-Object -First 1)).Trim()
    Commit     = (git log -1 --format=%cs $w.Head)
    NewestFile = if ($newest) { $newest.ToString('yyyy-MM-dd') } else { '?' }
    Dirty      = $status.Count
    RealDirty  = $real.Count                                     # uncommitted files that are not import byproducts
    RealSample = (($real | Select-Object -First 3 | ForEach-Object { $_.Substring(3) }) -join '; ')
    Path       = $p
  }
}
$rows | Export-Csv -NoTypeInformation -Path (Join-Path $OutDir 'worktrees.csv')
"##### WORKTREES (" + @($rows).Count + ", " + [math]::Round((($rows | Measure-Object MB -Sum).Sum) / 1024, 0) + " GB)"
$rows | Sort-Object Merged, MB -Descending | Select-Object MB, Dir, Branch, Merged, NotInMain, OnRemote, Commit, NewestFile, RealDirty, RealSample | Format-Table -AutoSize | Out-String -Width 300

# ---- worktree folders git does not know about
"##### UNREGISTERED WORKTREE FOLDERS"
$reg = $wts | ForEach-Object { Split-Path $_.Path -Leaf }
$parents = @($wts | ForEach-Object { Split-Path $_.Path -Parent } | Where-Object { $_ -match 'worktrees' } | Sort-Object -Unique)
foreach ($par in $parents) {
  Get-ChildItem -LiteralPath $par -Directory -Force | Where-Object { $reg -notcontains $_.Name } | ForEach-Object {
    "{0,6} MB  {1}  {2}" -f (Get-SizeMB $_.FullName), $_.LastWriteTime.ToString('yyyy-MM-dd'), $_.FullName
  }
}

# ---- branches with no worktree
$wtBranches = $wts | ForEach-Object { $_.Branch }
$brows = foreach ($x in (git for-each-ref refs/heads --format='%(refname:short)|%(committerdate:short)')) {
  $parts = $x -split '\|'
  if ($wtBranches -contains $parts[0] -or $parts[0] -eq 'main') { continue }
  git merge-base --is-ancestor $parts[0] main 2>$null
  [pscustomobject]@{ Branch = $parts[0]; Date = $parts[1]; Merged = ($LASTEXITCODE -eq 0) }
}
$brows | Export-Csv -NoTypeInformation -Path (Join-Path $OutDir 'branches.csv')
"##### BRANCHES WITHOUT A WORKTREE: merged " + @($brows | Where-Object Merged).Count + ", not merged " + @($brows | Where-Object { -not $_.Merged }).Count
$brows | Where-Object { -not $_.Merged } | Format-Table -AutoSize | Out-String -Width 200

# ---- folders
"##### FOLDERS (largest first)"
$folders = & {
  Show-Children $rootWin 15
  Show-Children (Join-Path $rootWin 'work') 40
  Show-Children (Join-Path $rootWin 'docs\captures') 15
  Show-Children (Split-Path $rootWin -Parent) 12
}
$folders | Set-Content -Encoding utf8 -Path (Join-Path $OutDir 'folders.txt')
$folders
"##### UNTRACKED IN THE MAIN CHECKOUT (not ignored)"
git status --porcelain | Where-Object { $_ -like '??*' -and $_ -notmatch '\.uid$' }
"##### GIT STORE"
git count-objects -vH | Where-Object { $_ -match 'size-pack|size:|garbage' }
"stashes: " + @(git stash list).Count
"Written to $OutDir"
