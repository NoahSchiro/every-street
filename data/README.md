# The data
I was interested in creating a general method that is applicable for any given city / area of interest, not just my hometown. The best (open source!) method I could find for collecting this kind of data is a website called [Open Street Map](https://www.openstreetmap.org/). In short, you can think of this website as a sort of wikipedia but for mapping. It's maintained by an active and vibrant community of mappers who are dedicated to reporting accurate information about... Well anything you can find on a map!

The feature that interests this project the most is the "export" feature. It's in the top left of the screen and manually let's you select a box that you can export a custom file type called .osm. More on that later.

![](./assets/osmExportExample.png)

In the example above, you can see we are trying to select San Francisco. There are some issues with this, namely that we can only draw a rectangular box. Because of this, we are clipping into Alcatraz Island a bit in the upper right side. Because of this, we are going to have to do some (manually) processing to clean up the file we export.

Clicking export will generate a .osm file. These are an extension on the XML format, and should be painless to parse because of that. This file type is covered by a unique license, the [ODbL](https://opendatacommons.org/licenses/odbl/1-0/). Because this repo is covered under the GPL, I will not include any .osm files, but if you clone this repo, they are generally stored in "./data/". If you are interested in learning more about the .osm file format (which will be important for parsing it into a graph), more information can be found [here](https://wiki.openstreetmap.org/wiki/OSM_XML).

## Ways
There are a few paths that need to be removed which are not "streets"

- Anything that doesn't have the tag with key value "highway." Even with the "highway" key, there are some values we want to pay attention to and some we don't want to pay attention to
	- Save
		- primary_link
		- secondary
		- motorway_link
		- service 
		- residential
		- motorway
		- unclassified (a fun category. I am sure this will cause headaches later)
		- primary
		- tertiary
	- Don't save 
		- footway
		- raceway
		- path
- Anything that has the tag key-value pair "access" -> "private." or "service" -> "driveway". We aren't keen to go anywhere we are not supposed to!
- Anything that has the tag key value of "service" may not have
	- parking_aisle
	- driveway
	- emergency_access

If you are trying this for your own city, you might want to try and see if your .osm file has any tag values which are not listed here. I am sure that there might be more weird features in this file format which might not be covered above.

Filtering the ways on these restrictions reduces the number of streets from 1414 to 366. This should make things a lot easier for the route inspection algorithm.

## Nodes
With our filtered ways, filtering the nodes we need is very simple. We can just collect every node referenced by a way in a set. Then loop through the nodes and only take the ones that are referenced by some way.

This reduces the number of nodes from 11120 to 3334. Again, this will make things significantly easier on the algorithm.