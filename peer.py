# Author: Michael Byrne
# Assignment 3_2
# CS 496
# Sources: example code at github.com/GoogleCloudPlatform/endpoints-proto-datastore



import endpoints

from google.appengine.ext import ndb
from protorpc import remote

from endpoints_proto_datastore.ndb import EndpointsModel
from google.appengine.api import users

CLIENT_ID = 'YOUR-CLIENT-ID'


class Article(EndpointsModel):
    title = ndb.StringProperty()
    image_url = ndb.StringProperty()
    public = ndb.BooleanProperty()
    user = ndb.StringProperty()
    db_id = ndb.StringProperty()

    #annotations


#begin API definition, invoke endpoints API decorator

@endpoints.api(name='pgapi', version='v1', description='Peer Genius API',allowed_client_ids=[CLIENT_ID, endpoints.API_EXPLORER_CLIENT_ID])
class PeerGApi(remote.Service):   #extends remote
    @Article.method(path='article', http_method='POST', name='article.insert')
    def ArticleInsert(self, article):
        # here we insert a new article into the database
        key = article.put()
        id = key.id()
        article.db_id = str(id)
        print(article.db_id)
        article.put()
        return article

    #query_method as defined in endpoints proto datastore: a useful model that creates query objects
    #from passed in metadata. here it just returns all articles.
    @Article.query_method(path='allarticles', name='article.all',allowed_client_ids=[CLIENT_ID, endpoints.API_EXPLORER_CLIENT_ID])
    def ListArticles(self, query):
        # Here we return every article in the database with no filtering applied
        return query


    #delete article, currently fails
    @Article.method(http_method='DELETE',
                       path='nuke/{id}',
                       name='article.delete')
    def ArticleDelete(self, request):
        if (request):
            article = Article.get_by_id(request.id)
            article.key.delete()
            return request
        else:
            raise endpoints.NotFoundException('entity does not exist // no action')












application = endpoints.api_server([PeerGApi], restricted=False)













