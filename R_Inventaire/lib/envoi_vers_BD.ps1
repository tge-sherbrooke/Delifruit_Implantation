
$Chemin_MongoDB = "$($env:LOCALAPPDATA)\MongoDBCompass"

if (Test-Path $Chemin_MongoDB) {
    Set-Location $Chemin_MongoDB
    Write-Host -BackgroundColor Blue "$(Get-Location)" -ForegroundColor White

    .\mongoimport.exe --uri 'mongodb+srv://dbtytren:Gl2v&di4su$A@cluster0.1z5z20t.mongodb.net/Base_De_Donnees_RH' `
        --collection 'Utilisateurs' --type json --file "D:\UCDownloads\OneDrive\A2025\Implantation_reseau\ESP\Delifruit_Implantation\R_Inventaire\Sortie\formulaire.json"
}