import json

from django.db import models
from django.http import JsonResponse


class FlexibleJsonEncoder(json.JSONEncoder):
    '''JSON encoder that calls __serialize__ on models to get an OrderedDict.

    Currently supports model instances and enumerables (such as lists, querysets).

    Example:
        ```
        class Article(models.Model):
            ...
            def __serialize__(self):
                return OrderedDict(title=self.title, content=self.content)

        articles = Article.objects.all()
        return JsonResponse(articles, encoder=FlexibleJsonEncoder, safe=False)
        ```
    '''
    def default(self, o):
        if isinstance(o, models.Model):
            if callable(getattr(o, '__serialize__')):
                return o.__serialize__()
            return super().default(o)

        try:
            iterable = iter(o)
        except TypeError:
            pass
        else:
            return [self.default(item) for item in iterable]

        return super().default(o)


def ApiResponse(data, **kwargs):
    '''Wrapper for JsonResponse that uses FlexibleJsonEncoder and UTF-8'''
    kwargs.setdefault('json_dumps_params', {})
    kwargs['json_dumps_params']['ensure_ascii'] = False
    kwargs['encoder'] = FlexibleJsonEncoder
    kwargs['safe'] = False
    return JsonResponse(data, **kwargs)

def ApiMessage(msg, **kwargs):
    '''Returns JSON response {'message': msg} while maintaining UTF-8 encoding'''
    kwargs.setdefault('json_dumps_params', {})
    kwargs['json_dumps_params']['ensure_ascii'] = False
    return JsonResponse({'message': msg}, **kwargs)
