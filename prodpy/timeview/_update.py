import os

import numpy
import pandas

import streamlit

from ._outlook import Outlook

from ._itemview import ItemView

class Update:

	@streamlit.cache_data
	def load_data(file):

		frame = pandas.DataFrame() # DEFAULT

		if file is None:
			return Outlook(frame)

		fmt = os.path.splitext(file.name)[1]

		if fmt == '.xlsx':
			frame = pandas.read_excel(file,sheet_name=0)
		elif fmt == '.csv':
			frame = pandas.read_csv(file)
		elif fmt == '.json':
			frame = pandas.read_json(file)
		elif fmt == '.txt':
			frame = pandas.read_fwf(file,widths=col_widths,header=None)
		elif fmt == '.dta':
			frame = pandas.read_stata(file)
		elif fmt == '.orc':
			frame = pandas.read_orc(file)

		return Outlook(frame)

	@staticmethod
	def load_view(state,data:Outlook):

		if Update.NoneFlag(state,'datehead','ratehead','nominals'):
			frame = pandas.DataFrame()
		else:
			frame = data(state.datehead).view(*state.nominals)

		return ItemView(frame)

	@staticmethod
	def load_frame(state,view:ItemView):

		if Update.NoneFlag(state,'itemname'):
			frame,title,limit = pandas.DataFrame(),'None',state.datelim
		else:
			frame,title,limit = view.filter(state.itemname)

		return frame,title,limit

	@staticmethod
	def NoneFlag(state,*args):

		for arg in args:
			if state[arg] is None:
				return True
			if len(state[arg])==0:
				return True

		return False