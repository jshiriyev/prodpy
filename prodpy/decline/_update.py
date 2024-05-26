from ._model import Model

from ._analysis import Analysis

class Update():

	@staticmethod
	def load_analysis(state):

		return Analysis(
			state.datehead,
			state.ratehead,
			)

	@staticmethod
	def slider(state):

		state['optimize'] = True

	@staticmethod
	def load_opacity(state,view):

		if view.frame.empty:
			return

		bools = Analysis.get_bools(
			view.dates,*state.estimate
			)

		return bools*0.7+0.3

	@staticmethod
	def mode(state):

		state['exponent'] = Model.get_exponent(state.mode)
		state['optimize'] = True

	@staticmethod
	def exponent(state):

		state['mode'] =  Model.get_mode(state.exponent)
		state['optimize'] = True

	@staticmethod
	def get_best_model(state,analysis):

		if Update.flag(state,'estimate','mode','exponent'):
			return

		return analysis.fit(
			    mode = state.mode,
			exponent = state.exponent,
			   start = state.estimate[0],
				 end = state.estimate[1],
			)

	@staticmethod
	def load_model(state,analysis):

		if not state.optimize:
			return

		if analysis.frame.empty:
			return

		model = Update.get_best_model(state,analysis)

		state['rate0'] = f'{model.rate0:f}'

		state['decline0'] = f'{model.decline0:f}'

	@staticmethod
	def attributes(state):

		state['optimize'] = False

	@staticmethod
	def get_user_model(state):

		if Update.flag(state,'estimate','mode','exponent','rate0','decline0'):
			return

		return Model(
				mode = state.mode,
			exponent = state.exponent,
			   date0 = state.date0,
			   rate0 = float(state.rate0),
			decline0 = float(state.decline0),
			)

	@staticmethod
	def load_curve(state,analysis):

		if analysis.frame.empty:
			return

		model = Update.get_user_model(state)

		start,end = state.estimate

		return analysis.run(model,start=start,end=end,periods=30)

	@staticmethod
	def load_forecast(state,analysis):

		model = Update.get_user_model(state)

		start,end = state.forecast

		return analysis.run(model,start=start,end=end,periods=30)

	@staticmethod
	def load_download(state,analysis):
		"""IT SHOULD RETURN PANDAS DATAFRAME"""

		start,end = state.forecast

		datetimes = analysis.get_datetimes(
			start=start,end=end,periods=30
			)

		for itemname,model in state.models.items():

			days = analysis.get_days(
				datetimes,start=model.date0
				)

			rates = analysis.get_rates(
				model,days
				)

			forecast['items'] = items # CORRECT THIS
			forecast['dates'] = dates
			forecast['rates'] = rates

		return forecast

	@staticmethod
	def flag(state,*args):

		for arg in args:
			if state[arg] is None:
				return True

		return False