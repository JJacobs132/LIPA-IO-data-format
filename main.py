import numpy as np
import csv
import os
import zipfile as zipf

class DC:
    def __init__(self,DC:np.ndarray = None):
        if DC is None:
            self.DC = np.array([]) #TODO: make objects lower case
        else:
            assert type(DC) == np.ndarray # assert that DC will behave as expected
            self.DC = DC

    def writenpy(self,file:str): # TODO: move csv suffix to classes so that they automatically add a suffix if needed
        np.save(file,self.DC)

    def readnpy(self, file:str):
        self.DC = np.load(file)

class SPM:
    def __init__(self,N_source:int,N_reciever:int):
        """

        """
        self.N_source = N_source
        self.N_reciever = N_reciever

        self.fieldnames = ['seqnr','t0', 'tf','n_averages','r_sx','r_rx']   # TODO: add correct stage parameter values
        self.SPM = np.array([[{} for _ in range(self.N_reciever)] for _ in range(self.N_source)], dtype=object)

    def writecsv(self,file:str):
        with open(file, mode = 'w', newline = '')as file:
            writer = csv.DictWriter(file,fieldnames=self.fieldnames)
            writer.writeheader()
            writer.writerows(self.SPM.flatten())

    def readcsv(self,file:str):
        empty = []
        with open(file, mode = 'r', newline = '')as file:
            reader = csv.DictReader(file,fieldnames=self.fieldnames)
            next(reader) # skipping header line
            for row in reader:
                row = {k: v for k, v in row.items() if v.strip()} # trim away whitespace
                empty.append(row)
            self.SPM = np.array(empty).reshape(self.N_source,self.N_reciever) # reshape list into numpy array with correct dimensions

    def enforcedatatype(self):
        """
        Correct data in dictionaries to associated dataypes
        """
        # TODO: implement
        pass



class CSPM:
    def __init__(self,N_source:int,N_reciever:int):
        self.N_source = N_source
        self.N_reciever = N_reciever

        self.fieldnames = ['r_s', 'r_r']
        self.CSPM = np.array([[{} for _ in range(self.N_reciever)] for _ in range(self.N_source)], dtype=object)

    def writecsv(self,file:str):
        with open(file, mode = 'w', newline = '')as file:
            writer = csv.DictWriter(file,fieldnames=self.fieldnames)
            writer.writeheader()
            writer.writerows(self.CSPM.flatten())

    def readcsv(self,file:str):
        empty = []
        with open(file, mode = 'r', newline = '')as file:
            reader = csv.DictReader(file,fieldnames=self.fieldnames)
            next(reader) # skipping header line
            for row in reader:
                row = {k: v for k, v in row.items() if v.strip()} # trim away whitespace
                empty.append(row)
            self.CSPM = np.array(empty).reshape(self.N_source,self.N_reciever) # reshape list into numpy array with correct dimensions

    def enforcedatatype(self):
        """
        Correct data in dictionaries to associated dataypes
        """
        # TODO: implement
        pass



class MTD:
    def __init__(self):
        self.MTD = {}
        self.fieldnames = ['f_s','l_s','l_r','t_m','t_i','wf','sample', 'setup','type','clamp', 'note' ]

    def writecsv(self,file:str):
            with open(file, mode = 'w', newline = '')as file:
                writer = csv.DictWriter(file,fieldnames=self.fieldnames)
                writer.writeheader()
                writer.writerow(self.MTD)

    def readcsv(self,file:str):
            empty = []
            with open(file, mode = 'r', newline = '')as file:
                reader = csv.DictReader(file,fieldnames=self.fieldnames)
                next(reader) # skipping header line
                for row in reader:
                    row = {k: v for k, v in row.items() if v.strip()} # trim away whitespace
                    self.MTD = row

    def enforcedatatype(self):
            """
            Correct data in dictionaries to associated dataypes
            """
            # TODO: implement
            pass

class LIPA_IO:
    def __init__(self, N_source, N_reciever, dc:DC = None, spm:SPM = None, mtd:MTD = None, cspm:CSPM = None):
        self.N_source = N_source
        self.N_reciever = N_reciever

        self.suffix = ['-dc.npy', '-spm.csv', '-mtd.csv', '-cspm.csv'] # extensions for each subfile

        # if subdata not loaded, initialize empty version
        self.dc = dc if dc is not None else DC()
        self.spm = spm if spm is not None else SPM(N_source,N_reciever)
        self.mtd = mtd if mtd is not None else MTD()
        self.cspm = cspm if cspm is not None else CSPM(N_source, N_reciever)


    def write(self,filename): # TODO implement existing filename check

        # write files for all subdata
        self.dc.writenpy(filename + self.suffix[0])
        self.spm.writecsv(filename + self.suffix[1]) 
        self.mtd.writecsv(filename + self.suffix[2])
        self.cspm.writecsv(filename + self.suffix[3])

        # zip subfiles together
        with zipf.ZipFile(filename+'.zip', "w") as zf: # TODO: change to LIPAIO extension for clarity
            for sufx in self.suffix:
                zf.write(filename + sufx) # TODO: seperate folder and filename, currently creates unnecessary forlder in zipfile

        # remove generated subdata files to prevent clutter, leaving only .LIPAIO file      
        for sufx in self.suffix:
           os.remove(filename + sufx)

    def read(self,filename):
        with zipf.ZipFile(filename +'.zip', "r") as zf: # TODO: change to LIPAIO extension for clarity
            self.dc = np.load(zf.open(filename + self.suffix[0])) # load the datacube directly
            
            for sufx in self.suffix[1:]: # extract csv files and read into appropriate objects
                zf.extract(filename + sufx)
            self.spm.readcsv(filename + self.suffix[1]) 
            self.mtd.readcsv(filename + self.suffix[2])
            self.cspm.readcsv(filename + self.suffix[3])

        # remove generated subdata files to prevent clutter, leaving only .LIPAIO file and object associated with the class
        for sufx in self.suffix[1:]:
            os.remove(filename + sufx)