# Error correcting codes(ECC) are a signal processing technique to correct errors
# ECC Algorithm: Reed-Solomon Code
# Algorithm can be found in ReedSolomon.py

from ReedSolomon import * 

def CodeWord(msg):
    encoded_data = rs_encode_msg(msg)
    correct_synd = rs_calc_syndromes(encoded_data)
    print("\nEncoded Message: " , encoded_data)
    # print("\nSynd before error: ", correct_synd)
    # if not rs_check_syndromes(correct_synd):
    #     raise RuntimeError("Syndrome should be an all zero array when the data is correct")
    return encoded_data

def ErrorAddition(encoded_data, error_loc):
    err = [0] * len(encoded_data)
    for e in error_loc:
        err[e[0]] = e[1]
    print("\nError Matrix: ", err)
    rcw = gf_poly_add(encoded_data, err)
    print("\nReceived Code Word: ", rcw)
    synd = rs_calc_syndromes(rcw)
    print("\nSyndrome Vector: ", synd)
    return synd, rcw

def ErrorCorrection(encoded_data, synd, rcw):
        if rs_check_syndromes(synd):
            print("\n[#] 0 Errors Detected.")
        else:
            locator, evaluator = rs_find_error_locator_and_evaluator(synd)
            error_loc = rs_find_errors(locator, len(rcw))
            # print(error_loc)
            # if len(error_loc) > nsym:
            #     print("\n[#] Error are more than {}".format(nsym))
            # elif len(error_loc) > (nsym/2):
            #     print("\n[#] This Error can't be correct")
            if len(error_loc) == 0:
                print("\n[#] Too many Errors Detected.")
                return 0
            print("\n[#] {} errors in the message".format(len(error_loc)))
            msg_fixed = rs_correct_errata(rcw, error_loc, locator, evaluator)
            
            if msg_fixed == encoded_data:
                # print("msg fixed: " + str(msg_fixed))
                print("\nCorrected Msg: ", msg_fixed)
                print("\n[#] Error has been fixed using Reed Solomon Algorithm.")

## Pre defined test cases

# Case: Zero Errors
# Msg = [1, 0, 1, 0, 1, 0, 1, 0] # 8 bits
# ErrorLocation = [] #  0 Errors

# Case: 8 bit, 1 error
# Msg = [1, 0, 1, 0, 1, 0, 1, 0] # 8 bits
# ErrorLocation = [[1, 1]] # 1 Errors

# Case: 8 bit, 4 error
# Msg = [1, 0, 1, 0, 1, 0, 1, 0] # 8 bits
# ErrorLocation = [[1, 1], [3, 1], [5, 1], [7, 1]] # 4 Errors

# Case: 8 bit, 5 error
# Msg = [1, 0, 1, 0, 1, 0, 1, 0] # 8 bits
# ErrorLocation = [[0, 1], [1, 1], [3, 1], [5, 1], [7, 1]] # 5 Errors

# Case: 16 bit, 4 error
# Msg = [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0] # 16 bits
# ErrorLocation = [[1, 1], [3, 1], [5, 1], [7, 1]] # 4 Errors

# Case: 16 bit, 5 error
# Msg = [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0] # 16 bits
# ErrorLocation = [[1, 1], [3, 1], [5, 1], [7, 1]] # 5 Errors

if __name__ == "__main__":
    gf_init_table()
    rs_init_code_generator()
    print("\nOriginal Msg: ", Msg)
    # print("\nError Location: ", ErrorLocation)
    EncodedData = CodeWord(Msg)
    SyndromeVector, ReceivedCodeWord = ErrorAddition(EncodedData, ErrorLocation)
    ErrorCorrection(EncodedData, SyndromeVector, ReceivedCodeWord)

print("\nDone and Exiting ...")

# Comments:
# Max Error Correction capabilites 2t = n - k;
# where n is the total number of bits in the codeword and k is the number of bits in the message.
# Here, n = 16 and k = 8, so t = (16 - 8)/2 = 4