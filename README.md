# ABOUT

We are creating an open-source (MIT license for code, CC BY-SA 4.0 for database) map/database/API for all the innovation spaces everywhere! This Atlas will merge existing lists of community innovation spaces from disparate maps onto a single, open-source platform— with an API so our data can be easily shared across other platforms. A tagging system will enable all spaces to share goals and find collaborators across interests such as electronic waste, prosthetics, 3D printing, primary education, green materials, water purification, etc.

We have three primary criteria for including a given “community innovation space” on our map:

1. Community: a physical space or event that is eager to collaborate with others-- it must be either open to the public or available for outside partnerships

2. Technology: utilizes old and/or new technology, including hardware, software, metal-working, handicrafts, repurposed trash, farming, etc.

3. Innovation: promotes creativity and nurtures new ideas

From July through December 2016, our team will develop, test, and then implement the platform to collaboratively host all these spaces.

## General details:
- Visual map (split into two maps) of all spaces and events: http://anansegroup.com/mapping.html
- Simple visual map of all spaces and events: http://anansegroup.github.io/ananse-map/
- Slide-deck with more info about our project: http://www.slideshare.net/annawaldmanbrown/atlas-of-innovation-spaces
- Our team: http://anansegroup.com

This is an open source and not-for-profit initiative sponsored by Deutsche Gesellschaft für Internationale Zusammenarbeit (GIZ) GmbH, the Fab Foundation, and the American Society of Mechanical Engineers (ASME).

## Collaborators:
- Our primary partners are the Open Movement: http://open.co
- We're working with rrbaker's Maker.json repo: https://github.com/rrbaker/maker.json
- Many thanks to the awesome APIs from Makery and Fablabs.io !
- Our other mapping partners include Global Innovation Gathering (GIG), Maker Media, World Bank, hackerspaces.org, Hacedores, Bongohive, Superhero Spaces, and others

## Prospective Collaborators:
- SpaceAPI: https://github.com/slopjong/OpenSpaceDirectory
- Python library for makerspaces: https://github.com/openp2pdesign/PyMakerspaces
- The Maker Map: https://github.com/hwstartup/TheMakerMap.com
- https://github.com/codeisland/makermap

To join us, please email our team at anansegroup@gmail.com

## Steps to get ready with the project:
- git clone https://github.com/AnanseGroup/atlas_of_innovation
- install vagrant and virtualbox
- on the project root run 'vagrant up'
- run 'vagrant ssh'
- run 'direnv allow'
- run 'atlas_db_prepare'
- run 'atlas_run'
- That's all, just check your http://localhost:8000 and you are ready.

## Steps for installing TLSH:
We use TLSH as a way of detecting spaces that may be repeated in the DB, to build 
follow this steps:
- You may need to install cmake ```sudo apt-get install cmake```
- git clone https://github.com/trendmicro/tlsh.git
- cd tlsh
- git checkout master
- run ```./make.sh```
If you get no errors, now is time to build the python extension
- cd py_ext/
- sudo python ./setup.py install
