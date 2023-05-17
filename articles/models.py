from django.db import models

class Article(models.Model):
    title = models.CharField('Title', max_length=150)
    author = models.CharField('Author', max_length=250)
    full_text = models.TextField('Article')
    date = models.DateTimeField('Publication Date')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f'/articles/{self.id}'

    class Meta:
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'