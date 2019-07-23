# Generating navfiles from bottle and CTD data

This project's purpose is to create nav files in .txt format for all bottle and ctd
dataset cruises that have no track but have files to obtain LONGITUDE and LATITUDE.
The python script `find_non_tracked.py` creates a list with cruise IDs of ALL cruises with
no tracks. The script `find_non_tracked_with_files.py` creates a list with cruise IDs of
all cruises only with no tracks that have files. The scripts `generate_nav_bottle.py` and
`generate_nav_ctd.py` generate navigation files in .txt.

Once the nav files are created each .txt can then be patched and curled to cchdo.ucsd.edu to update the empty track using `click_nav.py`.

## Getting Started

It is recommended to first create a virtual environment to run your project using `virutalenv`.
Instructions can be followed here to download and install pyenv https://github.com/pyenv/pyenv-virtualenv
Use
```
pyenv activate <name_of_your_virtualenv>
```
to activate in each terminal session.

Once you have a virtualenv then you can start with `generate_nav_bottle.py`. The script is commented at each step. To run it, change your directory to the project folder where the script is located and in the terminal enter
```
python generate_nav_bottle.py
```
 It will take several minutes to run because it loops
through all CCHDO cruises. Once it is completed there will be navigation files that appear in your directory with expocode_nav.txt such as
```
320619940214_nav.txt
```

Repeat this process for CTD's by running
```
python generate_nav_ctd.py
```

### Running the Patch to CCHDO

Go to the cruise page https://cchdo.ucsd.edu/api/v1/cruise to find the cruise
ID that matches the expocode of your cruise. For example `320619940214` is cruise ID `2121`. An example of how to run the patch is below

```
python click_nav.py 320619940214_nav.txt - | curl --http1.1 -X PATCH https://cchdo.ucsd.edu/api/v1/cruise/2121 --data @-
```
This can be repeated by replacing the above command each appropriate expocode and matching cruise number.


## Authors

* **Samantha Kuglen** 
