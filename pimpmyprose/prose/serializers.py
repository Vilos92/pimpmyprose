from rest_framework import serializers
from models import Prose, Pimp

class ProseSerializer( serializers.ModelSerializer ):
    username = serializers.ReadOnlyField( source = 'user.username' )
    pimp_set = serializers.HyperlinkedRelatedField( many = True, view_name = 'pimp-detail', read_only = True )

    class Meta:
        model = Prose
        fields = ( 'id', 'username', 'prose_text', 'pub_date', 'pimp_set', 'pimpScoreSum' )

class PimpSerializer( serializers.ModelSerializer ):
    username = serializers.ReadOnlyField( source = 'user.username' )
    user_id = serializers.ReadOnlyField( source = 'user.id' )
    prose = serializers.HyperlinkedRelatedField( view_name = 'prose-detail', read_only = True )
    upvotes = serializers.ReadOnlyField( source = 'upvotes.count' )
    downvotes = serializers.ReadOnlyField( source = 'downvotes.count' )

    class Meta:
        model = Pimp
        fields = ( 'id', 'username', 'user_id', 'prose', 'pimp_text', 'pub_date', 'upvotes', 'downvotes', 'percentMatch' )
