# Name:    MelissaGlobalAddressObjectWindowsPython3
# Purpose: Use the Melissa Updater to make the MelissaAddressObjectWindowsPython3 code usable

######################### Parameters ##########################

param(
  $addressLine1 = '""',
  $addressLine2 = '""',
  $addressLine3 = '""',
  $locality = '""',
  $administrativeArea = '""',
  $postalCode = '""',
  $country = '""',
  $license = '',
  [switch]$quiet = $false
)

######################### Classes ##########################

class FileConfig {
  [string] $FileName;
  [string] $ReleaseVersion;
  [string] $OS;
  [string] $Compiler;
  [string] $Architecture;
  [string] $Type;
}

class ManifestConfig {
  [string] $ManifestName;
  [string] $ReleaseVersion;
}

######################### Config ###########################

$RELEASE_VERSION = '2023.Q4'

# Uses the location of the .ps1 file 
# Modify this if you want to use 
$CurrentPath = $PSScriptRoot
Set-Location $CurrentPath
$ProjectPath = "$CurrentPath\MelissaGlobalAddressObjectWindowsPython3"
$DataPath = "$ProjectPath\Data"

If (!(Test-Path $DataPath)) {
  New-Item -Path $ProjectPath -Name 'Data' -ItemType "directory"
}

$DLLs = @(
  [FileConfig]@{
    FileName       = "mdAddr.dll";
    ReleaseVersion = $RELEASE_VERSION;
    OS             = "WINDOWS";
    Compiler       = "DLL";
    Architecture   = "64BIT";
    Type           = "BINARY";
  },
  [FileConfig]@{
    FileName       = "mdGeo.dll";
    ReleaseVersion = $RELEASE_VERSION;
    OS             = "WINDOWS";
    Compiler       = "DLL";
    Architecture   = "64BIT";
    Type           = "BINARY";
  },
  [FileConfig]@{
    FileName       = "mdGlobalAddr.dll";
    ReleaseVersion = $RELEASE_VERSION;
    OS             = "WINDOWS";
    Compiler       = "DLL";
    Architecture   = "64BIT";
    Type           = "BINARY";
  },
  [FileConfig]@{
    FileName       = "mdRightFielder.dll";
    ReleaseVersion = $RELEASE_VERSION;
    OS             = "WINDOWS";
    Compiler       = "DLL";
    Architecture   = "64BIT";
    Type           = "BINARY";
  }
)

$Wrapper = [FileConfig]@{
  FileName       = "mdGlobalAddr_pythoncode.py";
  ReleaseVersion = $RELEASE_VERSION;
  OS             = "ANY";
  Compiler       = "PYTHON";
  Architecture   = "ANY" ;
  Type           = "INTERFACE"
}


$Manifests = @(
  [ManifestConfig]@{
    ManifestName   = "global_dq_data";
    ReleaseVersion = $RELEASE_VERSION;
  }
)

######################## Functions #########################

function DownloadDataFiles([string] $license) {
  $DataProg = 0
  Write-Host "`n=============================== MELISSA UPDATER ============================="
  Write-Host "MELISSA UPDATER IS DOWNLOADING DATA FILE(S)..."

  foreach ($Manifest in $Manifests) {
    Write-Progress -Activity "Downloading Manifest(s)" -Status "$([math]::round($DataProg / $Manifests.Count * 100, 2))% Complete:"  -PercentComplete ($DataProg / $Manifests.Count * 100)
	
    .\MelissaUpdater\MelissaUpdater.exe manifest -p $Manifest.ManifestName -r $Manifest.ReleaseVersion -l $license -t $DataPath 
    if ($? -eq $False ) {
      Write-Host "`nCannot run Melissa Updater. Please check your license string!"
      Exit
    } 	    
  }

  Write-Host "Melissa Updater finished downloading data file(s)!"
}

function DownloadDLLs() {
  Write-Host "MELISSA UPDATER IS DOWNLOADING DLL(s)..."
  $DLLProg = 0
  foreach ($DLL in $DLLs) {
    Write-Progress -Activity "Downloading DLL(s)" -Status "$([math]::round($DLLProg / $DLLs.Count * 100, 2))% Complete:"  -PercentComplete ($DLLProg / $DLLs.Count * 100)

    # Check for quiet mode
    if ($quiet) {
      .\MelissaUpdater\MelissaUpdater.exe file --filename $DLL.FileName --release_version $DLL.ReleaseVersion --license $LICENSE --os $DLL.OS --compiler $DLL.Compiler --architecture $DLL.Architecture --type $DLL.Type --target_directory $ProjectPath > $null
      if (($?) -eq $False) {
        Write-Host "`nCannot run Melissa Updater. Please check your license string!"
        Exit
      }
    }
    else {
      .\MelissaUpdater\MelissaUpdater.exe file --filename $DLL.FileName --release_version $DLL.ReleaseVersion --license $LICENSE --os $DLL.OS --compiler $DLL.Compiler --architecture $DLL.Architecture --type $DLL.Type --target_directory $ProjectPath 
      if (($?) -eq $False) {
        Write-Host "`nCannot run Melissa Updater. Please check your license string!"
        Exit
      }
    }
    
    Write-Host "Melissa Updater finished downloading " $DLL.FileName "!"
    $DLLProg++
  }
}


function DownloadWrapper() {
  Write-Host "MELISSA UPDATER IS DOWNLOADING WRAPPER(S)..."

  # Check for quiet mode
  if ($quiet) {
    .\MelissaUpdater\MelissaUpdater.exe file --filename $Wrapper.FileName --release_version $Wrapper.ReleaseVersion --license $LICENSE --os $Wrapper.OS --compiler $Wrapper.Compiler --architecture $Wrapper.Architecture --type $Wrapper.Type --target_directory $ProjectPath > $null
    if (($?) -eq $False) {
      Write-Host "`nCannot run Melissa Updater. Please check your license string!"
      Exit
    }
  }
  else {
    .\MelissaUpdater\MelissaUpdater.exe file --filename $Wrapper.FileName --release_version $Wrapper.ReleaseVersion --license $LICENSE --os $Wrapper.OS --compiler $Wrapper.Compiler --architecture $Wrapper.Architecture --type $Wrapper.Type --target_directory $ProjectPath 
    if (($?) -eq $False) {
      Write-Host "`nCannot run Melissa Updater. Please check your license string!"
      Exit
    }
  }

  Write-Host "Melissa Updater finished downloading " $Wrapper.FileName "!"
}


function CheckDLLs() {
  Write-Host "`nDouble checking dll(s) were downloaded...`n"
  $FileMissing = $false 
  if (!(Test-Path ("$ProjectPath\mdAddr.dll"))) {
    Write-Host "mdAddr.dll not found." 
    $FileMissing = $true
  }
  if (!(Test-Path ("$ProjectPath\mdGeo.dll"))) {
    Write-Host "mdGeo.dll not found." 
    $FileMissing = $true
  }
  if (!(Test-Path ("$ProjectPath\mdGlobalAddr.dll"))) {
    Write-Host "mdGlobalAddr.dll not found." 
    $FileMissing = $true
  }
  if (!(Test-Path ("$ProjectPath\mdRightFielder.dll"))) {
    Write-Host "mdRightFielder.dll not found." 
    $FileMissing = $true
  }
  if ($FileMissing) {
    Write-Host "`nMissing the above data file(s).  Please check that your license string and directory are correct."
    return $false
  }
  else {
    return $true
  }
}

########################## Main ############################
Write-Host "`n======================= Melissa Global Address Object =======================`n                    	[ Python3 | Windows | 64BIT ]`n"

# Get license (either from parameters or user input)
if ([string]::IsNullOrEmpty($license) ) {
  $License = Read-Host "Please enter your license string"
}

# Check for License from Environment Variables 
if ([string]::IsNullOrEmpty($License) ) {
  $License = $env:MD_LICENSE # Get-ChildItem -Path Env:\MD_LICENSE   #[System.Environment]::GetEnvironmentVariable('MD_LICENSE')
}

if ([string]::IsNullOrEmpty($License)) {
  Write-Host "`nLicense String is invalid!"
  Exit
}
# Use Melissa Updater to download data file(s) 
# Download data file(s) 
DownloadDataFiles -license $License      # comment out this line if using DQS Release

# Set data file(s) path
# $DataPath = "C:\Program Files\Melissa DATA\DQT\Data"      # uncomment this line and change to your DQS Release data file(s) directory 

# Download dll(s)
DownloadDlls -license $License

# Check if all dll(s) have been downloaded. Exit script if missing
$DLLsAreDownloaded = CheckDLLs
if (!$DLLsAreDownloaded) {
  Write-Host "`nAborting program, see above.  Press any button to exit."
  $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
  exit
}

Write-Host "All file(s) have been downloaded/updated! "

# Start
# Run project
if ([string]::IsNullOrEmpty($addressLine1) -and [string]::IsNullOrEmpty($addressLine2) -and [string]::IsNullOrEmpty($addressLine3) -and [string]::IsNullOrEmpty($locality) -and [string]::IsNullOrEmpty($administrativeArea) -and [string]::IsNullOrEmpty($postalCode) -and [string]::IsNullOrEmpty($country)) {
  Push-Location MelissaGlobalAddressObjectWindowsPython3
  python3 MelissaGlobalAddressObjectWindowsPython3.py --license $License  --dataPath $DataPath
  Pop-Location
}
else {
  Push-Location MelissaGlobalAddressObjectWindowsPython3
  python3 MelissaGlobalAddressObjectWindowsPython3.py --license $License  --dataPath $DataPath --addressLine1 $addressLine1 --addressLine2 $addressLine2 --addressLine3 $addressLine3 --locality $locality --administrativeArea $administrativeArea --postalCode $postalCode --country $country
  Pop-Location
}
