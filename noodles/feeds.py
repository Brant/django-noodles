"""
Syndication feed helpers
"""
from django.utils import feedgenerator
from django.contrib.syndication.views import Feed

class ContentEncodedAttributes(feedgenerator.Rss201rev2Feed):
    """
    Create a type of RSS feed that has content:encoded elements.
    """
    def root_attributes(self):
        attrs = super(ContentEncodedAttributes, self).root_attributes()
        attrs['xmlns:content'] = 'http://purl.org/rss/1.0/modules/content/'
        return attrs
    
    def add_item_elements(self, handler, item):
        super(ContentEncodedAttributes, self).add_item_elements(handler, item)
        handler.addQuickElement(u'content:encoded', item['content_encoded'])
        

class RSSFeedWithContentEncoded(Feed):
    """
    An RSS feed with content:encoded element
    """
    feed_type = ContentEncodedAttributes
    
    def item_extra_kwargs(self, item):        
        return {'content_encoded': self.item_content_encoded(item)}
    
    def item_content_encoded(self, item):
        """
        Full entry content
        """
        raise NotImplementedError("Subclass must implement 'item_content_encoded'")