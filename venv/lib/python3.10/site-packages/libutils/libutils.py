import os
import sys

def real_path(filename):
	return os.path.dirname(os.path.abspath(sys.argv[0])) + f"/{filename}"

def filter(self, data):
	return list(set([x.strip() for x in data if x.strip() and not x.strip().startswith('#')]))