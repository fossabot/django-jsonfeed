import datetime
import json

try:
    from feedgenerator import SyndicationFeed
except ImportError:
    from django.utils.feedgenerator import SyndicationFeed


class JSONFeed(SyndicationFeed):
    content_type = 'application/json; charset=utf-8'

    def json_serial(self, obj):
        """
        Custom JSON serializer for objects not serializable by default.
        """

        if isinstance(obj, (datetime.datetime, datetime.date)):
            return obj.isoformat()

        raise TypeError('Type {} not serializable.'.format(type(obj)))

    def write(self, outfile, encoding):
        data = self.add_root_elements()

        for item in self.items:
            data['items'] += [self.add_item_elements(item), ]

        outfile.write(json.dumps(data, default=self.json_serial))

    def add_root_elements(self):  # noqa
        root_elements = {
            'version': 'https://jsonfeed.org/version/1'
        }

        root_elements['title'] = self.feed.get('title')
        root_elements['home_page_url'] = self.feed.get('link')
        root_elements['description'] = self.feed.get('description')

        if self.feed.get('author_link') or self.feed.get('author_name') or \
           self.feed.get('author_email'):
            root_elements['author'] = {}

        if self.feed.get('author_name'):
            root_elements['author']['name'] = self.feed.get('author_name')

        if self.feed.get('author_email'):
            root_elements['author']['email'] = self.feed.get('author_email')

        if self.feed.get('author_link'):
            root_elements['author']['url'] = self.feed.get('author_link')

        if self.feed.get('feed_url'):
            root_elements['feed_url'] = self.feed['feed_url']

        if self.feed.get('language'):
            root_elements['language'] = self.feed['language']

        if self.feed.get('categories'):
            root_elements['categories'] = self.feed['categories']

        if self.feed.get('icon'):
            root_elements['icon'] = self.feed['icon']

        if self.feed.get('favicon'):
            root_elements['favicon'] = self.feed['favicon']

        if self.feed.get('feed_guid'):
            root_elements['id'] = self.feed['feed_guid']

        if self.feed.get('feed_copyright') or self.feed.get('ttl'):
            root_elements['_django'] = {}

        if self.feed.get('feed_copyright'):
            root_elements['_django']['copyright'] = self.feed['feed_copyright']

        if self.feed.get('ttl'):
            root_elements['_django']['ttl'] = self.feed['ttl']

        root_elements['items'] = list()

        return root_elements

    def add_item_elements(self, item):  # noqa
        item_element = {}

        if item.get('title'):
            item_element['title'] = item.get('title')

        if item.get('description'):
            item_element['content_html'] = item.get('description')

        if item.get('content_text'):
            item_element['content_text'] = item.get('content_text')

        if item.get('link'):
            item_element['url'] = item.get('link')

        if item.get('guid'):
            item_element['id'] = item.get('guid')

        if item.get('author_name') or item.get('author_email') or \
           item.get('author_link'):
            item_element['author'] = {}

        if item.get('author_name'):
            item_element['author']['name'] = item.get('author_name')

        if item.get('author_email'):
            item_element['author']['email'] = item.get('author_email')

        if item.get('author_link'):
            item_element['author']['url'] = item.get('author_link')

        if item.get('enclosures'):
            item_element['attachments'] = []

        for attachment in item.get('enclosures', []):
            item_element['attachments'] += [attachment.__dict__, ]

        enclosure = {}

        if item.get('enclosure_url'):
            enclosure['url'] = item.get('enclosure_url')

        if item.get('enclosure_length'):
            enclosure['length'] = item.get('enclosure_length')

        if item.get('enclosure_mime_type'):
            enclosure['mime_type'] = item.get('enclosure_mime_type')

        if enclosure and item_element.get('attachments'):
            item_element['attachments'] += [enclosure, ]
        elif enclosure and not item_element.get('attachments'):
            item_element['attachment'] = [enclosure, ]

        if item.get('pubdate'):
            item_element['date_published'] = item.get('pubdate')

        if item.get('updateddate'):
            item_element['date_modified'] = item.get('updatedate')

        if item.get('categories'):
            item_element['tags'] = item.get('categories')

        if item.get('copyright'):
            item_element['_django'] = {'copyright': item.get('copyright')}

        if item.get('external_url'):
            item_element['external_url'] = item.get('external_url')

        return item_element
