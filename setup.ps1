$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$Python = Get-Command py -ErrorAction SilentlyContinue
if ($Python) {
  & py "$Root\scripts\scaffold.py" --target "$Root" --zip "$Root\interviewprep-bd.zip"
} else {
  & python "$Root\scripts\scaffold.py" --target "$Root" --zip "$Root\interviewprep-bd.zip"
}
if ($LASTEXITCODE -ne 0) { throw "Project generation failed." }
Write-Output "Project files refreshed and ZIP created at $Root\interviewprep-bd.zip"
