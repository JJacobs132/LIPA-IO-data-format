# LIPA-IO-data-format
The LIPAIO data format assumes that data collection has the following structure.
Measurement <br>
    -> Sequence <br>
        -> Aquisition <br>

An aquisition is a single recorded time trace, equivalent to a  single a-scan. 
All aquisitions made with the same parameters such as source-reciever location pair make up a sequence.
All sequences in a single experiment make up a measurement.

The LIPAIO data format consists of 4 parts:
Datacube (DC): 4 dimensional matrix storing the raw data recorded during an experiment or simulation. 
Sequence parameter matrix (SPM): Contains the experiment parameters which are constant for all aquisitions across a single sequence
Metadata (MTD): Contains the experiment parameters which are constant for all aquisitions in the measurement
Calculated sequence parameter matrix (CSPM): Contains certain derived values which are constant for all aquisitions across a single sequence

Except for the CSPM, nearly all data is either measured directly or set by the operator when conducting a measurement. The big exception to this is when the number of aquisitions would make the file size prohibitivly large, requiring the averaging of aquisitions. In this case the number of actual aquisitions to generate one stored aquisition over which was averaged will be stored in the SPM.



