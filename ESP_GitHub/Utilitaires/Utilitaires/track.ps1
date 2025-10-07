
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
        } else {
            <# Action when all if and elseif conditions are false #>
            $Taille = [Math]::Round($SizeVolume / 1GB, 2)
        }
        
        Write-Host $Taille 
        if ($gts -eq $true ) {
            
            Write-Host "gt"

            if ($Taille -gt $Qte) {
                # Write-Host "Volume $Taille $Type found"
                                
                $Cible = Get-Volume | Where-Object { $_.Size -eq $SizeVolume } | Select-Object DriveLetter
                $Cible = Get-Volume | Where-Object { $_.Size -eq $SizeVolume } | Select-Object DriveLetter
                $A = $Cible.DriveLetter
                Write-Host $A
                return $A
            }
            else {
                # Write-Host "Volume $Taille $Type not found"
            }
            
        }
        elseif ($lts -eq $true ) {
            
            Write-Host "lt"

            if ($Taille -lt $Qte) {
                # Write-Host "Volume $Taille $Type found"
                
                $Cible = Get-Volume | Where-Object { $_.Size -eq $SizeVolume } | Select-Object DriveLetter
                $A = $Cible.DriveLetter
                Write-Host $A
                return $A
            }
            else {
                # Write-Host "Volume $Taille $Type not found"
            }

        }
        else {

            Write-Host "eq"
            Write-Host "$Qte $Type"

            if ($Taille -eq $Qte) {
                # Write-Host "Volume $Taille found"

                $Cible = Get-Volume | Where-Object { $_.Size -eq $SizeVolume } | Select-Object DriveLetter
                $A = $Cible.DriveLetter
                Write-Host $A
                return $A
            }
            else {
                # Write-Host "Volume $Taille $Type not found"
            }
        }
    }
}




#
$ORDI_1 = CheckDriver -Qte "96.45" -Type "GB" -eqs $true 
#
$ORDI_2 = CheckDriver -Qte "192.68" -Type "GB" -eqs $true 
Set-Location $PSScriptRoot
Get-Location
if ($null -ne $ORDI_1){
    "TRACKING=$($ORDI_1)" | Set-Content -Path ".\track.txt"
        Write-Host -ForegroundColor Green  "Ecriture reussi."
} else {
    "TRACKING=$($ORDI_2)" | Set-Content -Path ".\track.txt"
}
Write-Host -ForegroundColor Yellow "Ecriture dans track.txt"




# Traceback (appels les plus récents en dernier) :
#   Fichier "code.py", ligne 8, dans <module>
#   Fichier "main.py", ligne 17, dans <module>
#   Fichier "/lib/_MQTT_.py", ligne 219, dans <module>
#   Fichier "/lib/_MQTT_.py", ligne 39, dans TempsP
#   Fichier "/lib/_MQTT_.py", ligne 110, dans UTC_heure
#   Fichier "/lib/_MQTT_.py", ligne 99, dans conversion_heure
# OverflowError: timestamp hors intervalle pour le 'time_t' de la plateforme