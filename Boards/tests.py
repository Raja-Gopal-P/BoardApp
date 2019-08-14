from django.test import TestCase
from django.urls import reverse
from django.db import IntegrityError
from .models import Board


# Create your tests here.
def create_board(name, description):
    Board.objects.create(name=name,description=description)


def remove_board(name):
    Board.objects.get(name=name).delete()


class ModelTest(TestCase):

    def test_index_rendering_correct(self):
        response = self.client.get(reverse('Boards:index'))
        self.assertContains(response,'Board1', False)

        create_board('Board1', 'Desc1')
        response = self.client.get(reverse('Boards:index'))
        self.assertContains(response, 'Board1', True)

        remove_board('Board1')
        response = self.client.get(reverse('Boards:index'))
        self.assertContains(response, 'Board1', False)

    def test_duplicate_prevention_board_model(self):
        create_board('Board1', 'Desc1')
        with self.assertRaises(IntegrityError):
            create_board('Board1', 'Desc2')
