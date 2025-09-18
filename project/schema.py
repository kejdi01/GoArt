import graphene

from application.profiles import schema as profile_schema


class Query(profile_schema.Query, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query)