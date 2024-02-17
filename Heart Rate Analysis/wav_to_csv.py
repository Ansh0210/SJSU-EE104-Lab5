import numpy as np
import scipy.io as sio
import pandas as pd

def wav_to_csv(wav_file, csv_file):
    
    wav_data = sio.wavfile.read(wav_file)
    
    wav_array = np.array(wav_data[1])
    
    df = pd.DataFrame(wav_array)
    
    df.to_csv(csv_file, index=False)

if __name__ == '__main__':

    wav_file = 'normal_22311236.wav'
    csv_file = 'my_csv_file.csv'

    wav_to_csv(wav_file, csv_file)
