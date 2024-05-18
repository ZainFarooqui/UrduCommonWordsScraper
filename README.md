# UrduCommonWords

This is a simple tool to scrape a number of supplied URLs and return the most common Urdu words found in the sample. This was made for my personal use for learning the language.

## How to use

Supply the desired URLs in the config file in under the "urls" fields array. You can also supply an array of excluded words to ignore. You can specify x number of words to return (defualt to 100) and to ignore the top y words (default to 0)

The tool will then output the list of words line by line to a text file called "output".