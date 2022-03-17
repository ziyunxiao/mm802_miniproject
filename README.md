# Introduction
This project is for MM802 mini project. 
The data source is from https://data.edmonton.ca/.

1. [Edmonton Property Assessment Data](https://data.edmonton.ca/City-Administration/Property-Assessment-Data-Current-Calendar-Year-/q7d6-ambg/data)
2. [EPS Neighbourhood Criminal Occurrences](https://dashboard.edmonton.ca/dataset/EPS-Neighbourhood-Criminal-Occurrences/xthe-mnvi/data)

For details, how the data is prepared please read `data_preparation.ipynb`.


## Access online
You can access the app from [here](https://share.streamlit.io/ziyunxiao/mm802_miniproject/app.py)

# Setup
The sample commands is based on Linux.
## prequirement
Python 3.9

## Setup project
1. clone the project `git clone https://github.com/ziyunxiao/mm802_miniproject.git`
2. cd project folder `cd mm802_miniproject`
3. setup python virtual env `python3.8 -m venv .venv`
4. activate virtual env `. .venv/bin/activate`
5. run `pip install --upgrade pip`
6. install required package `pip install -r requirements.txt`
7. Start web server `streamlit run app.py --server.port 8080`
8. open browser and access [http://localhost:8080/](http://localhost:8080/)

# 
