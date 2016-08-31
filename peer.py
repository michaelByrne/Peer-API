# Author: Michael Byrne
# Assignment 3_2
# CS 496
# Sources: example code at github.com/GoogleCloudPlatform/endpoints-proto-datastore



import endpoints

from google.appengine.ext import ndb
from protorpc import remote

from endpoints_proto_datastore.ndb import EndpointsModel


#models for Article and Annotation

class Article(EndpointsModel):
    title = ndb.StringProperty(required='true')
    pulls = ndb.IntegerProperty()
    arxId = ndb.StringProperty(required='true')
    created = ndb.DateTimeProperty(auto_now_add=True)
    annotations = ndb.IntegerProperty(repeated='true')

    #annotations

class Annotation(EndpointsModel):
    arxId = ndb.StringProperty()
    text = ndb.StringProperty()
    id = ndb.IntegerProperty(required='true')
    #author
    line = ndb.IntegerProperty()
    created = ndb.DateTimeProperty(auto_now_add=True)

#begin API definition, invoke endpoints API decorator

@endpoints.api(name='pgapi', version='v1', description='Peer Genius API')
class PeerGApi(remote.Service):   #extends remote
    @Article.method(path='article', http_method='POST', name='article.insert')
    def ArticleInsert(self, article):
        # here we insert a new article into the database
        article.put()
        return article

    #query_method as defined in endpoints proto datastore: a useful model that creates query objects
    #from passed in metadata. here it just returns all articles.
    @Article.query_method(path='articles', name='article.list')
    def ListArticles(self, query):
        # Here we return every article in the database with no filtering applied
        return query


    #inserts new annotation, matches article and adds annotation id to match
    @Annotation.method(path='annotation', http_method='POST', name='annotation.insert')
    def AnnotationInsert(self, annotation):
        # add new annotation to database
        new_key = annotation.put()
        annotation.id = new_key.id()
        annotation.put()
        parent = Article.query().filter(Article.arxId == annotation.arxId)
        p = parent.get()
        p.annotations.append(annotation.id)
        p.put()
        return annotation

    #deletes annotation, matches article. deletes id from article annotations
    @Annotation.method(http_method='DELETE',
                       path='delete/{id}',
                       name='annotation.delete')
    def AnnotationDelete(self,request):
        if (request):
            annote = Annotation.get_by_id(request.id)
            parent = Article.query().filter(Article.arxId == annote.arxId)
            p = parent.get()
            if request.id in p.annotations:
                index = p.annotations.index(request.id)
                del p.annotations[index]
                p.put()
            annote.key.delete()
            return request
        else:
            raise endpoints.NotFoundException('entity does not exist // no action')

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



    #gets annotation by id. decorator takes query field metadata and returns query object
    @Annotation.query_method(query_fields=('id',),
                          path='byid/{id}', name='annotation.list')
    def AnnotationById(self, query):
        if (query):
            return query
        else:
            raise endpoints.NotFoundException('Entity does not exist')

    #insert method allows for adding multiple annotations at a time. specifies an endpoints message class.
    @Annotation.method(request_message=Annotation.ProtoCollection(),
                    response_message=Annotation.ProtoCollection(),
                    user_required=True,
                    path='annote_multi',
                    name='annotation.insert_multi')
    def AnnoteMultiInsert(self, annote_collection):
        entities = [Annotation.FromMessage(item_msg)
                    for item_msg in annote_collection.items]
        ndb.put_multi(entities)
        response_items = [entity.ToMessage() for entity in entities]
        response_collection = Annotation.ProtoCollection()(items=response_items)
        return response_collection

    #update method finds annotation by id and updates properties with supplies parameters
    @Annotation.method(http_method='PUT',
                  path='update/{id}',
                  name='annotation.update')
    def AnnotationUpdate(self, request):
        entity = Annotation.get_by_id(request.id)
        if (entity):
            entity.arxId = request.arxId
            entity.text = request.text
            entity.created = request.created
            entity.put()
            return entity
        else:
            raise endpoints.NotFoundException('entity does not exist // no action')







application = endpoints.api_server([PeerGApi], restricted=False)













