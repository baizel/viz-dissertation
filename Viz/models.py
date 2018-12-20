from django.db import models


class BookManager(models.Manager):
    def createBook(self, title):
        book = self.create(title=title)
        # do something with the book
        return book


class Book(models.Model):
    title = models.CharField(max_length=100)
    objects = BookManager()
