#
$Date = Get-Date -Format "yyyy-MM-dd_HH-mm-ss" 

$Dossiers = @("Utilitaires", "lib", "Others")

$Fichiers = @("Code.py", "settings.toml", "_Main_.py", "CopyFichiersDossiers.ps1")
# Get-Volume | Where-Object { $_.Size -eq "D" } | Copy-Item -Destination "C:\Temp" -Recurse -Force

function CheckDriver {
    param (
        [string]$Qte = 0,
        [string]$lts = $false,
        [string]$gts = $false, 
        [string]$eqs = $false,
        [Parameter(Mandatory)][string]$Type
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
 
    $Objectif = "$env:backupesp"
    if (!$Objectif) {
        Write-Host -ForegroundColor Red "Chemin de transfert introuvable. Veuillez préciser le lieu de la sauvegarde de votre travail..."
        $Objectif = Read-Host -Prompt ""
    } 
    $GitDeposit = "$env:gitesp"
    if (!$GitDeposit) {
        Write-Host -ForegroundColor Red "Chemin de transfert introuvable. Veuillez préciser le lieu de la sauvegarde de votre travail..."
        $GitDeposit = Read-Host -Prompt ""
    } 

    Set-Location "$DisqueSource`:\"

    $Objets = Get-ChildItem -Path "$DisqueSource`:\"

    foreach ($Element in $Objets) {
        # Write-Host $Element

        foreach ($files in $Dossiers) {

            if ("$Element" -eq "$files") {
                
                Copy-Item "$files" -Destination "$($Objectif)\code_$($Date)\$files" -Recurse -Force
                Copy-Item "$files" -Destination "$($GitDeposit)\$files" -Recurse -Force
                Write-Host "$files envoyees"
            } 
        }

        foreach ($file in $Fichiers) {

            if ("$Element" -eq "$file") {
                Copy-Item $file -Destination "$($Objectif)\code_$($Date)\" -Force
                Copy-Item "$files" -Destination "$($GitDeposit)" -Force
                Write-Host "$file envoyees"
            } 
        }
    }

} 

elseif (($ORDI_2 -ne $null) -and ($DisqueSource -ne $null)) {
    $Objectif = "$env:backupesp"
    if (($null -eq $Objectif) -or (-not (Test-Path "$Objectif"))) {
        Write-Host -ForegroundColor Red "Chemin de transfert BACKUP introuvable. Veuillez préciser le lieu de la sauvegarde de votre travail... Ou vous pourriez éditer le script afin de conserver définitivement votre répertoire"
        $Objectif = Read-Host -Prompt "Dossier "
    } 
    $GitDeposit = "$env:gitesp"
    if (($null -eq $GitDeposit) -or (-not (Test-Path "$GitDeposit"))) {
        Write-Host -ForegroundColor Red "Chemin de transfert DEPOT GITHUB introuvable. Veuillez préciser le lieu de la sauvegarde de votre travail... Ou vous pourriez éditer le script afin de conserver définitivement votre répertoire"
        $GitDeposit = Read-Host -Prompt "Dossier "
    } 

    Set-Location "$DisqueSource`:\"

    $Objets = Get-ChildItem -Path "$DisqueSource`:\"

    foreach ($Element in $Objets) {
        # Write-Host $Element

        foreach ($files in $Dossiers) {

            if ("$Element" -match "$files") {
                
                Copy-Item "$files" -Destination "$($Objectif)\code_$($Date)\$files" -Recurse -Force
                Copy-Item "$files" -Destination "$($GitDeposit)\$files" -Recurse -Force
                Write-Host "$files envoyés"
            } 
        }

        foreach ($file in $Fichiers) {

            if ("$Element" -match "$file") {
                Copy-Item $file -Destination "$($Objectif)\code_$($Date)\" -Force
                Copy-Item "$file" -Destination "$($GitDeposit)\" -Force
                Write-Host "$file envoyés"
            } 
        }
    }

}
else {
    Write-Host "Impossible d'effectuer la tache : 1 ou 2 des 3 disques est manquant..."
}

































# function CheckDriver {
#     param (
#         [string]$Qte = 0,
#         [string]$lts=$false,
#         [string]$gts=$false, 
#         [string]$eqs=$false 
#     )

#     $Volume = (Get-Volume).Size

#     foreach ($Taille in $Volume) {
#         <# $taille is the current item #>
#         $Taille = $Taille / 1MB

#         if ($gts -eq $true ) {
            
#             Write-Host "gt"

#             if ($Taille -gt $Qte) {
#                 Write-Host "Volume $Taille found"
#                 $Taille = $Taille * 1MB
#                 $Cible = Get-Volume | Where-Object { $_.Size -eq $Taille } | Select-Object DriveLetter
#                 $Cible = Get-Volume | Where-Object { $_.Size -eq $Taille } | Select-Object DriveLetter
#                 $A = $Cible.DriveLetter
#                 Write-Host $A
#                 return $A
#             } else {
#                 Write-Host "Volume $Taille not found"
#             }
            
#         } elseif ($lts -eq $true ) {
            
#              Write-Host "lt"

#             if ($Taille -lt $Qte) {
#                 Write-Host "Volume $Taille found"
#                 $Taille = $Taille * 1MB
#                 $Cible = Get-Volume | Where-Object { $_.Size -eq $Taille } | Select-Object DriveLetter
#                 $A = $Cible.DriveLetter
#                 Write-Host $A
#                 return $A
#             } else {
#                 Write-Host "Volume $Taille not found"
#             }

#         } else {

#             Write-Host "eq"
#             Write-Host $Qte

#             if ($Taille -eq $Qte) {
#                 Write-Host "Volume $Taille found"
#                 $Taille = $Taille * 1MB
#                 $Cible = Get-Volume | Where-Object { $_.Size -eq $Taille } | Select-Object DriveLetter
#                 $A = $Cible.DriveLetter
#                 Write-Host $A
#                 return $A
#             } else {
#                 Write-Host "Volume not found"
#                 exit
#             }
#         }
#     }
# }
    

# $Disque = CheckDriver -Qte "14" -lts $true