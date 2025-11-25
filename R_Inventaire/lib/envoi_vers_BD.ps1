
Write-Host -BackgroundColor Blue "Envoi des données vers la base de données via Powershell..." -ForegroundColor White

$Chemin_MongoDB = "$($env:LOCALAPPDATA)\MongoDBCompass"


$Fichier_Utilisateurs = Join-Path $PSScriptRoot "../Sortie/formulaireRH.json"
$Fichier_Utilisateurs = Resolve-Path $Fichier_Utilisateurs

$Fichier_Inventaires = Join-Path $PSScriptRoot "../Sortie/formulaireIN.json"
$Fichier_Inventaires = Resolve-Path $Fichier_Inventaires

$Fichier_Init_RH = Join-Path $PSScriptRoot "_init_RH.json"

$Fichier_Init_IN = Join-Path $PSScriptRoot "_init_IN.json"



if (Test-Path $Fichier_Utilisateurs) {

    $Contenu_Utilisateurs = Get-Content $Fichier_Utilisateurs -Raw | ConvertFrom-Json | ConvertTo-Json -Compress -Depth 100
    $Contenu_Initial = Get-Content $Fichier_Init_RH -Raw | ConvertFrom-Json | ConvertTo-Json -Compress -Depth 100
    $Resultat_RH = Compare-Object $Contenu_Utilisateurs $Contenu_Initial

} 

if (Test-Path $Fichier_Inventaires) {
    $Contenu_Inventaires = Get-Content $Fichier_Inventaires -Raw | ConvertFrom-Json | ConvertTo-Json -Compress -Depth 100
    $Contenu_Initial_IN = Get-Content $Fichier_Init_IN -Raw | ConvertFrom-Json | ConvertTo-Json -Compress -Depth 100
    $Resultat_IN = Compare-Object $Contenu_Inventaires $Contenu_Initial_IN
}

if ($Resultat_RH) {

    if (Test-Path $Chemin_MongoDB) {

        Set-Location $Chemin_MongoDB
        Write-Host -BackgroundColor Blue "$(Get-Location)" -ForegroundColor White

        .\mongoimport.exe --uri 'mongodb+srv://dbtytren:Gl2v&di4su$A@cluster0.1z5z20t.mongodb.net/Base_De_Donnees_RH' `
            --collection 'Utilisateurs' --type json --file $Fichier_Utilisateurs        
    }

} 

if ($Resultat_IN) {

    if (Test-Path $Chemin_MongoDB) {

        Set-Location $Chemin_MongoDB
        Write-Host -BackgroundColor Blue "$(Get-Location)" -ForegroundColor White

        .\mongoimport.exe --uri 'mongodb+srv://dbtytren:Gl2v&di4su$A@cluster0.1z5z20t.mongodb.net/Base_De_donnees_IN' `
            --collection 'Inventaires' --type json --file $Fichier_Inventaires    
    }
}