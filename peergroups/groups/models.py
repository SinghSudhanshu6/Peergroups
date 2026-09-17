from django.conf import settings
from django.db import models
from django.urls import reverse

User = settings.AUTH_USER_MODEL

# A small starter list of interests. Feel free to add more, or replace this
# with a proper Interest model + admin later if you want tags to be
# manageable without a code change.
INTEREST_CHOICES = [
    ('study', 'Study group'),
    ('sports', 'Sports & fitness'),
    ('music', 'Music'),
    ('art', 'Art & design'),
    ('coding', 'Coding & tech'),
    ('books', 'Book club'),
    ('gaming', 'Gaming'),
    ('volunteering', 'Volunteering'),
    ('language', 'Language exchange'),
    ('food', 'Food & cooking'),
    ('other', 'Other'),
]


PRIVACY_CHOICES = [
    ('public', 'Public — anyone can join'),
    ('private', 'Private — leader approves who joins'),
]


class Group(models.Model):
    """A student-created meetup: what they're doing, where, and when."""

    name = models.CharField(max_length=120)
    interest = models.CharField(max_length=20, choices=INTEREST_CHOICES, default='other')
    description = models.TextField(help_text="What is this group doing / studying / about?")
    location = models.CharField(max_length=200, help_text="Where you're meeting")
    meeting_time = models.DateTimeField(help_text="When you're meeting")
    privacy = models.CharField(max_length=10, choices=PRIVACY_CHOICES, default='public')

    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_groups')
    members = models.ManyToManyField(User, through='Membership', related_name='joined_groups')

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['meeting_time']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('group_detail', kwargs={'pk': self.pk})

    @property
    def is_private(self):
        return self.privacy == 'private'

    @property
    def member_count(self):
        return self.memberships.filter(status='approved').count()

    @property
    def pending_requests(self):
        return self.memberships.filter(status='pending').select_related('user')


class Membership(models.Model):
    """Links a user to a group they've joined, or asked to join."""

    STATUS_CHOICES = [
        ('approved', 'Approved'),
        ('pending', 'Pending'),
    ]

    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='memberships')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='memberships')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='approved')
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('group', 'user')

    def __str__(self):
        return f'{self.user} in {self.group} ({self.status})'


class Comment(models.Model):
    """A message in a group's discussion, for coordinating before meeting up."""

    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField(max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'{self.author}: {self.text[:40]}'


class Photo(models.Model):
    """A photo shared to a group, e.g. from a past meetup."""

    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='photos')
    uploader = models.ForeignKey(User, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='group_photos/%Y/%m/')
    caption = models.CharField(max_length=200, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return f'Photo in {self.group} by {self.uploader}'
