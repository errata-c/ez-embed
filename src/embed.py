import sys

#	Load a manifest file.
#	Run through it line by line, assume each line is either blank, a comment, or a filepath.
#	All filepaths in the manifest are interpreted as relative to the location of the manifest, or a working directory.
#	Each file will be loaded as binary, put into a character array, and a size will be stored with it.
#	A header will be generated defining the array of embedded files, and a cmake target will be created to encapsulate it.


#	Usage
#	 cembed -i <manifest_file> -o <output_file>

#	Options
#	 --version                   = Print a version string
#	 --help                      = Print this help string
#	 --output,-o    <name>       = (REQUIRED) Specify the name of the source file to generate, expects something like {name}.c
#	 --input,-i     <manifest>   = (REQUIRED) The location of the manifest file to use, must be an actual filename
#	 --header       <name>       = Specify the name of the header file to generate, otherwise inferred from output name
#	 --dir,-d       <directory>  = Change the working directory to source manifest files from
#	 --namespace,-n <name>       = Specify a custom namespace for the embedded files

version_str = "cembed version 0.1.0"

help_str = """Usage
	cembed - i <manifest_file> -o <output_file>

	Options
	 --version = Print a version string
	 --help = Print this help string
	 --output,-o <name> = (REQUIRED) Specify the name of the source file to generate, expects something like {name}.c
	 --input,-i  <manifest> = (REQUIRED) The location of the manifest file to use, must be an actual filename
	 --header    <name> = Specify the name of the header file to generate, otherwise inferred from output name
	 --dir,-d    <directory> = Change the working directory to source manifest files from"""

class Token:
	def __init__(self, kind, text):
		self.kind = kind
		self.text = text

class Node:
	def __init__(self, kind, data):
		self.kind = kind
		self.data = data

def lex(text):
	if len(text) == 0:
		raise Exception("Empty text argument passed to lex function!")
	elif text[0] == '-':
		if text == "--help":
			return Token(kind="help", text=None)
		elif text == "-i" or text == "--input":
			return Token(kind="input", text=None)
		elif text == "-o" or text == "--output":
			return Token(kind="output", text=None)
		elif text == "-d" or text == "--dir":
			return Token(kind="directory", text=None)
		elif text == "-i" or text == "--input":
			return Token(kind="input", text=None)
		elif text == "--header":
			return Token(kind="header", text=None)
		elif text == "--version":
			return Token(kind="version", text=None)
		else:
			raise Exception("Invalid argument for cembed found: '{arg}'".format(arg = text))
	else:
		return Token(kind="text", text=text)

def parse(args):
	toks = []
	for arg in args:
		toks.append(lex(arg))

	nodes = []
	toks.reverse()
	while len(toks) != 0:
		tok = toks.pop()
		if tok.kind == "help":
			nodes.append(Node(kind="help", data=None))

		elif tok.kind == "input":
			ntok = toks.pop()
			if ntok.kind == "text":
				nodes.append(Node(kind="input", data=ntok.text))
			else:
				raise Exception("Expected a text argument after -i,--input!")

		elif tok.kind == "output":
			ntok = toks.pop()
			if ntok.kind == "text":
				nodes.append(Node(kind="output", data=ntok.text))
			else:
				raise Exception("Expected a text argument after -o,--output!")

		elif tok.kind == "directory":
			ntok = toks.pop()
			if ntok.kind == "text":
				nodes.append(Node(kind="directory", data=ntok.text))
			else:
				raise Exception("Expected a text argument after -d,--dir!")

		elif tok.kind == "header":
			ntok = toks.pop()
			if ntok.kind == "text":
				nodes.append(Node(kind="header", data=ntok.text))
			else:
				raise Exception("Expected a text argument after -h,--header!")

		elif tok.kind == "version":
			nodes.append(Node(kind="", data=version_str))
		elif tok.kind == "text":
			raise Exception("Unexpected text argument for cembed found: '{arg}'".format(arg=tok.text))

	return nodes	

if __name__ == "__main__":
	args = sys.argv.copy()
	args.pop(0)

	nodes = parse(args)
