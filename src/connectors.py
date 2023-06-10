from dotenv.main import load_dotenv
import os
import requests
load_dotenv()

from notion_client import Client

class NotionConnector:
    def __init__(self):
        self.notion = Client(auth=os.environ.get('NOTION_TOKEN'))
        self.notion_version = os.environ.get('NOTION_API_VERSION')

    def get_page_content(self, page_id):
        try:
            response = self.notion.blocks.children.list(block_id=page_id)
            blocks = response.get('results', [])
            content = []
            for block in blocks:
                if block.get('type') == 'paragraph':
                    text = block.get('paragraph', {}).get('text', [])
                    text_content = ''.join([t.get('plain_text', '') for t in text])
                    content.append(text_content)
            return '\n'.join(content)
        except Exception as e:
            print('Error retrieving page content:', e)

    def create_page(self, parent_id, title, content):
        try:
            response = self.notion.pages.create(parent={'database_id': parent_id},
                                                properties={'title': {'title': [{'text': {'content': title}}]}},
                                                children=[{'object': 'block', 'type': 'paragraph',
                                                           'paragraph': {'text': [{'type': 'text', 'text': {'content': content}}]}}])
            return response.get('id')
        except Exception as e:
            print('Error creating page:', e)

    def delete_page(self, page_id):
        try:
            self.notion.blocks.update(block_id=page_id, archived=True)
            print('Page deleted successfully.')
        except Exception as e:
            print('Error deleting page:', e)

    def update_page_content(self, page_id, content):
        try:
            blocks = []
            for line in content.split('\n'):
                blocks.append({
                    'object': 'block',
                    'type': 'paragraph',
                    'paragraph': {
                        'text': [{'type': 'text', 'text': {'content': line}}]
                    }
                })

            self.notion.blocks.children.update(block_id=page_id, children=blocks)
            print('Page content updated successfully.')
        except Exception as e:
            print('Error updating page content:', e)

    def get_block_content(self, block_id):
        try:
            response = self.notion.blocks.children.list(block_id=block_id)
            blocks = response.get('results', [])
            content = []
            for block in blocks:
                if block.get('type') == 'paragraph':
                    text = block.get('paragraph', {}).get('text', [])
                    text_content = ''.join([t.get('plain_text', '') for t in text])
                    content.append(text_content)
            return '\n'.join(content)
        except Exception as e:
            print('Error retrieving block content:', e)

    def create_block(self, parent_id, block_type, content):
        try:
            response = self.notion.blocks.children.append(block_id=parent_id, children=[{
                'object': 'block',
                'type': block_type,
                block_type: {'text': [{'type': 'text', 'text': {'content': content}}]}
            }])
            return response.get('id')
        except Exception as e:
            print('Error creating block:', e)

    def delete_block(self, block_id):
        try:
            self.notion.blocks.update(block_id=block_id, archived=True)
            print('Block deleted successfully.')
        except Exception as e:
            print('Error deleting block:', e)

    def get_database_entries(self, database_id):
        try:
            response = self.notion.databases.query(database_id={'database_id': database_id})
            entries = response.get('results', [])
            return entries
        except Exception as e:
            print('Error retrieving database entries:', e)

    def create_database_entry(self, database_id, properties):
        try:
            response = self.notion.pages.create(parent={'database_id': database_id},
                                                properties=properties)
            return response.get('id')
        except Exception as e:
            print('Error creating database entry:', e)

    def update_database_entry(self, entry_id, properties):
        try:
            self.notion.pages.update(page_id=entry_id, properties=properties)
            print('Database entry updated successfully.')
        except Exception as e:
            print('Error updating database entry:', e)

    def delete_database_entry(self, entry_id):
        try:
            self.notion.pages.update(page_id=entry_id, archived=True)
            print('Database entry deleted successfully.')
        except Exception as e:
            print('Error deleting database entry:', e)
