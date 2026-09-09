"""
Global Address Object corrects, verifies, and enhances Global addresses from over 250+
countries and territories. International address data quality is a challenge for
organizations of all sizes. Its differing address structures, terms, and alphabets can
have a substantial negative impact on your data-driven initiatives if handled poorly. By
using Global Address Object, you'll reduce undeliverables, increase communication efforts,
and save money on all your marketing campaigns.

High-level flow of this sample:
  1. SETUP     - create an mdGlobalAddr instance, hand it the license string and the
                 path to the data files, then InitializeDataFiles() (one time).
  2. INPUT     - set the address fields via SetInputParameter("input...", ...).
  3. PROCESS   - VerifyAddress() validates and standardizes the address.
  4. READ      - pull the corrected fields back out with GetOutputParameter("...")
                 (formattedAddress, latitude, iso2Code, MAK, ...).
  5. INTERPRET - GetOutputParameter("resultCodes") returns comma-separated result
                 codes describing what the object did/found.

This object uses the name/value parameter API: inputs are supplied by name with
SetInputParameter("input...", value) and every result - including the result codes - is
read back by name with GetOutputParameter("..."), rather than the dedicated Get* getters
and GetResults() used by some other Melissa objects.

The pieces in this file map onto that flow:
  - run_as_console / parse_arguments : console harness (argument parsing + the interactive loop).
  - GlobalAddressObject              : thin wrapper around mdGlobalAddr (setup + the call sequence).
  - DataContainer                    : holds one record's input fields, plus a small request filter.

Where mdGlobalAddr comes from:
  The mdGlobalAddr class lives in mdGlobalAddr_pythoncode.py, a generated Python wrapper
  over mdGlobalAddr.dll, which the accompanying
  MelissaGlobalAddressObjectWindowsPython3.ps1 script downloads alongside mdAddr.dll,
  mdGeo.dll, and mdRightFielder.dll.

Reference:
  Quickstart    : https://docs.melissa.com/on-premise-api/global-address-object/global-address-object-quickstart.html
  Release notes : https://releasenotes.melissa.com/on-premise-api/global-address-object/
  Result codes  : https://docs.melissa.com/on-premise-api/global-address-object/result-codes.html
"""

import mdGlobalAddr_pythoncode
import sys


class DataContainer:
    """
    Holds one record's input address fields, plus a small pre-processing filter
    (filter_request) the wrapper calls before sending the data to the object.
    """
    def __init__(self, addressLine1="", addressLine2="", addressLine3="", locality="", administrative_area="", postal_code="", country="", result_codes=[]):
        # Input: the first address line to process.
        self.addressLine1 = addressLine1

        # Input: the second address line to process.
        self.addressLine2 = addressLine2

        # Input: the third address line to process.
        self.addressLine3 = addressLine3

        # Input: the locality (city) to process.
        self.locality = locality

        # Input: the administrative area (state/province) to process.
        self.administrative_area = administrative_area

        # Input: the postal code to process.
        self.postal_code = postal_code

        # Input: the country to process.
        self.country = country

        # Output: comma-separated result codes (this sample reads them via GetOutputParameter).
        self.result_codes = result_codes

    def filter_request(self):
            """
            Drop an address line that merely repeats the locality / administrative area /
            postal code (an "area stack"), so those values are not sent to the object twice.
            If either address line 2 or address line 3 contains the area stack information
            (locality, admin area, and postal code) then erase that address line.
            """
            if self.check_for_area_stack(self.addressLine3):
                self.addressLine3 = ""
            elif self.check_for_area_stack(self.addressLine2):
                self.addressLine3 = ""
                self.addressLine2 = ""

    def check_for_area_stack(self, address_line):
        """
        Return True when the given address line contains the locality, administrative
        area, and postal code all at once - i.e. it is a redundant "area stack" line.
        """
        localityCheck = False
        adminAreaCheck = False
        postalCheck = False

        if self.locality in address_line and self.locality != "":
            localityCheck = True
        if self.administrative_area in address_line and self.administrative_area != "":
            adminAreaCheck = True
        if self.postal_code in address_line and self.postal_code != "":
            postalCheck = True

        if localityCheck and adminAreaCheck and postalCheck:
            return True

        return False

    

class GlobalAddressObject:
    """
    Wrapper that owns a single Melissa Global Address Object instance and encapsulates the
    two things every Melissa object needs: one-time setup (license + data files) and the
    per-record processing sequence. Reuse one instance across many addresses; do NOT
    re-initialize per address.
    """

    def __init__(self, license, data_path):
        """
        Perform the mandatory one-time setup. Both of the first two calls must happen
        before the third; this sample sets the data-file path before the license string:
          1. SetPathToGlobalAddrFiles    - tell it where the data files live.
          2. SetLicenseString            - authorize the object.
          3. InitializeDataFiles         - load the data into memory.

        Args:
            license: The Melissa license string used to authorize the object.
            data_path: Path to the folder containing the Global Address Object data files.
        """
        # The underlying Melissa Global Address Object instance.
        self.md_global_address_obj = mdGlobalAddr_pythoncode.mdGlobalAddr()

        # Point the object at the Global Address Object data files, then license it.
        self.md_global_address_obj.SetPathToGlobalAddrFiles(data_path)
        self.md_global_address_obj.SetLicenseString(license)

        # Load the data files. The returned ProgramStatus reports whether initialization succeeded.
        # If you see a different date than expected, check your license string and either download the new data files
        # or use the Melissa Updater program to update your data files.
        p_status = self.md_global_address_obj.InitializeDataFiles()

        # If an issue occurred, please investigate the common causes.
        # Common causes: an invalid/expired license, or missing/wrong-path data files.
        if (p_status != mdGlobalAddr_pythoncode.ProgramStatus.ErrorNone):
            print("Failed to Initialize Object.")
            print(p_status)
            return

        # Diagnostic information, handy for confirming the object loaded the data you expect:

        # Build date of the data files
        print(f"                        DataBase Date: {self.md_global_address_obj.GetOutputParameter('databaseDate')}")

        # When the license stops working
        print(f"                      Expiration Date: {self.md_global_address_obj.GetOutputParameter('databaseExpirationDate')}")

        # This number should match with the file properties of the Melissa Object binary file.
        # If TEST appears with the build number, there may be a license key issue.
        print(f"                       Object Version: {self.md_global_address_obj.GetOutputParameter('buildNumber')}\n")

    def execute_object_and_result_codes(self, data):
        """
        Run the full Global Address Object processing sequence for one address. This is the
        canonical per-record call pattern to copy into your own application:
          ClearProperties -> filter_request -> SetInputParameter (per field) -> VerifyAddress
        Results are read afterwards via GetOutputParameter (see run_as_console).

        Args:
            data: The record to process; its address fields are read as input.

        Returns:
            A DataContainer carrying the same address fields plus this run's result codes.
        """
        # Reset any state left over from a previous address so fields don't bleed across records.
        self.md_global_address_obj.ClearProperties()

        # Drop any address line that just repeats locality/area/postal (see DataContainer).
        data.filter_request()

        # Hand each input field to the object by its parameter name.
        self.md_global_address_obj.SetInputParameter("inputAddressLine1", data.addressLine1)
        self.md_global_address_obj.SetInputParameter("inputAddressLine2", data.addressLine2)
        self.md_global_address_obj.SetInputParameter("inputAddressLine3", data.addressLine3)
        self.md_global_address_obj.SetInputParameter("inputLocality", data.locality)
        self.md_global_address_obj.SetInputParameter("inputAdministrativeArea", data.administrative_area)
        self.md_global_address_obj.SetInputParameter("inputPostalCode", data.postal_code)

        self.md_global_address_obj.SetInputParameter("inputCountry", data.country)

        # Validate and standardize the address
        self.md_global_address_obj.VerifyAddress()
        result_codes = self.md_global_address_obj.GetOutputParameter("resultCodes")

        # ResultsCodes explain any issues Global Address Object has with the object.
        # List of result codes for Global Address Object
        # https://docs.melissa.com/on-premise-api/global-address-object/result-codes.html

        return DataContainer(data.addressLine1, data.addressLine2, data.addressLine3, data.locality, data.administrative_area, data.postal_code, data.country, result_codes)




def parse_arguments():
    """
    Read the supported command-line options and return them as a (license,
    test_addressLine1, test_addressLine2, test_addressLine3, test_locality,
    test_administrative_area, test_postal_code, test_country, data_path) tuple.

    Recognized flags (each followed by its value):
      --license / -l             : the Melissa license string
      --addressLine1 / -a1       : street address line 1
      --addressLine2 / -a2       : street address line 2
      --addressLine3 / -a3       : street address line 3
      --locality / -lo           : locality (city)
      --administrativeArea / -aa : administrative area (state/province)
      --postalCode / -p          : postal code
      --country / -c             : country
      --dataPath / -d            : path to the Global Address Object data files

    Returns:
        A (license, test_addressLine1, test_addressLine2, test_addressLine3,
        test_locality, test_administrative_area, test_postal_code, test_country, data_path)
        tuple, each entry empty when its flag was not supplied.
    """
    license, test_addressLine1, test_addressLine2, test_addressLine3, test_locality, test_administrative_area, test_postal_code, test_country, data_path = "", "", "", "", "", "", "", "", ""

    args = sys.argv
    index = 0
    for arg in args:

        if (arg == "--license") or (arg == "-l"):
            if (args[index+1] != None):
                license = args[index+1]
        if (arg == "--addressLine1") or (arg == "-a1"):
            if (args[index+1] != None):
                test_addressLine1 = args[index+1]
        if (arg == "--addressLine2") or (arg == "-a2"):
            if (args[index+1] != None):
                test_addressLine2 = args[index+1]
        if (arg == "--addressLine3") or (arg == "-a3"):
            if (args[index+1] != None):
                test_addressLine3 = args[index+1]
        if (arg == "--locality") or (arg == "-lo"):
            if (args[index+1] != None):
                test_locality = args[index+1]
        if (arg == "--administrativeArea") or (arg == "-aa"):
            if (args[index+1] != None):
                test_administrative_area = args[index+1]
        if (arg == "--postalCode") or (arg == "-p"):
            if (args[index+1] != None):
                test_postal_code = args[index+1]
        if (arg == "--country") or (arg == "-c"):
            if (args[index+1] != None):
                test_country = args[index+1]
        if (arg == "--dataPath") or (arg == "-d"):
            if (args[index+1] != None):
                data_path = args[index+1]
        index += 1

    return (license, test_addressLine1, test_addressLine2, test_addressLine3, test_locality, test_administrative_area, test_postal_code, test_country, data_path)


def run_as_console(license, test_addressLine1, test_addressLine2, test_addressLine3, test_locality, test_administrative_area, test_postal_code, test_country, data_path):
    """
    Set up the Global Address Object once, then drive the input -> process -> output cycle.

    In interactive mode (no address args) it loops, prompting for each field until the user
    answers "N". In one-shot mode (address args supplied) it runs a single pass and exits.

    Args:
        license: The Melissa license string used to initialize the object.
        test_addressLine1: A first address line to process in one-shot mode; if empty, the
            program prompts interactively.
        test_addressLine2: A second address line to process in one-shot mode.
        test_addressLine3: A third address line to process in one-shot mode.
        test_locality: A locality (city) to process in one-shot mode.
        test_administrative_area: An administrative area (state/province) to process in
            one-shot mode.
        test_postal_code: A postal code to process in one-shot mode.
        test_country: A country to process in one-shot mode.
        data_path: Path to the Global Address Object data files.
    """
    print("\n\n========== WELCOME TO MELISSA GLOBAL ADDRESS OBJECT WINDOWS PYTHON3 =========\n")

    # Construct the wrapper. This is where the object is licensed, pointed at the data
    # files, and initialized (see the GlobalAddressObject constructor above).
    address_object = GlobalAddressObject(license, data_path)

    should_continue_running = True

    # Gate the program on a successful initialization. This object reports status via
    # GetOutputParameter; if the data files could not be loaded (bad/expired license,
    # missing or wrong-path data files, ...), "initializeErrorString" holds the reason
    # instead of "No error." and we skip the processing loop entirely.
    if address_object.md_global_address_obj.GetOutputParameter("initializeErrorString") != "No error.":
        should_continue_running = False

    while should_continue_running:

        if ((test_addressLine1 == None or test_addressLine1 == "") and (test_addressLine2 == None or test_addressLine2 == "") and
            (test_addressLine3 == None or test_addressLine3 == "") and (test_locality == None or test_locality == "") and 
            (test_administrative_area == None or test_administrative_area == "") and 
            (test_postal_code == None or test_postal_code == "") and (test_country == None or test_country == "")):

            # Interactive mode: prompt the user for each address field.
            print("\nFill in each value to see the Address Object results")
            addressLine1 =          str(input("Address Line 1: "))
            addressLine2 =          str(input("Address Line 2: "))
            addressLine3 =          str(input("Address Line 3: "))
            locality =              str(input("Locality: "))
            administrative_area =   str(input("Administrative Area: "))
            postal_code =           str(input("Postal Code: "))
            country =               str(input("Country: "))
        else:
            # One-shot mode: use the address fields passed on the command line.
            addressLine1 = test_addressLine1
            addressLine2 = test_addressLine2
            addressLine3 = test_addressLine3
            locality = test_locality
            administrative_area = test_administrative_area
            postal_code = test_postal_code
            country = test_country

        # Holder for this pass's input and result codes.
        data = DataContainer(addressLine1, addressLine2, addressLine3, locality, administrative_area, postal_code, country)

        # Print user input
        print("\n=================================== INPUTS ==================================\n")
        print(f"                       Address Line 1: {data.addressLine1}")
        print(f"                       Address Line 2: {data.addressLine2}")
        print(f"                       Address Line 3: {data.addressLine3}")
        print(f"                             Locality: {data.locality}")
        print(f"                  Administrative Area: {data.administrative_area}")
        print(f"                          Postal Code: {data.postal_code}")
        print(f"                              Country: {data.country}")

        # Execute Global Address Object
        # Runs the verify sequence; results are then read via GetOutputParameter below.
        data_container = address_object.execute_object_and_result_codes(data)

        # Print output
        # Each GetOutputParameter("...") below returns one field the object produced for
        # the most recently processed address. These read directly from the mdGlobalAddr
        # instance, which still holds the results from the Execute call above.
        print("\n=================================== OUTPUT ==================================\n")
        print("\n\tGlobal Address Object Information:")

        print(f"\t                   MAK: ", address_object.md_global_address_obj.GetOutputParameter("MAK"))
        print(f"\t               Company: ", address_object.md_global_address_obj.GetOutputParameter("Organization") )
        print(f"\t        Address Line 1: ", address_object.md_global_address_obj.GetOutputParameter("addressLine1") )
        print(f"\t        Address Line 2: ", address_object.md_global_address_obj.GetOutputParameter("addressLine2") )
        print(f"\t        Address Line 3: ", address_object.md_global_address_obj.GetOutputParameter("addressLine3") )
        print(f"\t        Address Line 4: ", address_object.md_global_address_obj.GetOutputParameter("addressLine4") )
        print(f"\t        Address Line 5: ", address_object.md_global_address_obj.GetOutputParameter("addressLine5") )
        print(f"\t              Locality: ", address_object.md_global_address_obj.GetOutputParameter("Locality"))
        print(f"\t   Administrative Area: ", address_object.md_global_address_obj.GetOutputParameter("AdministrativeArea")) 
        print(f"\t           Postal Code: ", address_object.md_global_address_obj.GetOutputParameter("postalCode"))
        print(f"\t               Postbox: ", address_object.md_global_address_obj.GetOutputParameter("postBox"))
        print(f"\t               Country: ", address_object.md_global_address_obj.GetOutputParameter("countryName") )
        print(f"\t         Country ISO 2: ", address_object.md_global_address_obj.GetOutputParameter("iso2Code") )
        print(f"\t         Country ISO 3: ", address_object.md_global_address_obj.GetOutputParameter("iso3Code") )
        print(f"\t              Latitude: ", address_object.md_global_address_obj.GetOutputParameter("Latitude"))
        print(f"\t             Longitude: ", address_object.md_global_address_obj.GetOutputParameter("Longitude")) 
        print(f"\t     Formatted Address: ", address_object.md_global_address_obj.GetOutputParameter("formattedAddress") )
        print(f"\t          Result Codes: {data_container.result_codes}")

        # Unlike the other objects, Global Address returns its result codes through
        # GetOutputParameter("resultCodes") (printed above) rather than GetResults(), so
        # the per-code description loop below is left commented out.
        # rs = data_container.result_codes.split(',')
        # for r in rs:
            # print(
            #     f"        {r}: {address_object.md_global_address_obj.GetResultCodeDescription(r, mdGlobalAddr_pythoncode.ResultCdDescOpt.ResultCodeDescriptionLong)}")

        is_valid = False

        # In one-shot mode there is nothing more to do after a single pass: mark the
        # input handled and stop the outer loop.
        if not (test_addressLine1 == None or test_addressLine1 == ""):
            is_valid = True
            should_continue_running = False
        # Interactive mode: ask whether to process another address. Keep prompting until
        # we get a valid Y/N. "N" ends the program; "Y" falls through to another pass.
        while not is_valid:

            test_another_response = input(
                str("\nTest another address? (Y/N)\n"))

            if not (test_another_response == None or test_another_response == ""):
                test_another_response = test_another_response.lower()
            if test_another_response == "y":
                is_valid = True

            elif test_another_response == "n":
                is_valid = True
                should_continue_running = False
            else:

                print("Invalid Response, please respond 'Y' or 'N'")

    print("\n================= THANK YOU FOR USING MELISSA PYTHON3 OBJECT ================\n")


# ---------------------------- MAIN STARTS HERE ----------------------------

# Read the optional command-line arguments, then hand control to run_as_console, which
# performs the actual Global Address Object setup and processing.
license, test_addressLine1, test_addressLine2, test_addressLine3, test_locality, test_administrative_area, test_postal_code, test_country, data_path = parse_arguments()

run_as_console(license, test_addressLine1, test_addressLine2, test_addressLine3, test_locality, test_administrative_area, test_postal_code, test_country, data_path)
