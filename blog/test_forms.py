from django.test import TestCase
from .forms import CommentForm


class TestCommentForm(TestCase):

    def test_body_field_is_required(self):
        form = CommentForm({'body': ''})
        self.assertFalse(form.is_valid())
        self.assertIn('body', form.errors.keys())
        self.assertEqual(form.errors['body'][0], 'This field is required.')

    def test_form_is_valid_with_populated_body_field(self):
        form = CommentForm({'body': 'Test todo Item'})
        self.assertTrue(form.is_valid())

    def test_fields_are_explicit_in_form_metaclass(self):
        form = CommentForm()
        self.assertEqual(form.Meta.fields, ('body',))