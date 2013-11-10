# Discogsgrapher

*Discogsgrapher* generates a graph of from the artist/label connections of a certain *style* from the [Discogs](http://www.discogs.com/) database. 

This information is parsed from the *releases.xml* file of a [Discogs data dump](http://www.discogs.com/data/) and creates a graph from the information in the following manner: 

* Go through all the releases and find the ones that belong to the style in question and fit within the other parameters.
* Go through these artists and the labels that they have released music on.
* If two artists have released music on the same label consider them connected, if they have both released music on more than one label increase the weight of their connection.

You can see a live demo of the results for two of my favorite styles (*[Dubstep](http://www.discogs.com/explore?style=Dubstep)* and *[Drum n Bass](http://www.discogs.com/explore?style=Drum+n+Bass)*) at [http://www.karltryggvason.com/discogsgrapher](http://www.karltryggvason.com/discogsgrapher).

## Set up 

1. Run `pip install requirements.txt` (if don't like to be messy you might want to create an [environment](https://github.com/pypa/virtualenv) for this project)
2. Download the releases part of a [Discogs data dump](http://www.discogs.com/data/) 
3. run `python discogsgrapher.py` with the following parameters: 
    
        -x  /full/path/to/discogs/data/dump/release.xml
        -s  the style that you want to parse a network for
        -t  the treshold (minum number of releases) that artists must have in this style to be included
        -c  the country of the releases
        -b  the year you want to begin parsing from
        -e  the year you want to end the parsing on

4. Wait! The relases file is big (~12 gb) and this might take a while (about an hour on my admittely ancient Macbook)
5. You should now have a `.json` file that you can vizualize with [D3](http://d3js.org) 

## Links 

* The data is from the [Discogs data dumps](http://www.discogs.com/data/).
* [NetworkX](http://networkx.github.io/) is used for creating and manipulating the network.
* [lxml](http://lxml.de/) is used for parsing the data from the Discogs XML files.
* [python-louvain](https://bitbucket.org/taynaud/python-louvain) - for community detection.
