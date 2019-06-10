import unittest

from pyramid import testing

import transaction
import json


def dummy_request(dbsession):
    return testing.DummyRequest(dbsession=dbsession)

def dummy_request_JSON_post(dbsession, json_params):
    return testing.DummyRequest(dbsession=dbsession, json_body=json_params, method='POST')
    
class BaseTest(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp(settings={
            'sqlalchemy.url': 'sqlite:///:memory:'
        })
        self.config.include('.models')
        settings = self.config.get_settings()

        from .models import (
            get_engine,
            get_session_factory,
            get_tm_session,
            )

        self.engine = get_engine(settings)
        session_factory = get_session_factory(self.engine)

        self.session = get_tm_session(session_factory, transaction.manager)

    def init_database(self):
        from .models.meta import Base
        Base.metadata.create_all(self.engine)

    def tearDown(self):
        from .models.meta import Base

        testing.tearDown()
        transaction.abort()
        Base.metadata.drop_all(self.engine)

class TestInvoice(BaseTest):
    def setUp(self):
        super(TestInvoice, self).setUp()
        self.init_database()

    def test_invoice_view(self):
        from .models import Invoice
        from .views.invoice import invoice_view
        
        invoice = Invoice()
        self.session.add(invoice)
        response = invoice_view(dummy_request(self.session))
        self.assertEqual(response['status'], 200)
        
    
    def test_invoice_create_zero_date(self):
        from .models import Invoice
        from .views.invoice import invoice_create
        data = {
            'date': '0'
        }
        
        request = dummy_request_JSON_post(self.session, data)     
        response = invoice_create(request)
        
        self.assertEqual(response['status'], 200)
        self.assertEqual(response['payload'], '{"id": 1, "date": "1969-12-31T16:00:00"}')
    
    def test_invoice_create_empty_date(self):
        from .models import Invoice
        from .views.invoice import invoice_create
        data = {
            'date' : ''
        }
        
        request = dummy_request_JSON_post(self.session, data)     
        response = invoice_create(request)

        self.assertEqual(response['status'], 400)
    
    def test_invoice_create_no_date(self):
        from .models import Invoice
        from .views.invoice import invoice_create
        data = {}
        
        request = dummy_request_JSON_post(self.session, data)     
        response = invoice_create(request)

        self.assertEqual(response['status'], 200)

class TestInvoiceItem(BaseTest):
    def setUp(self):
        super(TestInvoiceItem, self).setUp()
        self.init_database()

    def test_item_create_valid(self):
        from .models import Invoice
        from .views.item import item_create
        
        invoice = Invoice()
        self.session.add(invoice)
        data = {
            'units':'1',
            'amount':'1.00',
            'description' : 'test',
            'parent_id' : '1'
        }
        
        request = dummy_request_JSON_post(self.session, data)     
        response = item_create(request)
        
        self.assertEqual(response['status'], 200)
    
    def test_item_create_invalid_units(self):
        from .models import Invoice
        from .views.item import item_create
        
        invoice = Invoice()
        self.session.add(invoice)
        data = {
            'units':'fdfas',
            'amount':'1.00',
            'description' : 'test',
            'parent_id' : '1'
        }
        
        request = dummy_request_JSON_post(self.session, data)     
        response = item_create(request)
        
        self.assertEqual(response['status'], 400)
    
    def test_item_create_negative_units(self):
        from .models import Invoice
        from .views.item import item_create
        
        invoice = Invoice()
        self.session.add(invoice)
        data = {
            'units':'-1',
            'amount':'1.00',
            'description' : 'test',
            'parent_id' : '1'
        }
        
        request = dummy_request_JSON_post(self.session, data)     
        response = item_create(request)
        
        self.assertEqual(response['status'], 400)
    
    def test_item_create_invalid_amount(self):
        from .models import Invoice
        from .views.item import item_create
        
        invoice = Invoice()
        self.session.add(invoice)
        data = {
            'units':'1',
            'amount':'-1.00',
            'description' : 'test',
            'parent_id' : '1'
        }
        
        request = dummy_request_JSON_post(self.session, data)     
        response = item_create(request)
        
        self.assertEqual(response['status'], 400)
    
    def test_item_create_negative_parent_id(self):
        from .models import Invoice
        from .views.item import item_create
        
        invoice = Invoice()
        self.session.add(invoice)
        data = {
            'units':'1',
            'amount':'1.00',
            'description' : 'test',
            'parent_id' : '-1'
        }
        
        request = dummy_request_JSON_post(self.session, data)     
        response = item_create(request)
        
        self.assertEqual(response['status'], 400)
    
    def test_item_create_invalid_parent_id(self):
        from .models import Invoice
        from .views.item import item_create
        
        invoice = Invoice()
        self.session.add(invoice)
        data = {
            'units':'1',
            'amount':'1.00',
            'description' : 'test',
            'parent_id' : '99'
        }
        
        request = dummy_request_JSON_post(self.session, data)     
        response = item_create(request)
        
        self.assertEqual(response['status'], 400)
    
    def test_item_create_missing_units(self):
        from .models import Invoice
        from .views.item import item_create
        
        invoice = Invoice()
        self.session.add(invoice)
        data = {
            'amount':'1.00',
            'description' : 'test',
            'parent_id' : '1'
        }
        
        request = dummy_request_JSON_post(self.session, data)     
        response = item_create(request)
        
        self.assertEqual(response['status'], 400)
    
    def test_item_create_missing_amount(self):
        from .models import Invoice
        from .views.item import item_create
        
        invoice = Invoice()
        self.session.add(invoice)
        data = {
            'units':'1',
            'description' : 'test',
            'parent_id' : '1'
        }
        
        request = dummy_request_JSON_post(self.session, data)     
        response = item_create(request)
        
        self.assertEqual(response['status'], 400)
        
    def test_item_create_missing_description(self):
        from .models import Invoice
        from .views.item import item_create
        
        invoice = Invoice()
        self.session.add(invoice)
        data = {
            'units':'1',
            'amount':'1.00',
            'parent_id' : '1'
        }
        
        request = dummy_request_JSON_post(self.session, data)     
        response = item_create(request)
        
        self.assertEqual(response['status'], 400)

    def test_item_create_missing_parent_id(self):
        from .models import Invoice
        from .views.item import item_create
        
        invoice = Invoice()
        self.session.add(invoice)
        data = {
            'units':'1',
            'amount':'1.00',
            'description' : 'test'
        }
        
        request = dummy_request_JSON_post(self.session, data)     
        response = item_create(request)
        
        self.assertEqual(response['status'], 400)
    
    