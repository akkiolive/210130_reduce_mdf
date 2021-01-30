print("loading asammdf...")
from asammdf import MDF, Signal
import numpy as np



def out(input_filename, verbose=True, save=True, saveName=None, overwrite=False):
    if verbose:
        print("loading mdf...:", input_filename)
    mdf = MDF(input_filename)


    #mdfreduc = mdf.cut(0,0) ##<- This will make duplicated channels for each signals
    mdfreduc = MDF(version=mdf.version)
    #mdfreduc.start_time = mdf.start_time ## <-This is not functional! You should replace mdf.header.start_time instead replacing mdf.start_time
    mdfreduc.header.start_time = mdf.start_time
    ss = []

    ignore_signals = ["time"]

    for num, signal in enumerate(mdf):
        if verbose:
            print(num, signal.name)
        t = signal.timestamps[0]
        v = signal.samples[0]
        s = Signal([v], [t], name=signal.name)
        t_prev = t
        v_prev = v
        for i in range(1, len(signal.timestamps)):
            t = signal.timestamps[i]
            v = signal.samples[i]
            if v_prev != v or i == len(signal.timestamps) - 1:
                s.samples = np.append(s.samples, v)
                s.timestamps = np.append(s.timestamps, t)
            t_prev = t
            v_prev = v
        ss.append(s)
        mdfreduc.append(s)

    #data_type 13 to 0
    if verbose:
        print("converting date_type 13(UNSIGNED_INTEL) to 0(UNSIGNED)...")
    for group in mdfreduc.groups:
        for channel in group.channels:
            if channel.data_type == 13:
                channel.data_type = 0

    if save:
        if verbose:
            print("saving...")
        if saveName:
            output_name = mdfreduc.save(saveName, overwrite=overwrite)
        else:
            output_name = mdfreduc.save(str(mdf.name.stem) + "_reduc", overwrite=overwrite)
        if verbose:
            print("output:", output_name)

    if verbose:
        print("closing mdf...")
    mdf.close()
    mdfreduc.close()

    if verbose:
        print("end")
    
    return mdfreduc


if __name__ == "__main__":    
    import sys
    if len(sys.argv) == 1:
        import tkinter.filedialog
        import os
        initDir = os.path.abspath(os.path.dirname(__file__))
        filenames = tkinter.filedialog.askopenfilenames(initialdir=initDir)
        for filename in filenames:
            out(input_filename=filename, verbose=True, save=True, overwrite=True)
    else:
        for filename in sys.argv:
            if filename != __file__:    
                out(input_filename=filename, verbose=True, save=True, overwrite=True)
    