from django.db.models import QuerySet
class LimitedQueryMixin:
    """
    associate with model classes to 
    limit query and increase performance.
    """
    @classmethod
    def limit_query(cls,query:QuerySet,offset=0,percent=.2):
        """
        yeild query each time returns percent
        of total items. if items are less than 10 
        it returns query.
        """
        count = query.count()
        if count > 10:
            step = count * percent
            for limit in range(offset,count,step):
                yield query[offset:limit]
