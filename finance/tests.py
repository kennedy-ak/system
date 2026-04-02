from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from decimal import Decimal
from datetime import date, timedelta
from .models import Account, Transaction, Subscription

User = get_user_model()


class AccountModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_account_creation(self):
        """Test that an account can be created."""
        account = Account.objects.create(
            name='Test Account',
            user=self.user,
            account_type='checking',
            initial_balance=Decimal('100.00')
        )
        self.assertEqual(account.name, 'Test Account')
        self.assertEqual(account.user, self.user)

    def test_current_balance_calculation(self):
        """Test that current_balance is calculated correctly."""
        account = Account.objects.create(
            name='Test Account',
            user=self.user,
            initial_balance=Decimal('100.00')
        )

        # Add income
        Transaction.objects.create(
            user=self.user,
            account=account,
            amount=Decimal('50.00'),
            t_type='income'
        )

        # Add expense
        Transaction.objects.create(
            user=self.user,
            account=account,
            amount=Decimal('30.00'),
            t_type='expense'
        )

        # Balance should be: 100 + 50 - 30 = 120
        self.assertEqual(account.current_balance(), Decimal('120.00'))

    def test_default_is_active(self):
        """Test default is_active is True."""
        account = Account.objects.create(name='Test Account', user=self.user)
        self.assertTrue(account.is_active)


class TransactionModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_transaction_creation(self):
        """Test that a transaction can be created."""
        transaction = Transaction.objects.create(
            user=self.user,
            amount=Decimal('50.00'),
            t_type='expense',
            category='food'
        )
        self.assertEqual(transaction.amount, Decimal('50.00'))
        self.assertEqual(transaction.t_type, 'expense')

    def test_get_category_choices_for_income(self):
        """Test category choices for income type."""
        choices = Transaction.get_category_choices('income')
        self.assertEqual(len(choices), 6)
        self.assertIn(('salary', 'Salary'), choices)

    def test_get_category_choices_for_expense(self):
        """Test category choices for expense type."""
        choices = Transaction.get_category_choices('expense')
        self.assertEqual(len(choices), 12)
        self.assertIn(('food', 'Food & Dining'), choices)


class SubscriptionModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_subscription_creation(self):
        """Test that a subscription can be created."""
        subscription = Subscription.objects.create(
            user=self.user,
            name='Netflix',
            amount=Decimal('15.99'),
            next_payment_date=date.today() + timedelta(days=30),
            frequency='monthly'
        )
        self.assertEqual(subscription.name, 'Netflix')
        self.assertEqual(subscription.status, 'active')

    def test_default_enable_reminders(self):
        """Test default enable_reminders is True."""
        subscription = Subscription.objects.create(
            user=self.user,
            name='Netflix',
            amount=Decimal('15.99'),
            next_payment_date=date.today() + timedelta(days=30)
        )
        self.assertTrue(subscription.enable_reminders)

    def test_update_next_payment_date_monthly(self):
        """Test update_next_payment_date for monthly frequency."""
        future_date = date.today() + timedelta(days=30)
        subscription = Subscription.objects.create(
            user=self.user,
            name='Netflix',
            amount=Decimal('15.99'),
            next_payment_date=future_date,
            frequency='monthly'
        )
        old_date = subscription.next_payment_date
        subscription.update_next_payment_date()
        # Should be approximately 30 days later
        self.assertEqual(subscription.next_payment_date, old_date + timedelta(days=30))

    def test_clean_validates_future_date(self):
        """Test that clean raises error for past dates."""
        subscription = Subscription(
            user=self.user,
            name='Netflix',
            amount=Decimal('15.99'),
            next_payment_date=date.today() - timedelta(days=1)
        )
        with self.assertRaises(ValidationError):
            subscription.clean()

    def test_str_method(self):
        """Test the __str__ method includes name and amount."""
        subscription = Subscription.objects.create(
            user=self.user,
            name='Netflix',
            amount=Decimal('15.99'),
            next_payment_date=date.today() + timedelta(days=30)
        )
        self.assertIn('Netflix', str(subscription))
        self.assertIn('15.99', str(subscription))
