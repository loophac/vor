def logo():
     print ("\n")
     print ("                    _____                    _           ")
     print ("                   |  ___|                  | |          ")
     print ("                   | |__ _ __   ___ ___   __| | ___ _ __ ")
     print ("                   |  __| '_ \ / __/ _ \ / _` |/ _ \ '__|")
     print ("                   | |__| | | | (_| (_) | (_| |  __/ |")   
     print ("                   \____/_| |_|\___\___/ \__,_|\___|_|") 
     print ("")
     print ("     ======================================================================")
     print ("     Requires Python3")
     print ("     Original Encode/Decode Algorithm Copyrighted by David Beazley (http://www.dabeaz.com)")
     print ("     Rebuilt by S1lv3r(Loophac) for user interface and easy deployment of script/text files 2017")
     print ("")
     input('Press enter to continue: ')
     print ("                     ")
     print ("                     ")
     print ("              \n       ")
     return main()
        


def main():
    #!/usr/bin/python
    # scriptencoder.py
    #
    # Author : s1lv3r (Watchmen)
    # 
    #
    # Requires Python 3.1.2 or newer
    # Rebuilt 2017
    
    """
    Takes the contents of a text file and encodes it into a Kansas
    City Standard WAV file, that when played will upload data via the
    cassette tape input on various vintage home computers. See
    http://en.wikipedia.org/wiki/Kansas_City_standard
    """
    
    import wave
    
    # A few global parameters related to the encoding
    
    FRAMERATE = 9600       # Hz
    ONES_FREQ = 80        # Hz (per KCS)
    ZERO_FREQ = 40        # Hz (per KCS)
    AMPLITUDE = 128        # Amplitude of generated square waves
    CENTER    = 128        # Center point of generated waves
    
    # Create a single square wave cycle of a given frequency 
    def make_square_wave(freq,framerate):
        n = int(framerate/freq/2)
        return bytearray([CENTER-AMPLITUDE//2])*n + \
               bytearray([CENTER+AMPLITUDE//2])*n
    
    # Create the wave patterns that encode 1s and 0s
    one_pulse  = make_square_wave(ONES_FREQ,FRAMERATE)*8
    zero_pulse = make_square_wave(ZERO_FREQ,FRAMERATE)*4
    
    # Pause to insert after carriage returns (10 NULL bytes)
    null_pulse = ((zero_pulse * 9) + (one_pulse * 2))*10
    
    # Take a single byte value and turn it into a bytearray representing
    # the associated waveform along with the required start and stop bits.
    def kcs_encode_byte(byteval):
        bitmasks = [0x1,0x2,0x4,0x8,0x10,0x20,0x40,0x80]
        # The start bit (0)
        encoded = bytearray(zero_pulse)
        # 8 data bits
        for mask in bitmasks:
            encoded.extend(one_pulse if (byteval & mask) else zero_pulse)
        # Two stop bits (1)
        encoded.extend(one_pulse)
        encoded.extend(one_pulse)
        return encoded
    
    # Write a WAV file with encoded data. leader and trailer specify the
    # number of seconds of carrier signal to encode before and after the data
    def kcs_write_wav(filename,data,leader,trailer):
        w = wave.open(filename,"wb")
        w.setnchannels(1)
        w.setsampwidth(1)
        w.setframerate(FRAMERATE)
    
        # Write the leader
        w.writeframes(one_pulse*(int(FRAMERATE/len(one_pulse))*leader))
    
        # Encode the actual data
        for byteval in data:
            w.writeframes(kcs_encode_byte(byteval))
            if byteval == 0x0d:
                # If CR, emit a short pause (10 NULL bytes)
                w.writeframes(null_pulse)
        
        # Write the trailer
        w.writeframes(one_pulse*(int(FRAMERATE/len(one_pulse))*trailer))
        w.close()
    
    if __name__ == '__main__':
        import sys
        in_filename = input('Enter an in_filename: ')  #Ask for a file name
        out_filename = input('Enter an out_filename: ') # ^^^^
        data = open(in_filename,"U").read()
        data = data.replace('\n','\r\n')         # Fix line endings
        rawdata = bytearray(data.encode('latin-1'))
        kcs_write_wav(out_filename,rawdata,5,5)
    
logo()
