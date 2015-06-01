import datetime
from haystack import indexes
from prose.models import Prose

class ProseIndex( indexes.SearchIndex, indexes.Indexable ):
	text = indexes.CharField( document = True, use_template = True )
	author = indexes.CharField( model_attr = 'user' )
	pub_date = indexes.DateTimeField( model_attr = 'pub_date' )
	
	def get_model(self):
		return Prose
		
	def index_queryset( self, using = None ):
		"""Used when the entire index for model is updated."""
		return self.get_model().objects.filter( pub_date__lte = datetime.datetime.now() )