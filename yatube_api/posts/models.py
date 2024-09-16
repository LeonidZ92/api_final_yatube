from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Q

from .constants import MAX_LENGHT

User = get_user_model()


class Group(models.Model):
    title = models.CharField(max_length=200)
    verbose_name = 'Группа постов'
    slug = models.SlugField(unique=True)
    description = models.TextField()

    def __str__(self):
        return self.title[:MAX_LENGHT]


class Post(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='posts')
    image = models.ImageField(
        upload_to='posts/', null=True, blank=True)
    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.text[:MAX_LENGHT]

    class Meta:
        ordering = ['-pub_date']


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)

    def __str__(self):
        return self.text[:MAX_LENGHT]


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        related_name='following',
        on_delete=models.CASCADE
    )
    following = models.ForeignKey(
        User,
        related_name='followers',
        on_delete=models.CASCADE
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'following'],
                                    name='unique_following'),
            models.CheckConstraint(
                check=~Q(user=models.F('following')),
                name='cannot_follow_self'
            )
        ]

    def __str__(self):
        return f"{self.user} follows {self.following}"
