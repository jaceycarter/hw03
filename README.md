# Hello World!

My name is Jacey and I am here to show you how to ebay scrape using python!!!

With this, you can download the content of a specific item, search for only a specified number of pages, and make it into a JSON or .csv file. Steps are below. 

Follow the [project instructions!](https://github.com/mikeizbicki/cmc-csci040/tree/2021fall/hw_03)

# General
- Creates an Ebay URL from your chosen search term
- Downloads the specified number of results pages (my default is 10)
- Extracts the price, items sold, free returns or not, and the shipping price
- Compiles a JSON file containing these pieces

# How to: JSON files

Open `ebay-dl.py` in VSCode and insert terminal commands in the following format:

For standard searches scraping 10 pages of results and one word items, run
```
python3 ebay-dl.py item
```
in the command line. 

To scrape anything other than 10 pages, or search items with 2 or more words, run
```
python3 ebay-dl 'an item' --num_pages=x
```

The items I searched for are vegan, jordans, and basketball jersey. If you want to search these as well, here are the commands.

for the vegan.json file,
```
python3 ebay-dl.py vegan
```
 for the jordans.json file,
```
python3 ebay-dl.py jordans
```
and for the basketball jersey.json file, 
```
python3 ebay-dl.py 'basketball_jersey'
```

# How to: CSV files

To specify .csv file generation in the command line, add a `--csv` flag in your command, making it look like:
```
python3 ebay-dl --csv item
```
To generate the same .csv files I've generated, use the commands
for the vegan.csv file,
```
python3 ebay-dl.py --csv vegan
``` 
for the jordans.csv file,
```
python3 ebay-dl.py --csv jordans
```
and for the basketball_jersey.csv file, 
```
python3 ebay-dl.py --csv "basketball jersey"
```

Thank you for reading and try this out! 
