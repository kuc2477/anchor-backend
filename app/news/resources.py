from sqlalchemy import sql
from flask.ext.login import current_user
from flask.ext.restful import (
    Resource,
    abort,
)
from .models import (
    News,
    NewsSchema,
)
from ..constants import LATEST_NEWS_PAGINATION_SIZE
from ..schedules.models import Schedule
from ..utils.restful import PaginatedResource
from ..extensions import db


class NewsResource(Resource):
    def get(self, id):
        news = News.query.get_or_404(id)
        return news.serialized

    def delete(self, id):
        news = Schedule.query.get_or_404(id)
        db.session.delete(news)
        db.session.commit()
        return '', 204


class NewsListResource(PaginatedResource):
    model = News
    schema = NewsSchema
    pagination_size = 20

    def get_query(self):
        if current_user.is_anonymous:
            return News.query.filter(sql.false())
        else:
            return News.query\
                .join(Schedule)\
                .filter(Schedule.owner_id == current_user.id)\
                .order_by(sql.desc(News.created))

    def get_filtered(self, instances):
        return [
            n for n in instances if
            (n.current_user_rating is None or n.current_user_rating) and
            n.image
        ]


class LatestListResource(Resource):
    def get(self):
        if current_user.is_anonymous:
            query = News.query.filter(sql.false())
        else:
            query = News.query.join(Schedule)\
                .filter(Schedule.owner_id == current_user.id)\
                .order_by(sql.desc(News.created))\
                .limit(LATEST_NEWS_PAGINATION_SIZE)\

        instances = query.all()
        filtered = [n for n in instances if
                    n.current_user_rating is None or n.current_user_rating]

        schema = NewsSchema(many=True, exclude='content')
        return schema.dump(filtered).data


class RecomListResource(Resource):
    def get(self):
        if current_user.is_anonymous:
            abort(400)

        recommendations = current_user.get_recommendations()
        schema = NewsSchema(many=True, exclude='content')
        return schema.dump(recommendations).data