# Python Projects and steps

## world_democracy_index.py

1. `world_democracy_index.py` only requires `pip install requirements.txt`

## fred_stuff.py

1. `fred_stuff.py` requires a FRED API key. Get one at `https://fredaccount.stlouisfed.org/apikeys`

# R projects and steps

## pums_analysis.R

1. You need three files: psam_pusa.csv, psam_pusb.csv, and PUMS_Data_Dictionary_2024.csv.
2. To obtain psam_pusa.csv and psum_pusb.csv run `curl -O https://www2.census.gov/programs-surveys/acs/data/pums/2024/1-Year/csv_pus.zip` in the data folder (/r/data). Then `unzip csv_pus.zip`
3. To obtain PUMS_Data_Dictionary_2024.csv run `curl -O https://www2.census.gov/programs-surveys/acs/data/pums/2024/1-Year/PUMS_Data_Dictionary_2024.csv` in the data folder (/r/data)
4. Then run `Rscript pums_analysis.R` in /r to perform the analysis