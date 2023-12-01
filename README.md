# Melissa - Global Address Object Windows Python3

## Purpose

This code showcases the Melissa Global Address Object using Python3.

Please feel free to copy or embed this code to your own project. Happy coding!

For the latest Melissa Global Address Object release notes, please visit: https://releasenotes.melissa.com/on-premise-api/global-address-object/

The console will ask the user for:

- Address Line 1
- Address Line 2
- Address Line 3
- Locality
- Administrative Area
- Postal Code
- Country

And return 

- Melissa Address Key (MAK)
- Company
- Address Line 1
- Address Line 2
- Address Line 3
- Address Line 4
- Address Line 5
- Locality
- Administrative Area
- Postal Code
- Postbox
- Country
- Country ISO 2
- Country ISO 3
- Latitude
- Longitude
- Formatted Address
- Result Codes

## Tested Environments

- Windows 10 64-bit Python 3.8.7, Powershell 5.1
- Melissa data files for 2023-Q4

## Required File(s) and Programs

#### Binaries

This is the c++ code of the Melissa Object.

- mdAddr.dll
- mdGeo.dll
- mdGlobalAddr.dll
- mdRightFielder.dll


#### Data File(s)
- Addr.dbf
- Congress.csv
- dph256.dte
- dph256.hsa
- dph256.hsc
- dph256.hsd
- dph256.hsf
- dph256.hsn
- dph256.hsp
- dph256.hsr
- dph256.hst
- dph256.hsu
- dph256.hsv
- dph256.hsx
- dph256.hsy
- dph256.hsz
- ews.txt
- icudt52l.dat
- lcd256
- mdAddr.dat
- mdAddr.lic
- mdAddr.nat
- mdAddr.str
- mdAddrKey.db
- mdAddrKeyCA.db
- mdCanada3.db
- mdCanadaPOC.db
- mdGeoCode.db3
- mdGlobalAddr.ffbb
- mdGlobalAddr.ffhb
- mdGlobalAddr.ffpl
- mdGlobalAddr.ffps
- mdGlobalAddr.ffst
- mdGlobalAddr.sac
- mdLACS256.dat
- mdRBDI.dat
- mdRightFielder.cfg
- mdRightFielder.dat
- mdSteLink256.dat
- mdSuiteFinder.db
- month256.dat

## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

This project is compatible with Python3

#### Install Python3
Before starting, make sure that Python3 has been correctly installed on your machine and your environment paths are configured. 

You can download Python here: 
https://www.python.org/downloads/

To set up your Path to correctly to use the python3 command, execute the following steps:
1) Run Powershell as an administrator 
2) Execute the command: 
`New-Item -ItemType SymbolicLink -Path "Link" -Target "Target"`

    where "Target" is the path to py.exe (by default this should be "C:\Windows\py.exe")\
    and "Link" is the path to py.exe, but "py.exe" is replaced with "python3.exe"\
    For Example:\
    `New-Item -ItemType SymbolicLink -Path "C:\Windows\python3.exe" -Target "C:\Windows\py.exe"`

If you are unsure, you can check by opening a command prompt window and typing the following:
`python3 --version`

![alt text](/screenshots/python_version.PNG)

If you see the version number then you have installed Python3 and set up your environment paths correctly!

----------------------------------------


#### Set up Powershell settings

If running Powershell for the first time, you will need to run this command in the Powershell console: `Set-ExecutionPolicy RemoteSigned`.
The console will then prompt you with the following warning shown in the image below. 
 - Enter `'A'`. 
 	- If successful, the console will not output any messages. (You may need to run Powershell as administrator to enforce this setting).
	
 ![alt text](/screenshots/powershell_executionpolicy.png)

----------------------------------------

#### Download this project
```
$ git clone https://github.com/MelissaData/GlobalAddressObject-Python3
$ cd GlobalAddressObject-Python3
```

#### Set up Melissa Updater 

Melissa Updater is a CLI application allowing the user to update their Melissa applications/data. 

- Download Melissa Updater here: <https://releases.melissadata.net/Download/Library/WINDOWS/NET/ANY/latest/MelissaUpdater.exe>
- Create a folder within the cloned repo called `MelissaUpdater`.
- Put `MelissaUpdater.exe` in `MelissaUpdater` folder you just created.

----------------------------------------

#### Different ways to get data file(s)
1.  Using Melissa Updater
	- It will handle all of the data download/path and dll(s) for you. 
	- **Please be aware that this object will require about 100GB of memory.**
2.  If you already have the latest GDQS Release (ZIP), you can find the data file(s) and dll(s) in there
	- Use the location of where you copied/installed the data and update the "$DataPath" variable in the powershell script.
	- Copy all the dll(s) mentioned above into the `MelissaGlobalAddressObjectWindowsPython3` project folder.
	
----------------------------------------

## Run Powershell Script

Please consult the release notes and wiki for the best way to input the parameters.

Release Notes: https://releasenotes.melissa.com/on-premise-api/global-address-object/

Wiki: https://wiki.melissadata.com/index.php?title=Result_Code_Details#Global_Address_Object

Parameters:
- -addressLine1: a test address line 1
- -addressLine2 (optional): a test address line 2
- -addressLine3 (optional): a test address line 3
- -locality: a test locality
- -administrativeArea: a test administrative area
- -postalCode: a test postal code
- -country: a test country
 	
  These are convenient when you want to get results for a specific address in one run instead of testing multiple addresses in interactive mode.

- -license (optional): a license string to test the Global Address Object
- -quiet (optional): add to the command if you do not want to get any console output from the Melissa Updater

When you have modified the script to match your data location, let's run the script. There are two modes:
- Interactive 

	The script will prompt the user for an address line 1, address line 2, address line 3, locality, administrative area, postal code, and country, then use the provided inputs to test Global Address Object. For example:
	```
	$ .\MelissaGlobalAddressObjectWindowsPython3.ps1
	```
	For quiet mode:
	```
	$ .\MelissaGlobalAddressObjectWindowsPython3.ps1 -quiet
	```
- Command Line 

	You can pass an address line 1, address line 2, address line 3, locality, administrative area, postal code, country, and a license string into the ```-addressLine1```, ```-addressLine2```, ```-addressLine3```, ```-locality```, ```-administrativeArea```, ```-postalCode```, ```-country```, and ```-license``` parameters respectively to test Global Address Object. For example:

	```
	$ .\MelissaGlobalAddressObjectWindowsPython3.ps1 -addressLine1 "Melissa Data GmbH" -addressLine2 "Cäcilienstr. 42-44" -addressLine3 "50667 Köln" -country "Germany" 
	$ .\MelissaGlobalAddressObjectWindowsPython3.ps1 -addressLine1 "Melissa Data GmbH" -addressLine2 "Cäcilienstr. 42-44" -addressLine3 "50667 Köln" -country "Germany" -license "<your_license_string>"
	```

	For quiet mode:
	```
	$ .\MelissaGlobalGlobalAddressObjectWindowsPython3.ps1 -addressLine1 "Melissa Data GmbH" -addressLine2 "Cäcilienstr. 42-44" -addressLine3 "50667 Köln" -country "Germany" -quiet
	$ .\MelissaGlobalGlobalAddressObjectWindowsPython3.ps1 -addressLine1 "Melissa Data GmbH" -addressLine2 "Cäcilienstr. 42-44" -addressLine3 "50667 Köln" -country "Germany" -license "<your_license_string>" -quiet
	```

This is the expected output from a successful setup for interactive mode:

![alt text](/screenshots/output.PNG)

    
## Troubleshooting

Troubleshooting for errors found while running your program.

### Errors:

| Error      | Description |
| ----------- | ----------- |
| ErrorRequiredFileNotFound      | Program is missing a required file. Please check your Data folder and refer to the list of required files above. If you are unable to obtain all required files through the Melissa Updater, please contact technical support below. |
| ErrorDatabaseExpired   | .db file(s) are expired. Please make sure you are downloading and using the latest release version. (If using the Melissa Updater, check powershell script for '$RELEASE_VERSION = {version}'  and change the release version if you are using an out of date release).     |
| ErrorFoundOldFile   | File(s) are out of date. Please make sure you are downloading and using the latest release version. (If using the Melissa Updater, check powershell script for '$RELEASE_VERSION = {version}'  and change the release version if you are using an out of date release).    |
| ErrorLicenseExpired   | Expired license string. Please contact technical support below. |


## Contact Us

For free technical support, please call us at 800-MELISSA ext. 4
(800-635-4772 ext. 4) or email us at tech@melissa.com.

To purchase this product, contact Melissa sales department at
800-MELISSA ext. 3 (800-635-4772 ext. 3).
