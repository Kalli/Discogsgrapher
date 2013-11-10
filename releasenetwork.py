#!/usr/bin/python
# -*- coding: utf-8 -*
import networkx as nx
from networkx.readwrite import json_graph
import json
import community

class ReleaseNetwork():
	def __init__(self, releaseparser):
		print("Creating network")
		print("---------------------------------")
		self.releaseparser = releaseparser
		self.g = nx.Graph()
		self.createArtistLabelGraph()
		self.detectCommunities()

	def createArtistLabelGraph(self):
		print("Adding Artist Nodes")
		for artist in self.releaseparser.artists:
			self.g.add_node(artist["name"], name=artist["name"], discogsid=artist["id"], count=artist["count"])
		print("Artist nodes: "+str(self.g.number_of_nodes()))
		print("Adding Label Edges")
		for label in self.releaseparser.labels:
			for index1, artistid in enumerate(label["artists"]):
				artist1 = self.releaseparser.findArtistById(str(artistid))
				if artist1 is not None:
					for index2 in range(index1, len(label["artists"])):
						artistid2 = label["artists"][index2]
						artist2 = self.releaseparser.findArtistById(str(artistid2))
						if artist2 is not None:
							if self.edgeExists(artist1, artist2):
								if label["name"] not in self.g[artist1["name"]][artist2["name"]]["label"]: 
									self.g[artist1["name"]][artist2["name"]]["label"] += ", "+label["name"]
								self.g[artist1["name"]][artist2["name"]]["value"] += 1
							if self.edgeExists(artist2, artist1):
								if label["name"] not in self.g[artist2["name"]][artist1["name"]]["label"]: 
									self.g[artist2["name"]][artist1["name"]]["label"] += ","+label["name"]
								self.g[artist2["name"]][artist1["name"]]["value"] += 1	
							else:
								self.g.add_edge(artist1["name"], artist2["name"], {"label":label["name"], "value":1})
		print("Label edges: "+str(self.g.number_of_edges()))

	def edgeExists(self, artist1, artist2):
		if artist1["name"] in self.g[artist1["name"]] and artist2["name"] in self.g[artist1["name"]]:
			return True
		else:
			return False


	def detectCommunities(self):
		artistcommunity = community.best_partition(self.g)
		for key, value in artistcommunity.items():
			self.g.node[key]["group"]=value


	def saveGraphAsJson(self):
		d = json_graph.node_link_data(self.g)
		filename = './'+self.releaseparser.style.replace(" ","-")+"-"+self.releaseparser.country+"-"+str(self.releaseparser.start)+"-"+str(self.releaseparser.end)+'.json'
		json.dump(d, open(filename,'w'))
		print("Network JSON saved to: "+filename)
