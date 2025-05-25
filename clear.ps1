# Path to the folder
$folderPath = "fixed_programs"

# Get all files except format.md
Get-ChildItem -Path $folderPath -Recurse |
Where-Object { $_.Name -ne "format.md" } |
Remove-Item -Recurse -Force
