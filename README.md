# Membership inference attack to trajectories
## Datasets:
* **GeoLife**: This GPS trajectory dataset was collected by the MSRA GeoLife project with 182 users in a period of over five years.
    * Link: https://www.microsoft.com/en-us/download/details.aspx?id=52367&from=https%3A%2F%2Fresearch.microsoft.com%2Fen-us%2Fdownloads%2Fb16d359d-d164-469e-9fd4-daa38f2b2e13%2F

* **Porto Taxi**: This GPS tarjectory dataset was collected during one year in the city of Porto, in Portugal. The dataset contains taxi trips that are sampled every 15 seconds to form a sequence of points.
    * Link: https://figshare.com/articles/dataset/Porto_taxi_trajectories/12302165?file=22677902

## Dependencies:
* python: 3.11.9
* torch: 2.3.1+cu118
* numpy: 1.26.3
* pandas: 2.2.2
* scikit-learn: 1.5.0
* matplotlib: 3.9.0

## Usage:
* Run python fbb.py --help to know the different configurations of the Full Balck Box attack.
* Run fbb.py with the desired configuration.
* Check in the data/geolife/[epsilon]/predictions folder the file created with the adv value at the beginning of the file name and the configuration of the attack performed on the rest of the name.
* Once some attacks have been done for all epsilon values run python code/evaluations.py in order to get the privacy gains displayed for all attacks performed in comparison to the best attack without DP. 