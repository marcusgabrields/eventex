from django.core import mail
from django.test import TestCase
from django.shortcuts import resolve_url as r

from eventex.subscriptions.forms import SubscriptionForm
from eventex.subscriptions.models import Subscription


class SubscriptionNewGet(TestCase):
    def setUp(self):
        self.resp = self.client.get(r('subscriptions:new'))

    def test_get(self):
        """Get /inscricao/ must return satatuscode 200"""
        self.resp = self.client.get(r('subscriptions:new'))
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        """Must use subscriptions/subscription_form.html"""
        self.resp = self.client.get(r('subscriptions:new'))
        self.assertTemplateUsed(self.resp, 'subscriptions/subscription_form.html')
    
    def test_html(self):
        """Html must contain input tags"""
        tags = (('<form', 1),
                ('<input', 6),
                ('type="text"', 3),
                ('type="email"', 1),
                ('type="submit"', 1))
        for text, count in tags:
            with self.subTest():
                self.assertContains(self.resp, text, count)
    
    def test_csrf(self):
        """Html must contains csrf"""
        self.assertContains(self.resp, 'csrfmiddlewaretoken')
    
    def test_has_form(self):
        """Context must have subscription form"""
        form = self.resp.context['form']
        self.assertIsInstance(form, SubscriptionForm)
    

class SubscriptionNewPostValid(TestCase):

    def setUp(self):
        data = dict(name='Gabriel Dantas', cpf='12345678901',
                    email='marcusgabriel.ds@gmail.com', phone='81-98965-2002')
        self.resp = self.client.post(r('subscriptions:new'), data)

    def test_post(self):
        """Valid POST shold redirect to /inscricao/1/"""
        self.assertRedirects(self.resp, r('subscriptions:detail', 1))
    
    def test_send_subscribe_email(self):
        self.assertEqual(1, len(mail.outbox))

    def test_save_subscription(self):
        self.assertTrue(Subscription.objects.exists())


class SubscriptionNewPostInvalid(TestCase):

    def setUp(self):
        self.resp = self.client.post(r('subscriptions:new'), {})

    def test_post(self):
        """Invalid Post shold not redirect"""
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):   
        self.assertTemplateUsed(self.resp, 'subscriptions/subscription_form.html')
    
    def test_has_form(self):
        form = self.resp.context['form']
        self.assertIsInstance(form, SubscriptionForm)

    def test_form_has_errors(self):
        form = self.resp.context['form']
        self.assertTrue(form.errors)
    
    def test_dont_save_subscription(self):
        self.assertFalse(Subscription.objects.exists())

