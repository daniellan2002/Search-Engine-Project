# Search-Engine-Project
This is the Search Engine Project for CS 121, Group 20. This is a search engine for a selection of subdomains that belong to UC Irvine's School of ICS. It instantly (usually within 150 ms) shows top-ranking results among 55,000+ webpages.

Goup 20 members:
* [Jack Yu](https://github.com/Jack-Yu-815)
* [Daniel Lan](https://github.com/daniellan2002)
* [Joseph Russell Pon](https://github.com/joeyrpon)
* [Ha Bach](https://github.com/muninnhugin)

The project has several segments:
* text extraction from HTML format
* tokenization and stemming
* index creation
* given a query, rank documents' relevance using Cosine Similarity

## Web Search Interface
Visit this [search engine website](http://ec2-34-219-99-245.us-west-2.compute.amazonaws.com:9000) and simply type in your query and search.
For example, try searching `VR gaming`, `machine learning`, the name of your favorite professor, and more...


## How to reproduce the result?

### 1. Index Creation
* [Download](https://drive.google.com/file/d/1abVnb3XhcwBlooW738F_2BdnB_VcLV9G/view?usp=share_link) and unzip the directory containing information of all the scraped webpages.
* run `M1` function inside `main.py` to create the full index file. This process may take some time.

### 2. Search Interface
* a) Search in Terminal
  * run `M2n3` function inside `main.py` and interact with the prompt
* b) Host Webpage and Its Backend
  * run the command `python3 flask_server.py` in terminal. You can change the port inside `flask_server.py` as you wish. 
  * visit the host machine's `IP_address:port_number` using a browser to access the Web search interface. 
