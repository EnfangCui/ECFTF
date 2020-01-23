# ECFTF
The source code of our paper "EC-FTF: Edge Computing Assisted Fast Time Fair Energy Allocation for Energy Harvesting Devices". 

### I. Code description
The code includes two parts: energy allocation algorithms and energy prediction algorithms. The following algorithms were implemented:
#### Energy allocation 
* **(1) FTF**: Fast Time Fair Energy Allocation algorithm of our paper.
* **(2) MAllEC**: implementation of Maximum Allowed Energy Consumption algorithm from "Mallec: Fast and optimal scheduling of energy consumption for energy harvesting devices," IEEE Internet of Things Journal, vol. 5, pp. 5132–5140, Dec 2018.
* **(3) buchli**: implementation of Periodic Optimal Control algorithm from "Optimal power management with guaranteed minimum energy utilization for solar energy harvesting systems", Buchli et al, DCOSS 2015
* **(4) gorlatova**: implementation of Progressive Filling algorithm from "Networking low-power energy harvesting devices: Measurements and algorithms", Gorlatova et al, INFOCOM, 2011.

Attention: The implementation of algorithm (2)(3)(4) refers to the source code [eh_python](https://github.com/victorcionca/eh_python) of V. Cionca. 

#### Energy Prediction
* LSTM based predictor.

#### Dataset
We collect 200 hours of metro vehicle vibration energy harvesting data in total at intervals of 2 min.


### II. Code File structure
* **/algorithms** -- Source code of algorithms.
* **/data** -- The metro vibration energy harvesting dataset we used.
* **/LSTM** -- LSTM energy predictor based on tensorflow.
* **/saved_models** -- Well trained LSTM model.
* **/simtest** -- Code for offline and online experiments
  * **/offline** -- Energy allocation algorithms + offline dataset
  * **/online** -- Energy allocation algorithms + Energy preditor
  
 ### III. Code environment requirements
 * Windows 10, IDE pycharm 2016.2.2 or higher
 * python 3.6.6
 * Tensorflow 1.10.0
 * keras 2.2.4
 * numpy 1.16.2
 * pandas 0.23.4
 
