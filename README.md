# CSGY-6513-Project


## Installation
To install the dependency, you can either use the requirements.txt file or directly use the conda environment on HPC.
### Use Conda Env on HPC
We have already created a conda enviroment containing all the necessary packages on HPC. If you are on Peel, you can directly use it by
```shell
conda activate /scratch/gw2145/conda/envs/covid
```
We have already granted the access to any of the users. However, due to the security issue, we are sorry we are not able to provide the access after May 2021.


### Install by Pip
If you would like to use your own Python environment, you can use pip to install the dependency.
```shell
pip install ./requirements.txt
```

## Prepare Data
To enable spark functions, you need to upload the data to HFS
```shell
hfs --put ./integrated_data.csv

```
## Running

Our analysis notebook relies on Pyspark and jupyter. Since Pyspark relies on the Spark session, you can not directly use jupyter notebook command to start the notebook. Here is the steps you need to do.
```shell
export PYSPARK_DRIVER_PYTHON=jupyter
export PYSPARK_DRIVER_PYTHON_OPTS='notebook'
export PYSPARK_PYTHON='/scratch/gw2145/conda/envs/covid/bin/python' # if you use your conda env, please modify it to you python executable file
cd ./notebooks
pyspark --deploy-mode=client
```
