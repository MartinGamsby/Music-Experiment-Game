import subprocess

#------------------------------------------------------------------------------
def run_uts():
    retVal = True
    for folder in ["test"]:
        returnCode = subprocess.run(['python', '-m', 'unittest', 'discover', folder]).returncode
        retVal &= (returnCode == 0 or returnCode == 5)# 5 is not tests
        if not retVal:
            print("Failed at least one UT, not doing further testing")
            return retVal
    
    return retVal
     
#------------------------------------------------------------------------------
if __name__ == "__main__":
    run_uts()
