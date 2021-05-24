# String Matching

## Description:
Smatcher is a string matching programme: given a pattern and a text to match, it will return the indices of the matches.  
Smatcher implements 2 Algorithms:
* Naive String Matching: a window of length of the pattern slides over the string, if the string in the window is equal to the search pattern, a result is found
* Aho-Corasick Algorithm: this is the standard matching algorithm. It creates an automaton based on the [Aho-Corasick
Algorithm](https://www.uio.no/studier/emner/matnat/ifi/INF3800/v13/undervisningsmateriale/aho_corasick.pdf) and uses it to find matches in the text


## Requirements

Smatcher is implemented using only the python standard library.  
Python version: 3.8.5  
Developed on: Ubuntu 20.04  
Tested on Ubuntu 20.04, Windows 10

## Synopsis
```
usage: smatcher.py [-h] -p PATTERN [PATTERN ...] -t TEXT [TEXT ...] [-i] [-n] [-r] [-j] [-c]

required arguments:
  -p PATTERN [PATTERN ...], --pattern PATTERN [PATTERN ...]
                        the pattern to match, can be a list of strings or a file
  -t TEXT [TEXT ...], --text TEXT [TEXT ...]
                        text to be searched, can be a list of strings, a file or a directory

optional arguments:
  -i, --insensitive     case insensitive search
  -n, --naive           naive algorithm
  -r, --recursive       recursively look for all files in TEXT folder
  -j, --json            save results in a json file
  -c, --counter         print counts of matches instead of indeces
```
PATTERN can be:
* a single string: the programme will only match this string
* multiple strings: the programme will match all patterns
* a file: each line in the file will be treated as a search pattern


TEXT can be:
* a single string: the programme will only look for matches in this string
* multiple strings: the programme will look for matches in each string
* a file: the programme will find any match contained in the file
* a directory containing text files: the programme will look for matches in every single file (only if a 
file has a match will it be included in the results)

OPTIONS:  
* -i: case insensitive string mathing
* -n: the naive algorithm is used instead of the standard Aho-Corasick to find matches
* -r: if the TEXT argument is a directory, the programme will recursively open every file in every sub-directory
* -j: instead of printing the results to the terminal, they will be saved in the same fashion in results.json
* -c: instead of returning the indeces of the matched patterns, the programme will return the number of matches found

### Examples:

```
$ python smatcher.py -p "curious" -t "Curiouser and curiouser!"
14
```


```
$ python smatcher.py -p "curious" -t "Curiouser and curiouser!" -i
0, 14
```


```
$ python smatcher.py --pattern "the night is dark and full of terrors" --text data/Game_of_Thrones-master/season2/ -i
- e1.txt
	19689, 19755, 20993, 24968

- e4.txt
	22993, 35379
```


```
$ python smatcher.py --pattern data/patterns.txt --text data/Game_of_Thrones-master/season2 -i
- e1.txt
	the night is dark    19689, 19755, 20993, 21045, 24968
	and full of terrors  19707, 19773, 21011, 24986

- e4.txt
	the night is dark    22993, 35379
	and full of terrors  23011, 35397

```

```
$ python smatcher.py --pattern data/patterns.txt --text data/Game_of_Thrones-master/season2 -i -c
- e1.txt
	the night is dark    5
	and full of terrors  4

- e4.txt
	the night is dark    2
	and full of terrors  2
```
 
```
$ python smatcher.py --pattern "morghulis" "valar" --text data/Game_of_Thrones-master/ -r
- data/Game_of_Thrones-master/final_data.txt
	morghulis  811468, 907041, 982253, 1073759, 1410418, 1438700, 1474328, 1587962, 1635219, 1687072
	valar      1410451

- data/Game_of_Thrones-master/season3/e10.txt
	morghulis  27132

- data/Game_of_Thrones-master/season3/e3.txt
	morghulis  24658

- data/Game_of_Thrones-master/season3/e6.txt
	morghulis  7466

- data/Game_of_Thrones-master/season3/e8.txt
	morghulis  12195

- data/Game_of_Thrones-master/season4/e10.txt
	morghulis  26568
	valar      26601

- data/Game_of_Thrones-master/season5/e2.txt
	morghulis  825

- data/Game_of_Thrones-master/season5/e3.txt
	morghulis  774

- data/Game_of_Thrones-master/season5/e6.txt
	morghulis  4259

- data/Game_of_Thrones-master/season5/e7.txt
	morghulis  24088

- data/Game_of_Thrones-master/season5/e9.txt
	morghulis  14593

The following file(s) could not be opened:
	data/Game_of_Thrones-master/Arbeitsgruppen Kickoff, Protokoll.pdf
	data/Game_of_Thrones-master/mysteriousisland.epub
```

```
$ python smatcher.py --pattern "this" "programme" --text "some say this is a great programme" "others say this programme could be better"
- some say this is a great programme
	this       9
	programme  25

- others say this programme could be better
	this       11
	programme  16
```


##  Known Bugs
 
All bugs are unknown

### Notes

In order to take full advantage of bash shell autocompletion, it is advisable to use the full flag --text and --pattern for the required arguments.  
When using the short form (-t or -p), autocompletion will treat them as arguments for the python interpreter and thus will only autocomplete folder names.  
By using the long form, file names will be autocompleted correctly.

## Sources  

* Collection of Sherlock Holmes books from the Gutenberg Project: [big.txt](http://norvig.com/big.txt)
* Transcripts from every episode of the TV series Game of Thrones: [Game_of_Thrones-master](https://github.com/shekharkoirala/Game_of_Thrones)
* ePub version of the Book [The Mysterious Island](https://archive.org/details/mysteriousisland1884vern) from Jules Verne
