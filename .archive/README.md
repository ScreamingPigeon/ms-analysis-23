# ms-analysis-23

This is the repository that contains the notebooks for the Multiple-Sclerosis project at the Mobility and Fall Prevention Research Laboratory at the University of Illinois Urbana-Champaign.

The aim of this project is to use multi-class labeled gait (accelerometer) data to build a classifier for HoA individuals.
Once relevant features are identified - we intend to look at the class-wise differences between HoA and MS individuals to attempt to build a MS classifier to aid in diagnoses.
The data in question has is tri-axis accelerometer from an E4 wrist-band, sampled at 32Hz. This was collected during 2 hour clinical trials, where subjects performed a varited of ambulatory tasks.


## Setup
This noteook was written in a `Python 3.10.12` environment. The exact dependencies have been listed out in `requirements.txt`. 

Ensure that a `data/` directory exists. In case it does not, the `read_csv()` method may break, or the return value may be an empty `list` object. 

You can fork the repository and submit Pull Requests to contribute. Please work on reature/dev branches while pushing.





