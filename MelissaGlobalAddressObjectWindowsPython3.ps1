<#
.SYNOPSIS
    Downloads the required components and then runs MelissaGlobalAddressObjectWindowsPython3

.DESCRIPTION
    This script uses the Melissa Updater to fetch the data file(s) and DLL(s),
    verifies the DLL(s) downloaded, then runs the Python script against the supplied address.

    Overall flow:
      1. Read parameters / prompt for the license and data path.
      2. Download data file(s) and DLL(s) via the Melissa Updater.
      3. Confirm the DLL(s) are present.
      4. Run the script (single test address or interactive).

.PARAMETER addressLine1
    First address line of the address to verify.

.PARAMETER addressLine2
    Second address line of the address to verify.

.PARAMETER addressLine3
    Third address line of the address to verify.

.PARAMETER locality
    Locality (city) of the address to verify.

.PARAMETER administrativeArea
    Administrative area (state/province) of the address to verify.

.PARAMETER postalCode
    Postal code of the address to verify.

.PARAMETER country
    Country of the address to verify.

.PARAMETER dataPath
    Path to an existing data files directory. If omitted, the script prompts for
    a path; pressing Enter at that prompt skips it and downloads the data files
    into the project's Data folder via the Melissa Updater. A path that does not
    exist aborts the script.

.PARAMETER license
    License string. Resolved in this order:
      1. This parameter.
      2. An interactive prompt, if the parameter was not supplied.
      3. The MD_LICENSE environment variable, if the prompt was left blank.
    Note that the environment variable is the last resort, not the first: running
    without -license always prompts, even when MD_LICENSE is set.

.PARAMETER quiet
    Suppresses the Melissa Updater console output during downloads.

.EXAMPLE
    .\MelissaGlobalAddressObjectWindowsPython3.ps1 -license "your-license"

.EXAMPLE
    .\MelissaGlobalAddressObjectWindowsPython3.ps1 -addressLine1 "Melissa Data GmbH" -addressLine2 "Cäcilienstr. 42-44" -addressLine3 "50667 Köln" -country "Germany" -license "your-license"
#>

######################### Parameters ##########################

param(
  $addressLine1 = '""',
  $addressLine2 = '""',
  $addressLine3 = '""',
  $locality = '""',
  $administrativeArea = '""',
  $postalCode = '""',
  $country = '""',
  $dataPath = '',
  $license = '',
  [switch]$quiet = $false
)

######################### Classes ##########################

# Describes a single file to request from the Melissa Updater
class FileConfig {
  [string] $FileName;
  [string] $ReleaseVersion;
  [string] $OS;
  [string] $Compiler;
  [string] $Architecture;
  [string] $Type;
}

######################### Config ###########################

# Product release the updater pulls files for
$RELEASE_VERSION = '2026.Q3'
$ProductName = "GLOBAL_DQ_DATA"

# Uses the location of the .ps1 file 
$CurrentPath = $PSScriptRoot
Set-Location $CurrentPath
$ProjectPath = "$CurrentPath\MelissaGlobalAddressObjectWindowsPython3"

if ([string]::IsNullOrEmpty($dataPath)) {
  $DataPath = "$ProjectPath\Data" 
}

if (!(Test-Path $DataPath) -and ($DataPath -eq "$ProjectPath\Data")) {
  New-Item -Path $ProjectPath -Name 'Data' -ItemType "directory"
}
elseif (!(Test-Path $DataPath) -and ($DataPath -ne "$ProjectPath\Data")) {
  Write-Host "`nData file path does not exist. Please check that your file path is correct."
  Write-Host "`nAborting program, see above.  Press any button to exit.`n"
  $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown") > $null
  exit
}

# Binary/DLL(s) needed to run the example
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

# Python wrapper source that exposes the DLL to the script
$Wrapper = [FileConfig]@{
  FileName       = "mdGlobalAddr_pythoncode.py";
  ReleaseVersion = $RELEASE_VERSION;
  OS             = "ANY";
  Compiler       = "PYTHON";
  Architecture   = "ANY" ;
  Type           = "INTERFACE"
}

######################## Functions #########################

# Download the product data file(s) into $DataPath via the Melissa Updater.
function DownloadDataFiles([string] $license) {
  Write-Host "`n=============================== MELISSA UPDATER ============================="
  Write-Host "MELISSA UPDATER IS DOWNLOADING DATA FILE(S)..."

  .\MelissaUpdater\MelissaUpdater.exe manifest -p $ProductName -r $RELEASE_VERSION -l $license -t $DataPath 
  if($? -eq $False ) {
    Write-Host "`nCannot run Melissa Updater. Please check your license string!"
    Exit
  }     

  Write-Host "Melissa Updater finished downloading data file(s)!"
}

# Download each DLL in $DLLs into the project folder (with a progress bar).
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


# Download the Python wrapper source into the project folder.
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


# Verify the expected DLL(s) landed in the project folder
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
  $License = $env:MD_LICENSE 
}

if ([string]::IsNullOrEmpty($License)) {
  Write-Host "`nLicense String is invalid!"
  Exit
}

# Get data file path (either from parameters or user input)
if ($DataPath -eq "$ProjectPath\Data") {
  $dataPathInput = Read-Host "Please enter your data files path directory if you have already downloaded the release zip.`nOtherwise, the data files will be downloaded using the Melissa Updater (Enter to skip)"

  if (![string]::IsNullOrEmpty($dataPathInput)) {
    if (!(Test-Path $dataPathInput)) {
      Write-Host "`nData file path does not exist. Please check that your file path is correct."
      Write-Host "`nAborting program, see above.  Press any button to exit.`n"
      $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown") > $null
      exit
    }
    else {
      $DataPath = $dataPathInput
    }
  }
}

# Use Melissa Updater to download data file(s) 
# Download data file(s) 
DownloadDataFiles -license $License # Comment out this line if using own release

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
# No address supplied -> run interactively; otherwise pass the address in.
# Push-Location switches into the project folder first so the script and wrapper resolve.
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
