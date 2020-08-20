# zippy-dl

zippy-dl is self-contained selenium based zippyshare downloader. It also extracts everything.

### No need to download anything

## How to run
Clone the repo: \
```git clone https://github.com/JSubelj/zippy-dl.git```
Install requirements:\
```
cd zippy-dl
pip install -r requirements.txt
```
Run:
```
zippy-dl.py --help                                                                                                                       [0]
usage: zippy-dl.py [-h] [-f FILE] [-o OUTPUT] [url]

Downloads a file from zippyshare

positional arguments:
  url                   an integer for the accumulator

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  File with urls separated by newline
  -o OUTPUT, --output OUTPUT
                        Output directory (default: '.')

```

### TODO:
Create proper installer\
Get to pip