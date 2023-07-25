import mdGlobalAddr_pythoncode
import sys


class DataContainer:
    def __init__(self, addressLine1="", addressLine2="", addressLine3="", locality="", administrative_area="", postal_code="", country="", result_codes=[]):
        self.addressLine1 = addressLine1
        self.addressLine2 = addressLine2
        self.addressLine3 = addressLine3
        self.locality = locality
        self.administrative_area = administrative_area
        self.postal_code = postal_code
        self.country = country

        self.result_codes = result_codes

    # These 2 functions are to ensure that the input does not repeat information in the area stack of the address within the address lines.
    # If either address line 2 or address line 3 contains the area stack information (locality, admin area, and postal code) then erase that address line.
    def filter_request(self):
            
            if self.check_for_area_stack(self.addressLine3):
                self.addressLine3 = ""
            elif self.check_for_area_stack(self.addressLine2):
                self.addressLine3 = ""
                self.addressLine2 = ""

    def check_for_area_stack(self, address_line):
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
    

    def __init__(self, license, data_path):

        """ Create instance of Melissa Address Object """
        self.md_global_address_obj = mdGlobalAddr_pythoncode.mdGlobalAddr()

        """ Set license string and set path to data files  (.dat, etc) """
        self.md_global_address_obj.SetPathToGlobalAddrFiles(data_path)
        self.md_global_address_obj.SetLicenseString(license)


        """    
        If you see a different date than expected, check your license string and either download the new data files or use the Melissa Updater program to update your data files.
        """

        p_status = self.md_global_address_obj.InitializeDataFiles()

        if (p_status != mdGlobalAddr_pythoncode.ProgramStatus.ErrorNone):
            print("Failed to Initialize Object.")
            print(p_status)
            return

        print(f"                        DataBase Date: {self.md_global_address_obj.GetOutputParameter('databaseDate')}")
        print(f"                      Expiration Date: {self.md_global_address_obj.GetOutputParameter('databaseExpirationDate')}")

        """
        This number should match with file properties of the Melissa Object binary file.
        If TEST appears with the build number, there may be a license key issue.
        """
        print(f"                       Object Version: {self.md_global_address_obj.GetOutputParameter('buildNumber')}\n")

    """ This will call the Lookup function to process the input address, city, state, and zip as well as generate the result codes """
    def execute_object_and_result_codes(self, data):
        self.md_global_address_obj.ClearProperties()

        data.filter_request()

        self.md_global_address_obj.SetInputParameter("inputAddressLine1", data.addressLine1)
        self.md_global_address_obj.SetInputParameter("inputAddressLine2", data.addressLine2)
        self.md_global_address_obj.SetInputParameter("inputAddressLine3", data.addressLine3)
        self.md_global_address_obj.SetInputParameter("inputLocality", data.locality)
        self.md_global_address_obj.SetInputParameter("inputAdministrativeArea", data.administrative_area)
        self.md_global_address_obj.SetInputParameter("inputPostalCode", data.postal_code)

        self.md_global_address_obj.SetInputParameter("inputCountry", data.country)

        self.md_global_address_obj.VerifyAddress()
        result_codes = self.md_global_address_obj.GetOutputParameter("resultCodes")

        """ 
        ResultsCodes explain any issues Global Address Object has with the object.
        List of result codes for Global Address Object
        https://wiki.melissadata.com/index.php?title=Result_Code_Details#Global_Address_Object

        """

        return DataContainer(data.addressLine1, data.addressLine2, data.addressLine3, data.locality, data.administrative_area, data.postal_code, data.country, result_codes)


    

def parse_arguments():
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
    print("\n\n========== WELCOME TO MELISSA GLOBAL ADDRESS OBJECT WINDOWS PYTHON3 =========\n")

    address_object = GlobalAddressObject(license, data_path)

    should_continue_running = True

    if address_object.md_global_address_obj.GetOutputParameter("initializeErrorString") != "No error.":
        should_continue_running = False

    while should_continue_running:

        if ((test_addressLine1 == None or test_addressLine1 == "") and (test_addressLine2 == None or test_addressLine2 == "") and
            (test_addressLine3 == None or test_addressLine3 == "") and (test_locality == None or test_locality == "") and 
            (test_administrative_area == None or test_administrative_area == "") and 
            (test_postal_code == None or test_postal_code == "") and (test_country == None or test_country == "")):

            print("\nFill in each value to see the Address Object results")
            addressLine1 =          str(input("Address Line 1: "))
            addressLine2 =          str(input("Address Line 2: "))
            addressLine3 =          str(input("Address Line 3: "))
            locality =              str(input("Locality: "))
            administrative_area =   str(input("Administrative Area: "))
            postal_code =           str(input("Postal Code: "))
            country =               str(input("Country: "))
        else:
            addressLine1 = test_addressLine1
            addressLine2 = test_addressLine2
            addressLine3 = test_addressLine3
            locality = test_locality
            administrative_area = test_administrative_area
            postal_code = test_postal_code
            country = test_country

        data = DataContainer(addressLine1, addressLine2, addressLine3, locality, administrative_area, postal_code, country)

        """ Print user input """
        print("\n=================================== INPUTS ==================================\n")
        print(f"                       Address Line 1: {data.addressLine1}")
        print(f"                       Address Line 2: {data.addressLine2}")
        print(f"                       Address Line 3: {data.addressLine3}")
        print(f"                             Locality: {data.locality}")
        print(f"                  Administrative Area: {data.administrative_area}")
        print(f"                          Postal Code: {data.postal_code}")
        print(f"                              Country: {data.country}")

        data_container = address_object.execute_object_and_result_codes(data)

        """ Print output """
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

        # rs = data_container.result_codes.split(',')
        # for r in rs:
            # print(
            #     f"        {r}: {address_object.md_global_address_obj.GetResultCodeDescription(r, mdGlobalAddr_pythoncode.ResultCdDescOpt.ResultCodeDescriptionLong)}")

        is_valid = False
        if not (test_addressLine1 == None or test_addressLine1 == ""):
            is_valid = True
            should_continue_running = False
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

"""  MAIN STARTS HERE   """

license, test_addressLine1, test_addressLine2, test_addressLine3, test_locality, test_administrative_area, test_postal_code, test_country, data_path = parse_arguments()

run_as_console(license, test_addressLine1, test_addressLine2, test_addressLine3, test_locality, test_administrative_area, test_postal_code, test_country, data_path)
