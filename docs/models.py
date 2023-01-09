from django.db import models


class DocsSchema(models.Model):
    schema = models.TextField()
    version = models.CharField(max_length=12)
    default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class DocsSettings(models.Model):
    public = models.BooleanField(default=False)

# class PathSchema(models.Model):
#     path = models.CharField(max_length=docs_settings.PATH_LENGTH)
#     summary = models.TextField(blank=True)
#     description = models.TextField(blank=True)
#     ref = models.CharField(max_length=docs_settings.PATH_LENGTH+20, blank=True)
#     servers = models.TextField(blank=True)
    
#     parameters = models.ManyToManyField('Parameters', blank=True)
    
#     def __str__(self) -> str:
#         return self.path


# class Parameters(models.Model):
#     name = models.CharField(max_length=120)
#     IN = (
#         ("query", "query"),
#         ("header", "header"),
#         ("path", "path"),
#         ("cookie", "cookie")
#     )
#     in_ = models.CharField(max_length=10, choices=IN)
#     required = models.BooleanField(default=True)
#     description = models.CharField(max_length=docs_settings.PATH_LENGTH)
#     allowEmptyValue = models.BooleanField(blank=True)
#     STYLE = (
#     ("form", '"form" with query, cookie')
#     ("simple", '"simple" with header, path'),
#     ("matrix", '"visit specification for details'),
#     ("label", '"visit specification for details'),
#     ("spaceDelimited", '"visit specification for details'),
#     ("pipeDelimited", '"visit specification for details'),
#     ("deepObject", '"visit specification for details')
#     )
#     style = models.CharField(max_length=20, choices=STYLE)
#     explode = models.BooleanField(blank=True)
#     allowReserved = models.BooleanField(blank=True)
#     deprecated = models.BooleanField(blank=True)
    
#     schema = models.TextField(blank=True)
#     content = models.TextField(blank=True)
#     example = models.TextField(blank=True)
#     examples = models.TextField(blank=True)
    
#     def __str__(self) -> str:
#         return self.name


