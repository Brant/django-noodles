def re_create_assets(self, request, queryset):
    for item in queryset:
        item.assets_from_images = None
        item.save()
re_create_assets.short_descripton = "Re-create Assets"
