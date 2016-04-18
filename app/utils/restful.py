from flask import url_for
from flask.ext.restful import Resource, reqparse


class PaginatedResource(Resource):
    link_key = 'Link'
    pagination_key = 'page'
    pagination_size = 10

    model = None
    schema = None
    order_by = 'id'

    def get_query(self):
        return self.model.query

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument(self.pagination_key, type=int)
        page = parser.parse_args()[self.pagination_key] or 0

        instances = self.get_query()\
            .limit(self.pagination_size)\
            .offset(self.pagination_size * page)\
            .all()

        schema = self.schema(many=True)
        link = '{}?{}={}'.format(self.url, self.pagination_key, page + 1)
        return schema.dump(instances).data, 200, (
            {self.link_key: link} if len(instances) >= self.pagination_size
            else None
        )

    @property
    def url(self):
        return url_for('.{}'.format(self.__class__.__name__.lower()))
