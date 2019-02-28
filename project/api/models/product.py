from django.db import models


class ProductTagManager(models.Manager):
    def bulk_get_or_create(self, tags):
        '''
        Gets a list of strings and creates tags for those that don't exist
        while fetching those that do.

        Returns:
        - List of ProductTag instances.
        '''
        # Omit repetitions
        tags = set(tags)
        tag_objs = []
        for tag in tags:
            tobj, _ = self.get_or_create(tag=tag)
            tag_objs.append(tobj)
        return tag_objs


class ProductTag(models.Model):
    tag = models.CharField(primary_key=True, max_length=255)

    objects = ProductTagManager()

    def __str__(self):
        return self.tag

    def __serialize__(self):
        return self.tag


class ProductQuerySet(models.QuerySet):
    def with_tags(self, tags):

        return self.filter(
            tags__tag__in=tags
        ).distinct()

# Adapted from:
# https://docs.djangoproject.com/en/2.1/topics/db/managers/#from-queryset
ProductManager = models.Manager.from_queryset(ProductQuerySet)

class Product(models.Model):

    # Long integers are required from the specification
    id = models.BigAutoField(primary_key=True)

    name = models.CharField(max_length=255)

    description = models.TextField()

    category = models.CharField(max_length=255)

    withdrawn = models.BooleanField(default=False)

    tags = models.ManyToManyField(ProductTag)

    objects = ProductManager()

    def __str__(self):
        return self.name + (' (withdrawn)' if self.withdrawn else '')

    def __serialize__(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'category': self.category,
            'tags': self.tags.all(),
            'withdrawn': self.withdrawn,
        }
