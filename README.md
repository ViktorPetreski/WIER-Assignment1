# Navigation


[Assignment 1: Web crawler](#assignment-1-web-crawler)

[Assignment 2: Structured data extraction](#assignment-2-structured-data-extraction)

[Assignment 3: Searching with inverted index](#assignment-3-searching-with-inverted-index)


# Assignment 1: Web crawler

For the purpose of this assignment we implemented a crawler that crawls *\*.gov.si* pages. The crawler is implemented in Python and for storing the information from the crawled pages we used PostgreSQL database with the provided *crawldb* model.

## The crawler

The main code that we used is located in the `Main_crawler.ipynb` file. To be able to run this code you will need to install MurmurHash3 and OrderedSet:
- `conda install -c keiserlab mmh3`  or `pip install mmh3`
- `conda install -c conda-forge ordered-set` or `pip install ordered-set`

The file `Frontier_crawler.ipynb` contains only part of the crawler, used for extracting the content of each URL that has the *page_type_code* set to FRONTIER. We ran this code after having enough URLs in the frontier to try to speed up the process. 

## The database
> Note: The database was dockerized

To be able to import the database, you need to remove the existing container, create new one without the init-scripts volume and let it start. After the container is started, use the *sql* dump to restore the database.
The commands are below (change *dump_name* with the database dump name):
```
docker rm -f postgresql-wier
docker run --name postgresql-wier -e POSTGRES_PASSWORD=postgres -e POSTGRES_USER=postgres -v $PWD/pgdata:/var/lib/postgresql/data -p 5432:5432 -d postgres:9
cat {dump_name}.sql | docker exec -i postgresql-wier psql -U postgres
```
If you are using Windows execute `docker volume create --driver local pgdata` and remove *$PWD/* from the second line above.

> There are 403 codes in the database even though the content is there. It was too late to change the method from *head* to *get* as you suggested

[Google Drive link to the database](https://drive.google.com/open?id=1_rOJB_z2xKtohWERE8qKcYgtDK8tLs7H)

Extract it with `tar -xvf database.tar.gz`

[The report](report-crawler.pdf)

## Network graph for eprostor.gov.si
It is better if you download it and zoom it
![the network](crawler/path1.png)


# Assignment 2: Structured data extraction

For this assignment, we implemented content extractors using regular expressions, XPath and automatic web extraction with a roadrunner-like algorithm. We tested our implementation using the provided offline web pages and a third one of our choice.

We attach the [pseudo code pdf](Pseudocode.pdf) for better visibility.
There is also a separate HTML file for each web site that contains the extracted output from the roadrunner-like algorithm.

[The report](report-extraction.pdf)

## Execution

#### Requirements
- BeautifulSoup
- lxml
 
Call `run-extractor.py` with the type of the extractor needed: _regex_, _xpath_, _roadrunner_.

Example: `run-extractor.py regex`

Each extractor prints the result on standard output. The name of the domain is also printed for better distinction of the results 

## Additional website
We chose [Global Scale Company](globalscalecompany.com)'s website. It has mix of both data and list elements. The structure of the page and the names of the fields that we extracted are shown on the image below. 
![the structure](implementation-extraction/combined.png)

# Assignment 3: Searching with inverted index

For the third assignment we implemented an inverted index for information retrieval.

## Execution

#### Requirements
- BeautifulSoup
- nltk
- tabulate
- tqdm

Call `implementation-indexing/run-basic-search.py` or `implementation-indexing/run-sqlite-search.py` with the seach parameter that you want to query. They have to be called from the root folder.

Examples: `implementation-indexing/run-basic-search.py "social services"`, `implementation-indexing/run-sqlite-search.py "social services"`.

Both of the functions will print the output in the required format on the standard output.


 


