> in order to decompress workload.tbz2 files:
> ```shell
> tar -jxvf workload.tbz2
> ```
> This gives you a workload.txt file. in this file,
> request rates (number of requests per second) are separated by a space.

### Ready to use dataset files:
- #### Nasa: [link](https://github.com/reconfigurable-ml-pipeline/web-service-datasets/raw/master/dataset/nasa/workload.tbz2)

### Nasa dataset
- Two months' logs of all HTTP requests to the NASA Kennedy Space Center WWW server in Florida
- Read logs description: run `wget ftp://ita.ee.lbl.gov/html/contrib/NASA-HTTP.html` 
  in terminal, then open the html file in your browser.
- Download logs data: run 
    ```shell
    wget ftp://ita.ee.lbl.gov/traces/NASA_access_log_Jul95.gz
    wget ftp://ita.ee.lbl.gov/traces/NASA_access_log_Aug95.gz
    gzip -dk NASA_access_log_Jul95.gz
    gzip -dk NASA_access_log_Aug95.gz
    ```
- Process dataset to generate workload.tbz2 (already done, and the files are ready to use):
    - make a .env file in the root directory of the repository.
    - add this to the .env file (replace the path with the correct path):
      `nasa_logs_directory="/path/to/directory/containing/above/files"`
    - run `pip install -r requirements.txt` in terminal
    - run `python dataset/nasa/dataset_reader.py`
    - now you have the files in the related directory
  

### WorldCup dataset
- All the requests made to the 1998 WorldCup Website between April 30, 1998, and July 26, 1998.
- Read logs description: run `wget ftp://ita.ee.lbl.gov/html/contrib/WorldCup.html` in terminal,
  then open the html file in your browser.
- Download all wc_day{x}_{y}.gz files listed in the above html into a directory (you can use "wget" for downloading).
- run `gzip -dk wc_dayx_y.gz` on each files (replace x and y with related numbers in filenames).
- Process dataset to generate workload.tbz2 (already done, and the files are ready to use):
  - make a .env file in the root directory of the repository.
  - add this to the .env file (replace the path with the correct path):
    `worldcup_logs_directory="/path/to/directory/containing/above/files"`
  - run `pip install -r requirements.txt` in terminal.
  - run `python dataset/worldcup/dataset_reader.py`
  - now you have the files in the related directory