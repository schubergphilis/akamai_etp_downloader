Akamai Enterprise Threat Protection Reports Downloader
======================
Script to download Akamai Enterprise Threat Protection reports as CSV files.

The script can keep state across runs and download only the new reports.

Installation
```
sudo pip install -r requirements.txt
```

Prior to running the script, the following environment variables need to be set:
```sh
  ETP_ACCESS_TOKEN      Akamai ETP Access Token
  ETP_CLIENT_TOKEN      Akamai ETP Client Token
  ETP_CLIENT_SECRET     Akamai ETP Client Secret
```

Using the Akamai ETP downloader:
```sh
$ ./etp_downloader.py -h
usage: etp_downloader.py [-h] -s SERVER [-r READ_FILE] [-l LOG_FILE] [-D]
                         [-d DOWNLOAD_FOLDER]

Download reports from Akamai ETP

optional arguments:
  -h, --help            show this help message and exit
  -s SERVER, --server SERVER
                        Akamai ETP Servername
  -r READ_FILE, --read_file READ_FILE
                        Read this file instead of making a web request (for
                        DEBUG)
  -l LOG_FILE, --log_file LOG_FILE
                        Log to file instead of STDERR
  -D, --debug           Debug
  -d DOWNLOAD_FOLDER, --download_folder DOWNLOAD_FOLDER
                        Destination folder for CSVs - default to "./akamai-
                        etp-reports"
```

