# imagescrape
# An argparse script that scrapes google image search for images and saves
# to designated folder.
# Parse will accept the search term. 
# (C) 2017 Ali Rassolie 
try:
	from bs4 import BeautifulSoup as bs4
except Exception as e:
	print(e)
try: 
	from urllib.request import urlopen, Request, urlretrieve
except: 
	print("Make sure that you have the urllib donwloaded")
import argparse as ap
import os

class ImageScrape:
	def __init__(self, *args, **kwargs):
		print("\n\n\nImageScrape\n(C) 2017 Ali Rassolie\n")
	# Creating the argparse parameters
		self.arguments()
		self.search()
		self.collection_handler()
	

	def arguments(self):
	# The argparse arguments necessary for the script
		self.the_arguments = ap.ArgumentParser(
			prog="ImageScraper",
			description="""This scraper will grab images from
							Google images and store them to 
							designated folder""")
		
		self.the_arguments.add_argument("-s", "--search",  help="The search-term", nargs=1)
		self.the_arguments.add_argument("-d", "--destination", help="Specify destination folder, enclosing in quotes",  nargs=1)
		self.the_arguments.add_argument("-l","--limit", help="The amount of images", nargs=1)

		
	# Storing the parsed arguments
		self.opts = self.the_arguments.parse_args()
		
		try:
			temporary_opts = (self.opts.search[0], self.opts.destination[0], self.opts.limit[0])
			print("Search term: {}\nDestination folder: {}\nNumber of images: {}\n\n".format(temporary_opts))
		
		except Exception as e:
			print(e)

	def search(self):
	# Performing the search, having used the parsed arguments of user
		self.search_term = self.opts.search[0]
		base_url = "https://www.google.se/search?hl=sv&site=imghp&tbm=isch&source=hp&q="
		header = {'User-Agent': 'Mozilla/5.0'}
		url = base_url + self.search_term
		collected_data_type = "html.parser"
		
	# Requesting the data from given url using provided header
		request = Request(url, headers=header)
		html = urlopen(request)
		self.soup = bs4(html, collected_data_type)
	
	def collection_handler(self):
		try:
			self.destination = os.path.abspath(self.opts.destination[0])
			print("""\nWorking\n
			*************************************************************************************************	""")
		except:
			self.destination = os.getcwd()
			print("""\n\nAs the file-destination was not defined, we will use the current directory to save the images\n
				***********************\n""")

		new_dir = self.destination + "\\images\\" 
		if not os.path.exists(new_dir):
			os.makedirs(new_dir)
			print("Made a new directory at: {}\n".format(new_dir))
		
		self.limit = int(self.opts.limit[0])
		imgs = self.soup.find_all("img", alt="Bildresultat för {}".format(self.search_term), limit=self.limit)
		
		pos = 0 
		for i in imgs:
			img_url = imgs[pos]["src"]
			filename = "image{}.jpg".format(int(pos))
			full_filename = os.path.join(new_dir, filename)
			print("Saving to: {}\nImage url: {}\n".format(full_filename,  img_url,))
			urlretrieve(img_url, full_filename)
			pos += 1

if __name__ == '__main__':
	session_1 = ImageScrape()