import os
import sys
import math

import array

import statistics

from matplotlib import rc
rc('font', family='Droid Sans', weight='normal', size=14)

import matplotlib.pyplot as plt



class WikiGraph:

	def load_from_file(self, filename):
		print('Загружаю граф из файла' + filename)
		with open(filename) as f:
			(n, _nlinks) = (map(int, f.readline().split()))
			self._titles = []
			steps = 2854434 / 6  
			self._sizes = array.array('L', [0]*n)
			self._links = array.array('L', [0]*_nlinks)
			self._redirect = array.array('B', [0]*n)
			self._offset = array.array('L', [0]*(n+1))
			n_ls = 0 
			for i in range(n):
				self._titles.append(f.readline().rstrip())
				(size, redirect, ls) = (map(int, f.readline().split()))
				self._sizes[i] = size
				self._redirect[i] = redirect
				for j in range(n_ls, n_ls + ls):
					self._links[j] = int(str(f.readline()))
				n_ls += ls
				self._offset[i+1] = self._offset[i] + ls
				if i % steps == 0:
					print ('*', end = ' ')
			print('Done!')
		print('Граф загружен')


	def get_number_of_links_from(self, _id):
		return len(self._links[self._offset[_id]:self._offset[_id+1]])

	def get_links_from(self, _id):
		return self._links[self._offset[_id]:self._offset[_id+1]]

	def get_id(self, title):
		for i in range(len(self._titles)):
			if self._titles[i] == title:
				return(i)


	def get_number_of_pages(self):
		return len(self._titles)

	def is_redirect(self, _id):
		return self._redirect[_id]

	def get_title(self, _id):
		return self._titles[_id]

	def get_page_size(self, _id):
		return self._sizes[_id]


	def hist(fname, data, bins, xlabel, ylabel, title, facecolor='green', alpha=0.5, transparent=True, **kwargs):
		plt.clf()
       

def analyse_links_from_page(G):
	numlinks_from = list(map(G.get_number_of_links_from, range(G.get_number_of_pages())))
	Max = max(numlinks_from)
	Min = min(numlinks_from)
	Mx = sum(x == Max for x in numlinks_from)
	Mn = sum(x == Min for x in numlinks_from)
	print("Минимальное количество ссылок из статьи:", Min)
	print("Количество статей с минимальным количеством ссылок:", Mn)
	print("Максимальное количество ссылок из статьи:", Max)
	print("Количество статей с максимальным количеством ссылок:", Mx)
	for i in range(G.get_number_of_pages()):
		if G.get_number_of_links_from(i) == Max:
			break
	print("Статья с наибольшим количеством ссылок:", G.get_title(i))


if __name__ == '__main__':

	if len(sys.argv) != 2:
		print('Использование: wiki_stats.py <файл с графом статей>')
		sys.exit(-1)

	if os.path.isfile(sys.argv[1]):
		wg = WikiGraph()
		wg.load_from_file(sys.argv[1])
		analyse_links_from_page(wg)
	else:
		print('Файл с графом не найден')
		sys.exit(-1)
