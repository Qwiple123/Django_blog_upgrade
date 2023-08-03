from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify as django_slugify

alphabet = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i',
            'й': 'j', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't',
            'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ы': 'i', 'э': 'e', 'ю': 'yu',
            'я': 'ya'}

def slugify(s):
        return django_slugify(''.join(alphabet.get(w, w) for w in s.lower()))

def generate_unique_slug(klass, field, instance=None):
    origin_slug = slugify(field)
    unique_slug = origin_slug
    numb = 1
    if instance is not None:
        while klass.objects.filter(slug=unique_slug).exclude(id=instance.id).exists():
            unique_slug = '%s-%d' % (origin_slug, numb)
            numb += 1
    else:
        while klass.objects.filter(slug=unique_slug).exists():
            unique_slug = '%s-%d' % (origin_slug, numb)
            numb += 1
    return unique_slug


STATUS = (
    ('published', 'published'),
    ('draft', 'draft')
)

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    slug = models.SlugField(unique=True)
    create_date = models.DateTimeField(auto_now_add=timezone.now)
    update_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS)
    author = models.ForeignKey(User, on_delete=models.CASCADE)


    def save(self, *args, **kwargs):
        if self.slug:  # edit
            if slugify(self.title) != self.slug:
                self.slug = generate_unique_slug(Post, self.title)
        else:  # create
            self.slug = generate_unique_slug(Post, self.title)
        super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return self.title