class MyModel(DefinedWidthsAssetsFromImagesMixin, models.Model):
    image = models.ImageField(upload_to="path/to/uploads")

    def get_dimensions(self):
        """ returns a list of desired widths """
        return [400, 600, 1000]

    def get_quality(self):
        """ returns quality argument for jpegs 
        defaults to 75 """
        return 100


instance = MyModel.objects.get(pk=1)
instance.image_400.url
instance.image_600.url
instance.image_1000.url

{{ instance.image_400.url }}
{{ instance.image_600.url }}
{{ instance.image_1000.url }}

