from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.name


class Author(models.Model):
    fullname = models.CharField(max_length=150)
    born_date = models.DateField()
    born_location = models.CharField(max_length=100)
    description = models.CharField()

    def __str__(self) -> str:
        return self.fullname


class Quote(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    quote = models.CharField()
    tags = models.ManyToManyField(Tag)

    class Meta:
        ordering = ['id']

    def __str__(self) -> str:
        return self.quote

    def get_list_tags(self):
        return ', '.join(tag.name for tag in self.tags.all())
