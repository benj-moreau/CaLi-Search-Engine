curl -X POST \
  http://127.0.0.1:8000/api/ld/licenses \
  -H 'Admin-Password: YOUR_ADMIN_PASSWORD' \
  -H 'Content-Type: application/json' \
  -d '[
	{
		"labels": ["ODC-PDDL", "Public-domain", "CC-Ze"],
		"licensing_terms": ["https://www.opendatacommons.org/licenses/pddl/1-0", "https://creativecommons.org/publicdomain/zero/1.0/legalcode"],
	    "permissions": ["Distribution", "Reproduction", "CommericalUse", "DerivativeWorks", "modify"],
	    "obligations": [],
	    "prohibitions": [],
	    "resources": [
	    	{
				"label": "LOD-a-lot",
				"uri": "http://lod-a-lot.lod.labs.vu.nl/LOD-a-lot",
				"description": "A Queryable Dump of the LOD Cloud"
			},
			{
				"label": "Enipedia - Energy Industry Data",
				"uri": "http://enipedia.tudelft.nl/sparql",
				"description": "Enipedia is an active exploration into the applications of wikis and the semantic web for energy and industry issues. Through this we seek to create a collaborative environment for discussion, while also providing the tools that allow for data from different sources to be connected, queried, and visualized from different perspectives."
			},
			{
				"label": "NASA Space Flight & Astronaut data",
				"uri": "http://api.kasabi.com/dataset/nasa/apis/sparql",
				"description": "Conversion of various NASA datasets into RDF, starting with the spacecraft data from the NSSDC master catalog."
			},
			{
				"label": "Bicycle Crashes",
				"uri": "https://data.opendatasoft.com/explore/api/tpf/bicycle-crash-data-chapel-hill-region@townofchapelhill",
				"description": "This data set maps the locations of crashes involving bikes in the Chapel Hill Region of North Carolina."
			}
	    ]
	},
	{
		"labels": ["MIT"],
		"licensing_terms": ["https://opensource.org/licenses/MIT"],
	    "permissions": ["Distribution", "Reproduction", "CommericalUse", "DerivativeWorks", "modify"],
	    "obligations": ["Notice"],
	    "prohibitions": [],
	    "resources": [
	    	{
				"label": "CaLi Classifiaction",
				"uri": "http://cali.priloo.univ-nantes.fr/api/licenses",
				"description": "CaLi Classifiaction of licenses for the linked Data."
			}
	    ]
	},
	{
		"labels": ["CC BY", "ODC-By", "Etalab-ol-lo", "UK-open-government", "GPL3"],
		"licensing_terms": ["https://creativecommons.org/licenses/by/3.0/legalcode", "https://opendatacommons.org/licenses/by/1-0/", "https://github.com/etalab/licence-ouverte/blob/master/open-licence.md", "http://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/", "https://www.gnu.org/licenses/gpl-3.0"],
	    "permissions": ["Distribution", "Reproduction", "CommericalUse", "DerivativeWorks", "modify"],
	    "obligations": ["Attribution", "Notice"],
	    "prohibitions": [],
	    "resources": [
	    	{
				"label": "RISM Authority data",
				"uri": "http://data.rism.info/sparql",
				"description": "Authority data used in the (RISM catalogue, dataset description). It contains information about persons, organisations and literary works."
			},
			{
				"label": "RDFLicense",
				"uri": "http://purl.org/NET/rdflicense",
				"description": "This dataset contains 126 licenses (suitable for general works, data, etc.) expressed as RDF.This work is the joint effort of OEG-UPM (Víctor Rodríguez-Doncel) and INRIA (Serena Villata). The editors have not acted in behalf of any of the license issuers, do not claim the legal value of this RDF-version of the licenses, and explicitly decline any responsibility in their use."
			},
			{
				"label": "LinkedDrugs: Linked Drug Product Data on a Global Scale",
				"uri": "http://drugs.linkeddata.finki.ukim.mk/",
				"description": "The LinkedDrugs dataset with drug product data from different countries."
			},
			{
				"label": "TweetsKB - A Public and Large-Scale RDF Corpus of Annotated Tweets",
				"uri": "http://l3s.de/tweetsKB/endpoint/",
				"description": "TweetsKB is a public RDF corpus of anonymized data for a large collection of annotated tweets. The dataset currently contains data for more than 1.5 billion tweets, spanning almost 5 years (January 2013 - November 2017). Metadata information about the tweets as well as extracted entities, sentiments, hashtags and user mentions are exposed in RDF using established RDF/S vocabularies. For the sake of privacy, we anonymize the usernames and we do not provide the text of the tweets. However, through the tweet IDs, actual tweet content and further information can be fetched."
			},
			{
				"label": "Influence Tracker Dataset",
				"uri": "http://www.influencetracker.com:8890/sparql",
				"description": "Datasets regarding the Influence Tracker service."
			},
			{
				"label": "WarSampo",
				"uri": "http://ldf.fi/warsa/sparql",
				"description": "This dataset includes harmonized data of different kinds concerning the Second World War in Finland, separated in different graphs representing events, actors, places, photographs, and other aspects and documentation of the war. To test and demonstrate its usefulness, this data service is in use in the semantic portal WarSampo explained in more detail in the project page."
			},
			{
				"label": "IMGpedia",
				"uri": "http://imgpedia.dcc.uchile.cl/sparql",
				"description": "IMGpedia is a large-scale linked dataset that incorporates visual information of the images from the Wikimedia Commons dataset: it brings together descriptors of the visual content of 15 million images, 450 million visual-similarity relations between those images, links to image metadata from DBpedia Commons, and links to the DBpedia resources associated with individual images."
			},
			{
				"label": "FOODpedia",
				"uri": "http://foodpedia.tk/sparql",
				"description": "At this moment FOODpedia contains information about only Russian food products and ingredients that was crawled from GoodsMatrix web site. Also it has links to ingredients from AGROVOC."
			},
			{
				"label": "Places disponibles parkings Saemes",
				"uri": "https://data.opendatasoft.com/explore/api/tpf/places-disponibles-parkings-saemes@saemes",
				"description": "Ce jeu de données présente les places disponibles en temps réel des parkings exploités par Saemes à Paris et en Ile-de-France."
			},
			{
				"label": "JCDecaux Bike Stations Data",
				"uri": "https://data.opendatasoft.com/explore/api/tpf/jcdecaux_bike_data@public",
				"description": "JCDecaux bike stations availability data. This dataset is updated in real time. You can access these data directly from the JCDecaux Developer site: https://developer.jcdecaux.com/#/home."
			},
			{
				"label": "Public bike pumps Bristol",
				"uri": "https://data.opendatasoft.com/explore/api/tpf/public-bike-pumps@bristol",
				"description": "Location of free to use bycyle pumps Bristol City Council"
			}
	    ]
	},
	{
		"labels": ["ODC-ODbL"],
		"licensing_terms": ["https://opendatacommons.org/licenses/odbl/1.0"],
	    "permissions": ["Distribution", "Reproduction", "CommericalUse", "DerivativeWorks", "modify"],
	    "obligations": ["Attribution", "ShareAlike", "Notice"],
	    "prohibitions": [],
	    "resources": [
	    	{
				"label": "OSM Semantic Network",
				"uri": "http://spatial.ucd.ie/lod/sparql",
				"description": "The OSM Semantic Network is a Semantic Web resource extracted from the OpenStreetMap Wiki website, encoded as a SKOS vocabulary."
			},
			{
				"label": "Autolib - Disponibilité temps réel",
				"uri": "https://data.opendatasoft.com/explore/api/tpf/autolib-disponibilite-temps-reel@parisdata",
				"description": "Données de disponibilités des voitures et bornes des stations Autolib."
			},
			{
				"label": "Durham Bike Racks",
				"uri": "https://data.opendatasoft.com/explore/api/tpf/durham-bike-parking@durham",
				"description": "Dataset of bike racks in the City of Durham"
			}
	    ]
	},
	{
		"labels": ["CC BY-SA"],
		"licensing_terms": ["https://creativecommons.org/licenses/by-sa/3.0/legalcode"],
	    "permissions": ["Distribution", "Reproduction", "CommericalUse", "DerivativeWorks", "modify"],
	    "obligations": ["Attribution", "Notice", "ShareAlike"],
	    "prohibitions": [],
	    "resources": [
	    	{
				"label": "Fatal Traffic Accidents in greek roads",
				"uri": "https://ckannet-storage.commondatastorage.googleapis.com/2014-11-23T07:56:29.726Z/roadaccidents.ttl",
				"description": "Fatal Traffic Accidents in greek roads (From 01-Jan-2010 to 11-Aug-2014)"
			},
			{
				"label": "LODStats",
				"uri": "http://lodstats.aksw.org/sparql",
				"description": "LODStats: The Data Web Census Dataset."
			},
			{
				"label": "DBpedia",
				"uri": "http://dbpedia.org/sparql",
				"description": "DBpedia.org is a community effort to extract structured information from Wikipedia and to make this information available on the Web. DBpedia allows you to ask sophisticated queries against Wikipedia and to link other datasets on the Web to Wikipedia data."
			}
	    ]
	},
	{
		"labels": ["CC BY-NC"],
		"licensing_terms": ["https://creativecommons.org/licenses/by-nc/3.0/legalcode"],
	    "permissions": ["Distribution", "Reproduction", "DerivativeWorks", "modify"],
	    "obligations": ["Attribution", "Notice"],
	    "prohibitions": ["CommericalUse"],
	    "resources": [
	    	{
				"label": "TAXREF-LD: Linked Data French Taxonomic Register",
				"uri": "http://taxref.mnhn.fr/sparql",
				"description": "TAXREF-LD is the Linked Data representation of TAXREF, the French national taxonomical register for fauna, flora and fungus, that covers mainland France and overseas territories. It accounts for over 500000 scientific names."
			},
			{
				"label": "EARTh",
				"uri": "http://linkeddata.ge.imati.cnr.it:8890/sparql",
				"description": "The Environmental Applications Reference Thesaurus (EARTh) has been compiled and is maintained by the CNR-IIA-EKOLab to facilitate the indexing, retrieval, harmonizing and integration of human- and machine-readable environmental information from disparate sources, across the cultural and linguistic barriers. Ownership of such material always remains with the CNR-IIA-EKOLab."
			},
			{
				"label": "US Political Violence",
				"uri": "http://dacura.cs.tcd.ie/sparql",
				"description": "A dataset comprising reports of political violence events causing death between 1780 and 2010 in the United States of America."
			}
	    ]
	},
	{
		"labels": ["CC BY-NC-SA"],
		"licensing_terms": ["https://creativecommons.org/licenses/by-nc-sa/3.0/legalcode"],
	    "permissions": ["Distribution", "Reproduction", "DerivativeWorks", "modify"],
	    "obligations": ["Attribution", "Notice", "ShareAlike"],
	    "prohibitions": ["CommericalUse"],
	    "resources": [
	    	{
				"label": "LinkedCT",
				"uri": "http://data.linkedct.org/sparql",
				"description": "Linked Clinical Trials."
			},
			{
				"label": "Mathematics Subject Classification",
				"uri": "http://sparql.msc2010.org/",
				"description": "The Mathematics Subject Classification (MSC2010)."
			}
	    ]
	},
	{
		"labels": ["CC BY-NC-ND"],
		"licensing_terms": ["https://creativecommons.org/licenses/by-nc-nd/3.0/legalcode"],
	    "permissions": ["Distribution", "Reproduction"],
	    "obligations": ["Attribution", "Notice"],
	    "prohibitions": ["CommericalUse", "DerivativeWorks", "modify"],
	    "resources": [
	    	{
				"label": "Demand Data at Province",
				"uri": "https://data.opendatasoft.com/explore/api/tpf/demand-data-at-province@kapsarc",
				"description": "This dataset contains China Demand Data at Province 2004-2017 Power Knowledge Thinker Demand, Export API data for more datasets to advance energy economics research."
			},
			{
				"label": "Power Supply and Consumption",
				"uri": "https://data.opendatasoft.com/explore/api/tpf/power-supply-and-consumption0@kapsarc",
				"description": "This dataset contains China Power Supply and Consumption 2006-2017 Power Knowledge Thinker , Export API data for more datasets to advance energy economics research."
			},
			{
				"label": "Coal Production By Province",
				"uri": "https://data.opendatasoft.com/explore/api/tpf/coal-production-by-provinces@kapsarc",
				"description": "Coal production by month from PK Thinker."
			},
			{
				"label": "Extra-Vehicular Activity",
				"uri": "https://data.opendatasoft.com/explore/api/tpf/extra-vehicular-activity@datastro",
				"description": "Activities done by an astronaut outside a spacecraft beyond the Earth'\''s appreciable atmosphere. Data for US and Russia."
			}
	    ]
	},
	{
		"labels": ["GFDL"],
		"licensing_terms": ["https://www.gnu.org/licenses/fdl"],
	    "permissions": ["Distribution", "Reproduction", "CommericalUse", "DerivativeWorks", "modify"],
	    "obligations": ["Attribution", "Notice", "ShareAlike"],
	    "prohibitions": [],
	    "resources": [
	    	{
				"label": "Russian Universities Specialities",
				"uri": "https://datahub.ckan.io/dataset/c8bb2280-5919-4fbb-85b1-52d03d403e21/resource/38b05231-715e-411e-9c04-4752d08dfa6d/download/specialitydatahub.rdf",
				"description": "This ontology describes a degree of higher education and the direction of bachelor'\''s and master'\''s degrees in the Russian Federation and their compliance with the various official lists. It is assumed that a given ontology can be used in various applications of the Semantic Web in Russian higher education."
			},
			{
				"label": "Alpine Ski Racers of Austria",
				"uri": "http://vocabulary.semantic-web.at/PoolParty/sparql/AustrianSkiTeam",
				"description": "Austrian top-skiers active in world cup."
			}
	    ]
	}


]'
