from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Project

User = get_user_model()


class ProjectModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_project_creation(self):
        """Test that a project can be created."""
        project = Project.objects.create(
            title='Test Project',
            description='Test description',
            owner=self.user,
            status='ongoing'
        )
        self.assertEqual(project.title, 'Test Project')
        self.assertEqual(project.owner, self.user)
        self.assertEqual(project.status, 'ongoing')

    def test_project_str_method(self):
        """Test the __str__ method returns the project title."""
        project = Project.objects.create(title='Test Project', owner=self.user)
        self.assertEqual(str(project), 'Test Project')

    def test_default_status(self):
        """Test default status is ongoing."""
        project = Project.objects.create(title='Test Project', owner=self.user)
        self.assertEqual(project.status, 'ongoing')

    def test_total_income_method(self):
        """Test the total_income method calculates correctly."""
        from finance.models import Transaction
        from decimal import Decimal

        project = Project.objects.create(title='Test Project', owner=self.user)

        # Create some income transactions
        Transaction.objects.create(
            user=self.user,
            project=project,
            amount=Decimal('100.00'),
            t_type='income',
            category='salary'
        )
        Transaction.objects.create(
            user=self.user,
            project=project,
            amount=Decimal('50.00'),
            t_type='income',
            category='freelance'
        )
        Transaction.objects.create(
            user=self.user,
            project=project,
            amount=Decimal('25.00'),
            t_type='expense',
            category='food'
        )

        self.assertEqual(project.total_income(), Decimal('150.00'))
