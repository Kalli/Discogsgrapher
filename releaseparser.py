#!/usr/bin/python
# -*- coding: utf-8 -*-
from lxml import etree

def recursive_dict(element):
     return element.tag, \
            dict(map(recursive_dict, element)) or element.text

class ReleaseParser():
    def __init__(self, pathToReleaseXML, style, threshold, country, start, end):
        print("---------------------------------")
        print("Parsing: ")
        print("File: "+pathToReleaseXML)
        print("Style: "+style)
        print("Country: "+country)
        print("Release threshold: "+str(threshold))
        print("From: "+str(start)+" to "+str(end))
        print("---------------------------------")
        self.filepath=pathToReleaseXML
        self.style = style
        self.country = country
        self.threshold = threshold
        self.start = start
        self.end = end

        self.artists = []
        self.labels = []


        self.findAllStyleArtists()
        self.removeArtistsBelowThreshold()
        print("---------------------------------")
        print("Finished Parsing"+self.filepath)
        print("---------------------------------")
        print("Found "+str(len(self.artists))+" artists")
        print("Found "+str(len(self.labels))+" labels")
        print("---------------------------------")


    def findAllStyleArtists(self):
        context = etree.iterparse(self.filepath, events=("start", "end"))
        context = iter(context)
        event, root = context.next()
        for event, elem in context:
            try:
                if event == "end" and elem.tag == "release":      
                    if self.shouldParse(elem):
                        self.parseArtistAndLabel(elem)
                root.clear()
            except ValueError, error:
                print error
                return False

    def shouldParse(self, elem):
        country = elem.find("country")        
        if country is None or country.text != self.country:
            return False
        released = elem.find("released")
        if released is None:
            return False
        if len(released.text) < 3:
            return False
        released = int(released.text[0:4])
        if released < self.start or released > self.end:
            return False
        return True
        styles = elem.find("styles")
        if styles is not None:
            for style in styles:
                if style.text == self.style:
                    return True


    def removeArtistsBelowThreshold(self):
        self.artists = [artist for artist in self.artists if artist["count"] >= self.threshold]
        for label in self.labels:
            if label["name"] == "Not On Label":
                self.labels.remove(label)


    def parseArtistAndLabel(self, elem):
        if elem.find("artists") is not None and elem.find("labels") is not None:
            release_labels = self.parseLabels(elem)
            release_artists = self.parseArtists(elem)
            for release_artist in release_artists:
                if release_artist["id"] != "194" and release_artist["name"] != "Unknown Artist": # 194 is the pesky "Various"
                    artist = self.findArtistById(release_artist["id"])
                    if artist is None:
                        release_artist["count"] = 1
                        self.artists.append(release_artist)
                    else:
                        artist["count"] += 1
                    for release_label in release_labels:
                        release_label["artists"].append(release_artist["id"])
            for release_label in release_labels:
                label = next((label for label in self.labels if label["name"] == release_label["name"]), None)
                if label is None:
                    self.labels.append(release_label)
                else:
                    label["artists"].extend(release_label["artists"])
            

    def parseArtists(self, elem):
        artists = elem.find("artists")
        release_artists = []
        for artist in artists:
            release_artists.append(recursive_dict(artist)[1])
        return release_artists


    def parseLabels(self, elem):
        labels = []
        for label in elem.find("labels"):
            if label.get("name") is not "Not On Label":
                labels.append({"name":label.get("name"), "artists":[]})
        return labels

    def findArtistById(self, id):
        search_artist = None
        for artist in self.artists:
            if artist["id"] == id:
                search_artist = artist
                break
        return search_artist
