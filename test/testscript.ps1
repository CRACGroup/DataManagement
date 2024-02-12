Write-Host "Automatization script testing"
Write-Host "Will try to construct scp commands"
$datatext = Get-Content C:\Users\Mixtli\OneDrive\Work\UCC\Research\DataManagement\testIPandPath.txt
$datestamp = Get-Date -Format "yyyyMMdd\\\\"
for ($i=0; $i -lt $datatext.Count; $i++)
{
    $actcomm = $datatext[$i]+$datestamp+" ."
    Write-Host "SCP instruction:" $actcomm
    Write-Host "Trying actual command:"
    echo $actcomm
}
#python C:\Users\Mixtli\OneDrive\Work\UCC\Research\DataManagement\testpy.py