import numpy

from ._genmod import GenModel

from ._exponential import Exponential

from ._hyperbolic import Hyperbolic

from ._harmonic import Harmonic

class Arps(GenModel):

	def __init__(self,*args,**kwargs):

		super(Arps,self).__init__(*args,**kwargs)

	def __model(self):

		if self.exponent==0.:
			return Exponential(*self.props)
		elif self.exponent==1.:
			return Harmonic(*self.props)
		elif self.exponent>0. and self.exponent<1.:
			return Hyperbolic(*self.props)

	def ycal(self,x:numpy.ndarray):

		return self.__model.ycal(x)

	def ycum(self,x:numpy.ndarray):

		return self.__model.ycum(x)

	def params(self,x:numpy.ndarray,yobs:numpy.ndarray,x0:float=None):

		y0,D0,linear = self.__model.params(x,yobs)

		nonlinear = NonLinResult(D0,y0,self.rvalue(x,yobs))

		return Score(linear,nonlinear)

	def rvalue(self,x:numpy.ndarray,yobs:numpy.ndarray):

		ssres = numpy.nansum((yobs-self.ycal(x))**2)
		sstot = numpy.nansum((yobs-numpy.nanmean(yobs))**2)

		return 1-ssres/sstot

