from ctypes import *
from enum import Enum
import ctypes
import os
import sys

if (os.name == 'nt' and sys.version_info[:2] >= (3,8)):
  lib = ctypes.CDLL('mdGlobalAddr.dll', winmode=0)
elif (os.name == 'nt'):
  lib = ctypes.CDLL('mdGlobalAddr.dll')
else:
  lib = ctypes.CDLL('libmdGlobalAddr.so')

lib.mdGlobalAddrCreate.argtypes = []
lib.mdGlobalAddrCreate.restype = c_void_p
lib.mdGlobalAddrDestroy.argtypes = [c_void_p]
lib.mdGlobalAddrDestroy.restype = None
lib.mdGlobalAddrSetLicenseString.argtypes = [c_void_p, c_char_p]
lib.mdGlobalAddrSetLicenseString.restype = c_bool
lib.mdGlobalAddrSetPathToGlobalAddrFiles.argtypes = [c_void_p, c_char_p]
lib.mdGlobalAddrSetPathToGlobalAddrFiles.restype = None
lib.mdGlobalAddrInitializeDataFiles.argtypes = [c_void_p]
lib.mdGlobalAddrInitializeDataFiles.restype = c_int
lib.mdGlobalAddrClearProperties.argtypes = [c_void_p]
lib.mdGlobalAddrClearProperties.restype = None
lib.mdGlobalAddrSetInputParameter.argtypes = [c_void_p, c_char_p, c_char_p]
lib.mdGlobalAddrSetInputParameter.restype = c_bool
lib.mdGlobalAddrVerifyAddress.argtypes = [c_void_p]
lib.mdGlobalAddrVerifyAddress.restype = c_int
lib.mdGlobalAddrGetOutputParameter.argtypes = [c_void_p, c_char_p]
lib.mdGlobalAddrGetOutputParameter.restype = c_char_p
lib.mdGlobalAddrTransliterateText.argtypes = [c_void_p, c_char_p, c_char_p, c_char_p]
lib.mdGlobalAddrTransliterateText.restype = c_char_p
lib.mdGlobalAddrGetCurrentAtomSet.argtypes = [c_void_p]
lib.mdGlobalAddrGetCurrentAtomSet.restype = c_char_p
lib.mdGlobalAddrInputsAsAtomSet.argtypes = [c_void_p]
lib.mdGlobalAddrInputsAsAtomSet.restype = c_char_p
lib.mdGlobalAddrRightFieldResultsAsAtomSet.argtypes = [c_void_p, c_char_p]
lib.mdGlobalAddrRightFieldResultsAsAtomSet.restype = c_char_p
lib.mdGlobalAddrTokenizerResultsAsAtomSet.argtypes = [c_void_p, c_char_p]
lib.mdGlobalAddrTokenizerResultsAsAtomSet.restype = c_char_p
lib.mdGlobalAddrInputMapperResultsAsAtomSet.argtypes = [c_void_p, c_char_p]
lib.mdGlobalAddrInputMapperResultsAsAtomSet.restype = c_char_p
lib.mdGlobalAddrMatchEngineResultsAsAtomSet.argtypes = [c_void_p, c_char_p]
lib.mdGlobalAddrMatchEngineResultsAsAtomSet.restype = c_char_p
lib.mdGlobalAddrOutputMappingResultsAsAtomSet.argtypes = [c_void_p, c_char_p]
lib.mdGlobalAddrOutputMappingResultsAsAtomSet.restype = c_char_p
lib.mdGlobalAddrSetOutputsFromAtomSet.argtypes = [c_void_p, c_char_p]
lib.mdGlobalAddrSetOutputsFromAtomSet.restype = None

# mdGlobalAddr Enumerations
class ProgramStatus(Enum):
	ErrorNone = 0
	ErrorOther = 1
	ErrorOutOfMemory = 2
	ErrorRequiredFileNotFound = 3
	ErrorFoundOldFile = 4
	ErrorDatabaseExpired = 5
	ErrorLicenseExpired = 6

class AccessType(Enum):
	Local = 0
	Remote = 1

class DiacriticsMode(Enum):
	Auto = 0
	On = 1
	Off = 2

class StandardizeMode(Enum):
	ShortFormat = 0
	LongFormat = 1
	AutoFormat = 2

class SuiteParseMode(Enum):
	ParseSuite = 0
	CombineSuite = 1

class AliasPreserveMode(Enum):
	ConvertAlias = 0
	PreserveAlias = 1

class AutoCompletionMode(Enum):
	AutoCompleteSingleSuite = 0
	AutoCompleteRangedSuite = 1
	AutoCompletePlaceHolderSuite = 2
	AutoCompleteNoSuite = 3

class ResultCdDescOpt(Enum):
	ResultCodeDescriptionLong = 0
	ResultCodeDescriptionShort = 1

class MailboxLookupMode(Enum):
	MailboxNone = 0
	MailboxExpress = 1
	MailboxPremium = 2

class mdGlobalAddr(object):
	def __init__(self):
		self.I = lib.mdGlobalAddrCreate()

	def __del__(self):
		lib.mdGlobalAddrDestroy(self.I)

	def SetLicenseString(self, p1):
		return lib.mdGlobalAddrSetLicenseString(self.I, p1.encode('utf-8'))

	def SetPathToGlobalAddrFiles(self, p1):
		lib.mdGlobalAddrSetPathToGlobalAddrFiles(self.I, p1.encode('utf-8'))

	def InitializeDataFiles(self):
		return ProgramStatus(lib.mdGlobalAddrInitializeDataFiles(self.I))

	def ClearProperties(self):
		lib.mdGlobalAddrClearProperties(self.I)

	def SetInputParameter(self, pszParamName, pszParamValue):
		return lib.mdGlobalAddrSetInputParameter(self.I, pszParamName.encode('utf-8'), pszParamValue.encode('utf-8'))

	def VerifyAddress(self):
		return lib.mdGlobalAddrVerifyAddress(self.I)

	def GetOutputParameter(self, pszParamName):
		return lib.mdGlobalAddrGetOutputParameter(self.I, pszParamName.encode('utf-8')).decode('utf-8')

	def TransliterateText(self, pszInput, pszInputScript, pszOutputScript):
		return lib.mdGlobalAddrTransliterateText(self.I, pszInput.encode('utf-8'), pszInputScript.encode('utf-8'), pszOutputScript.encode('utf-8')).decode('utf-8')

	def GetCurrentAtomSet(self):
		return lib.mdGlobalAddrGetCurrentAtomSet(self.I).decode('utf-8')

	def InputsAsAtomSet(self):
		return lib.mdGlobalAddrInputsAsAtomSet(self.I).decode('utf-8')

	def RightFieldResultsAsAtomSet(self, pszAtomSet):
		return lib.mdGlobalAddrRightFieldResultsAsAtomSet(self.I, pszAtomSet.encode('utf-8')).decode('utf-8')

	def TokenizerResultsAsAtomSet(self, pszAtomSet):
		return lib.mdGlobalAddrTokenizerResultsAsAtomSet(self.I, pszAtomSet.encode('utf-8')).decode('utf-8')

	def InputMapperResultsAsAtomSet(self, pszAtomSetArray):
		return lib.mdGlobalAddrInputMapperResultsAsAtomSet(self.I, pszAtomSetArray.encode('utf-8')).decode('utf-8')

	def MatchEngineResultsAsAtomSet(self, pszAtomSetArray):
		return lib.mdGlobalAddrMatchEngineResultsAsAtomSet(self.I, pszAtomSetArray.encode('utf-8')).decode('utf-8')

	def OutputMappingResultsAsAtomSet(self, pszAtomSet):
		return lib.mdGlobalAddrOutputMappingResultsAsAtomSet(self.I, pszAtomSet.encode('utf-8')).decode('utf-8')

	def SetOutputsFromAtomSet(self, pszAtomSet):
		lib.mdGlobalAddrSetOutputsFromAtomSet(self.I, pszAtomSet.encode('utf-8'))
