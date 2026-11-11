# LIPA-IO-data-format
The LIPAIO data format assumes that data collection has the following structure. <br>
Measurement <br>
    -> Sequence <br>
        -> Aquisition <br>

An acquisition is a single recorded time trace, equivalent to a  single a-scan. 
All acquisitions made with the same parameters, such as source-receiver location pairs, make up a sequence.
All sequences in a single experiment make up a measurement.

The LIPAIO data format consists of 4 parts:
Datacube (DC): 4 dimensional matrix storing the raw data recorded during an experiment or simulation. <br>
Sequence parameter matrix (SPM): Contains the experiment parameters that are constant for all acquisitions across a single sequence. <br>
Metadata (MTD): Contains the experiment parameters that are constant for all acquisitions in the measurement. <br>
Calculated sequence parameter matrix (CSPM): Contains certain derived values that are constant for all acquisitions across a single sequence

Except for the CSPM, nearly all data is either measured directly or set by the experiment operator when conducting a measurement. The big exception to this is when the number of acquisitions would make the file size prohibitively large, requiring the averaging of acquisitions. In this case the number of actual acquisitions to generate one stored acquisition over which was averaged will be stored in the SPM.



