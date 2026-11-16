import numpy as np
import csv
import os
import zipfile as zipf

class DC:
    def __init__(self,dc:np.ndarray = None):
        if dc is None:
            self.dc = np.array([]) 
        else:
            assert type(dc) == np.ndarray # assert that DC will behave as expected
            self.dc = dc

    def writenpy(self,file:str): # TODO: move csv suffix to classes so that they automatically add a suffix if needed
        np.save(file,self.dc)

    def readnpy(self, file:str):
        self.dc = np.load(file)

class SPM:
    def __init__(self,N_source:int,N_reciever:int):
        """
        TODO: description
        """
        self.N_source = N_source
        self.N_reciever = N_reciever

        self.fieldnames = ['seqnr','t0', 'tf','n_averages','r_sx','r_rx']   # TODO: add correct stage parameter values
        self.dtypes = [int, str,str,int,float,float]
        self.spm = np.array([[{} for _ in range(self.N_reciever)] for _ in range(self.N_source)], dtype=object)

    def writecsv(self,file:str):
        """
        Write SMP matrix-dictionary to a csv file
        """
        self.check_dict_keys() # checking consitensy of filled dictionary fields and associated datatypes
        self.check_datatype()

        with open(file, mode = 'w', newline = '')as file:
            writer = csv.DictWriter(file,fieldnames=self.fieldnames)
            writer.writeheader()
            writer.writerows(self.spm.flatten())

    def readcsv(self,file:str):
        """
        Read SMP matrix-dictionary from a csv file
        """
        empty = []
        with open(file, mode = 'r', newline = '')as file:
            reader = csv.DictReader(file,fieldnames=self.fieldnames)
            next(reader) # skipping header line
            for row in reader:
                row = {k: v for k, v in row.items() if v.strip()} # trim away whitespace
                empty.append(row)
            self.spm = np.array(empty).reshape(self.N_source,self.N_reciever) # reshape list into numpy array with correct dimensions

        self.enforce_datatype() # set all values to their associated datatypes
        
    def present_keys_dtypes(self):
        """
        Makes a list of the keys present in the (0,0) dictioinary of the SPM
        """
        self.keys_present = []
        self.dtypes_present = []
        tkeys = list(self.spm[0,0].keys())
        for tkey in tkeys:
            self.keys_present.append(tkey)
            self.dtypes_present.append(self.dtypes[self.fieldnames.index(tkey)])

    def check_dict_keys(self):
        keys00 = self.spm[0,0].keys()
        for i in range(self.N_source):
            for j in range(self.N_reciever):
                if self.spm[i,j].keys() != keys00:
                    raise Exception("dictionary keys within SPM are inconsistent")
        print("SPM dictionary keys are consistent")

    def check_datatype(self):
        """
        Set data in dictionaries to associated dataypes
        """
        self.present_keys_dtypes()
        for i in range(self.N_source):
            for j in range(self.N_reciever):
                for k in range(len(self.keys_present)):
                    if type(self.spm[i,j][self.keys_present[k]]) != self.dtypes_present[k]:
                        raise TypeError('Incorrect datatype for SPM sequence '+str(i)+','+str(j))
        print('All SPM datatypes are as expected')
        

    def enforce_datatype(self):
        """
        Set data in dictionaries to associated dataypes
        """
        self.present_keys_dtypes()
        for i in range(self.N_source):
            for j in range(self.N_reciever):
                for k in range(len(self.keys_present)):
                    self.spm[i,j][self.keys_present[k]] = self.dtypes_present[k](self.spm[i,j][self.keys_present[k]])
        print('Set SPM data to appropriate datatypes')



class CSPM:
    def __init__(self,N_source:int,N_reciever:int):
        self.N_source = N_source
        self.N_reciever = N_reciever

        self.fieldnames = ['r_s', 'r_r']
        self.dtypes = [float, float]
        self.cspm = np.array([[{} for _ in range(self.N_reciever)] for _ in range(self.N_source)], dtype=object)

    def writecsv(self,file:str):
        """
        Read CSPM matrix-dictionary from a csv file
        """
        self.check_dict_keys() # checking consitensy of filled dictionary fields and associated datatypes
        self.check_datatype()

        with open(file, mode = 'w', newline = '')as file:
            writer = csv.DictWriter(file,fieldnames=self.fieldnames)
            writer.writeheader()
            writer.writerows(self.cspm.flatten())

    def readcsv(self,file:str):
        """
        Read CSPM matrix-dictionary from a csv file
        """
        empty = []
        with open(file, mode = 'r', newline = '')as file:
            reader = csv.DictReader(file,fieldnames=self.fieldnames)
            next(reader) # skipping header line
            for row in reader:
                row = {k: v for k, v in row.items() if v.strip()} # trim away whitespace
                empty.append(row)
            self.cspm = np.array(empty).reshape(self.N_source,self.N_reciever) # reshape list into numpy array with correct dimensions

        self.enforce_datatype() # set all values to their associated datatypes

    def present_keys_dtypes(self):
        """
        Makes a list of the keys present in the (0,0) dictioinary of the CSPM
        """
        self.keys_present = []
        self.dtypes_present = []
        tkeys = list(self.cspm[0,0].keys())
        for tkey in tkeys:
            self.keys_present.append(tkey)
            self.dtypes_present.append(self.dtypes[self.fieldnames.index(tkey)])

    def check_dict_keys(self):
        keys00 = self.cspm[0,0].keys()
        for i in range(self.N_source):
            for j in range(self.N_reciever):
                if self.cspm[i,j].keys() != keys00:
                    raise Exception("dictionary keys within CSPM are inconsistent")
        print("CSPM dictionary keys are consistent")
        
    def check_datatype(self):
        """
        Compare datatypes in dictionaries to associated dataypes
        """
        self.present_keys_dtypes()
        for i in range(self.N_source):
            for j in range(self.N_reciever):
                for k in range(len(self.keys_present)):
                    if type(self.cspm[i,j][self.keys_present[k]]) != self.dtypes_present[k]:
                        raise TypeError('Incorrect datatype for CSPM sequence '+str(i)+','+str(j))
        print('All CSPM datatypes are as expected')
        

    def enforce_datatype(self):
        """
        Set data in dictionaries to associated dataypes
        """
        self.present_keys_dtypes()
        for i in range(self.N_source):
            for j in range(self.N_reciever):
                for k in range(len(self.keys_present)):
                    self.cspm[i,j][self.keys_present[k]] = self.dtypes_present[k](self.cspm[i,j][self.keys_present[k]])
        print('Set CSPM data to appropriate datatypes')



class MTD:
    def __init__(self):
        self.mtd = {}
        self.fieldnames = ['f_s','l_s','l_r','t_m','t_i','wf','sample', 'setup','type','clamp', 'note' ]
        self.dtypes = [float, float, float, float, float, str, str, str, str, str, str]

    def writecsv(self,file:str):
        self.check_datatype() # checking consitensy of associated datatypes 
        with open(file, mode = 'w', newline = '')as file:
            writer = csv.DictWriter(file,fieldnames=self.fieldnames)
            writer.writeheader()
            writer.writerow(self.mtd)

    def readcsv(self,file:str):
        empty = []
        with open(file, mode = 'r', newline = '')as file:
            reader = csv.DictReader(file,fieldnames=self.fieldnames)
            next(reader) # skipping header line
            for row in reader:
                row = {k: v for k, v in row.items() if v.strip()} # trim away whitespace
                self.mdt = row

        self.enforce_datatype() # set all values to their associated datatypes

    def present_keys_dtypes(self):
        self.keys_present = []
        self.dtypes_present = []
        tkeys = list(self.mtd.keys())
        for tkey in tkeys:
            self.keys_present.append(tkey)
            self.dtypes_present.append(self.dtypes[self.fieldnames.index(tkey)])

    def check_datatype(self):
        """
        Compare datatypes in dictionaries to associated dataypes
        """
        self.present_keys_dtypes()
        for k in range(len(self.keys_present)):
            if type(self.mtd[self.keys_present[k]]) != self.dtypes_present[k]:
                raise TypeError('Incorrect datatype in the metadata !')
        print('All MTD datatypes are as expected')
        

    def enforce_datatype(self):
        """
        Set data in dictionaries to associated dataypes
        """
        self.present_keys_dtypes()
        for k in range(len(self.keys_present)):
            self.mtd[self.keys_present[k]] = self.dtypes_present[k](self.mtd[self.keys_present[k]])
        print('Set MTD data to appropriate datatypes')

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