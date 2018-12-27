import inspect
import json

from django.db import models
from django.http import JsonResponse


class FlexibleJsonEncoder(json.JSONEncoder):
    '''JSON encoder that calls __serialize__ on models to get an OrderedDict.

    Currently supports model instances and enumerables (such as lists, querysets).

    To pass arguments to the __serialize__ method, set the `serialize_args` argument
    of `json.dumps()` or any function that uses it internally.

    Example:
        ```
        class Article(models.Model):
            ...
            def __serialize__(self, capitalize_title=False):
                title = self.title
                if capitalize_title:
                    title = title.capitalize()
                return OrderedDict(title=title, content=self.content)

        articles = Article.objects.all()
        return JsonResponse(articles, encoder=FlexibleJsonEncoder, safe=False, serialize_args={
            'capitalize_title': True
        })
        ```
    '''
    def __init__(self, serialize_args=None, **kwargs):
        if serialize_args is None:
            serialize_args = {}
        self.serialize_args = serialize_args
        super().__init__(**kwargs)

    def default(self, o):
        if isinstance(o, models.Model):
            if callable(getattr(o, '__serialize__', None)):
                # For each argument in the object's __serialize__ method
                their_kwargs = inspect.signature(o.__serialize__).parameters.keys()
                # Omit kwargs that do not appear in self.serialize_kwargs
                common_kwargs = [k for k in their_kwargs if k in self.serialize_args]
                # Get the corresponding value from serialize_args
                final = {k: self.serialize_args[k] for k in common_kwargs}
                return o.__serialize__(**final)
            return super().default(o)

        try:
            iterable = iter(o)
        except TypeError:
            pass
        else:
            return [self.default(item) for item in iterable]

        return super().default(o)

def ApiResponse(data, **kwargs):
    '''Wrapper for JsonResponse that uses FlexibleJsonEncoder and UTF-8.

    The input data can also be a combination of native Python types and Django model
    instances.

    Example:
        ```
        data = {
            "start": 0,
            "count": 20,
            "articles": Article.objects.all()[:20]
        }
        return ApiResponse(data)
        ```
    '''
    kwargs.setdefault('json_dumps_params', {})
    kwargs['json_dumps_params']['ensure_ascii'] = False
    kwargs['encoder'] = FlexibleJsonEncoder
    kwargs['safe'] = False
    return JsonResponse(data, **kwargs)

def ApiMessage(msg, **kwargs):
    '''Returns JSON response {'message': msg} while maintaining UTF-8 encoding.

    Example:
        ```
        return ApiMessage('The field "title" is required.', status=400)
        ```

        Will return a 400 status code and {"message": "The field \"title\" is required."}
        as JSON content.
    '''
    kwargs.setdefault('json_dumps_params', {})
    kwargs['json_dumps_params']['ensure_ascii'] = False
    return JsonResponse({'message': msg}, **kwargs)
