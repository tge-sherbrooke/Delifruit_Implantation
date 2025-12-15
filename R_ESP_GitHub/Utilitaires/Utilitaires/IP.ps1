# 
$Dossier = "Utilitaires"; 
$FichierCible = "config.json"; $SousFichier = "prewifi.txt"
$AutreSousFichier = "track.txt"
$Interface = "Connexion au réseau local* 13"
$Texte = "Mosquitto"

function ExtraitCibleDeFichier {
    param (
        [string]$Cible,
        [string]$Repository
    )
    $WifiJSON = @()
    $Division = Get-Content $Repository | Select-String -Pattern $Cible
    $SSID = $Division -replace ".*$($Cible)\s*: ?\s*", ""
    
    return $SSID

}

function AppendIIFichiers {
    param (
        [string]$Cible,
        [string]$Disque,
        [string]$Repository = "$($E)\$($Dossier)",
        [string]$AutreFichier
    )

    $E = "$Disque`:"

    Set-Location $E    

    if (Test-Path "$($E)\$($Dossier)\$Cible") {
        <# Action to perform if the condition is true #>
        # Remove-Item "$($E)\$($Dossier)\$Cible"
        Write-Host -ForegroundColor Blue "$(Get-Location)"
    }
    <# $ is the current item #>
    if ( Test-Path "$($E)\$($Dossier)\$Cible") {
        <# Action to perform if the condition is true #>
        Write-Host $fichierD 
        $WifiJSON = Get-Content -raw -Path $Repository | ConvertFrom-Json
        # PAS UTILISEE: pour un texte
        # $SSID = ExtraitCibleDeFichier -Cible "SSID" -Repository $Repository

        # $IP = (Get-NetIPAddress -AddressFamily IPv4 -InterfaceAlias "Connexion au réseau local* 10").IPAddress 
        $IP = (Get-NetIPAddress -AddressFamily IPv4 -InterfaceAlias $Interface).IPAddress 
        $BlockTexte = "$Texte`: $IP"

        $WifiJSON += $BlockTexte

        $WifiJSON | ConvertTo-Json -Depth 10 | Set-Content -Path $Repository -Encoding UTF8
        
        $BlockTexte = "$Texte=$IP"
        $Occurence = Select-String -Path "$($E)\$($Dossier)\$AutreFichier" `
            -Pattern $BlockTexte
        if (-not $Occurence) {
            "$Texte=$IP" | Out-File -FilePath "$($E)\$($Dossier)\$AutreFichier" -Append -Encoding utf8
        }
        
        # C O N V E R S I O N
        $FichierIt = "$($E)\$($Dossier)\$Cible"
        $FichierIIt = "$($E)\$($Dossier)\$AutreFichier"
        $FichierI = Get-Content $FichierIt -Raw
        $FichierII = Get-Content $FichierIIt -Raw
        
        $No_UTF8 = New-Object System.Text.utf8Encoding($false)
        [System.IO.File]::WriteAllText($FichierIt, $FichierI, $No_UTF8)
        [System.IO.File]::WriteAllText($FichierIIt, $FichierII, $No_UTF8)
    }
    
}
function CheckDriver {
    param (
        [string]$Qte = 0,
        [string]$lts = $false,
        [string]$gts = $false, 
        [string]$eqs = $false,
        [Parameter(Mandatory)]
        [string]$Type
    )

    $Volume = (Get-Volume).Size
    
    # Write-Host $Volume 

    foreach ($SizeVolume in $Volume) {
        <# $taille is the current item #>
        if ($Type -eq "MB") {
            <# Action to perform if the condition is true #>
            $Taille = [Math]::Round($SizeVolume / 1MB, 2)
        }
        else {
            <# Action when all if and elseif conditions are false #>
            $Taille = [Math]::Round($SizeVolume / 1GB, 2)
        }
        
        Write-Host $Taille 
        if ($gts -eq $true ) {
            
            Write-Host "gt"

            if ($Taille -gt $Qte) {
                Write-Host "Volume $Taille $Type found"
                                
                $Cible = Get-Volume | Where-Object { $_.Size -eq $SizeVolume } | Select-Object DriveLetter
                $Cible = Get-Volume | Where-Object { $_.Size -eq $SizeVolume } | Select-Object DriveLetter
                $A = $Cible.DriveLetter
                Write-Host $A
                return $A
            }
            else {
                Write-Host "Volume $Taille $Type not found"
            }
            
        }
        elseif ($lts -eq $true ) {
            
            Write-Host "lt"

            if ($Taille -lt $Qte) {
                Write-Host "Volume $Taille $Type found"
                
                $Cible = Get-Volume | Where-Object { $_.Size -eq $SizeVolume } | Select-Object DriveLetter
                $A = $Cible.DriveLetter
                Write-Host $A
                return $A
            }
            else {
                Write-Host "Volume $Taille $Type not found"
            }

        }
        else {

            Write-Host "eq"
            Write-Host "$Qte $Type"

            if ($Taille -eq $Qte) {
                Write-Host "Volume $Taille found"

                $Cible = Get-Volume | Where-Object { $_.Size -eq $SizeVolume } | Select-Object DriveLetter
                $A = $Cible.DriveLetter
                Write-Host $A
                return $A
            }
            else {
                Write-Host "Volume $Taille $Type not found"
            }
        }
    }
}

#
$ORDI_1 = CheckDriver -Qte "96.45" -Type "GB" -eqs $true 
#
$ORDI_2 = CheckDriver -Qte "306.76" -Type "GB" -eqs $true 
#
$DisqueSource = CheckDriver -Qte "14" -Type "MB" -lts $true 

if ($ORDI_1) {
    Write-Host "ORDI_1 : $ORDI_1`:/"
} else {
    Write-Host "ORDI_1 : N'existe pas."
}
if ($ORDI_2) {
    Write-Host "ORDI_2 : $ORDI_2`:/"
} else {
    Write-Host "ORDI_2 : N'existe pas."
}
if ($DisqueSource) {
    Write-Host "DisqueSource : $DisqueSource`:/"
} else {
    Write-Host "DisqueSource : Non trouvé."
}



if (($ORDI_1 -ne $null) -and ($DisqueSource -ne $null)) {
    
    AppendIIFichiers -Disque $DisqueSource -Cible $FichierCible `
        -Repository "$($DisqueSource)\$($Dossier)\$($FichierCible)" -AutreFichier $AutreSousFichier
}

elseif (($ORDI_2 -ne $null) -and ($DisqueSource -ne $null)) {
    
    AppendIIFichiers -Disque $DisqueSource -Cible $FichierCible `
        -Repository "$($E)\$($Dossier)\$($FichierCible)" -AutreFichier $AutreSousFichier

}
else {
    Write-Host "Impossible d'effectuer la tache : 1 ou 2 des 3 disques est manquant..."
}