class MyModel(HalfQuarterAssetsMixin, models.Model):
    image = models.ImageField(upload_to="path/to/uploads")

instance = MyModel.objects.get(pk=1)
instance.image_half.url

{{ instance.image_half.url }}
