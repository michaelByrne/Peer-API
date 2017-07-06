# Peer-Genius-API
A RESTful API using Google Endpoints/ProtoRPC adding a view layer and annotation functionality to the arXiv database.

This is a project I made for a class in 2016 demonstrating usage of Google Endpoints. Ostensibly, its function is to provide a view layer to the arXiv.org server such that users can make comments on articles and vote articles up or down. It provides model classes for articles and article annotations (comments) per the inherited EndpointsModel class. It then provides definitions for a RESTful API including methods for matching arXiv articles to annotations. 
