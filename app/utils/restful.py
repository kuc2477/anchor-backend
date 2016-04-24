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

    def get_filtered(self, instances):
        return instances

    def get_link(self, current_page):
        return '{}?{}={}'.format(
            self.url,
            self.pagination_key,
            current_page + 1
        )

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument(self.pagination_key, type=int)
        page = parser.parse_args()[self.pagination_key] or 0

        instances = self.get_query()\
            .limit(self.pagination_size)\
            .offset(self.pagination_size * page)\
            .all()

        filtered = self.get_filtered(instances)

        schema = self.schema(many=True)
        return schema.dump(filtered).data, 200, (
            {self.link_key: self.get_link(page)}
            if len(instances) >= self.pagination_size
            else None
        )

    @property
    def url(self):
        return url_for('.{}'.format(self.__class__.__name__.lower()))
