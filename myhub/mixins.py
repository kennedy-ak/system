"""
Common mixins for use across all apps.
"""
import csv
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse
from typing import List, Tuple


class UserIsOwnerMixin(UserPassesTestMixin):
    """
    Mixin that checks if the current user is the owner of an object.
    Assumes the object has a 'user' or 'owner' attribute.
    """
    def test_func(self):
        obj = self.get_object()
        if hasattr(obj, 'user'):
            return obj.user == self.request.user
        elif hasattr(obj, 'owner'):
            return obj.owner == self.request.user
        return False


class SuccessMessageMixin:
    """
    Mixin that adds success messages to CreateViews, UpdateViews, and DeleteViews.
    """
    success_message = None

    def get_success_message(self):
        return self.success_message or f"{self.model._meta.verbose_name.capitalize()} successfully saved."

    def form_valid(self, form):
        messages.success(self.request, self.get_success_message())
        return super().form_valid(form)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.get_success_message())
        return super().delete(request, *args, **kwargs)


class FilterMixin:
    """
    Mixin that provides common filtering functionality for ListViews.
    Subclasses should define the `filter_fields` attribute.
    """
    filter_fields = []  # List of field names to filter by

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search', '')

        # Apply text search if there's a search parameter
        if search_query and hasattr(self, 'get_search_filters'):
            search_filters = self.get_search_filters(search_query)
            if search_filters:
                queryset = queryset.filter(search_filters)

        # Apply field-based filters
        for field in self.filter_fields:
            filter_value = self.request.GET.get(field, '')
            if filter_value:
                # Handle foreign key fields (end with '_id' or '_filter')
                if field.endswith('_id'):
                    queryset = queryset.filter(**{field: filter_value})
                else:
                    queryset = queryset.filter(**{field: filter_value})

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add current filter values to context for form persistence
        context['search_query'] = self.request.GET.get('search', '')
        for field in self.filter_fields:
            context[f'{field}_filter'] = self.request.GET.get(field, '')
        return context


class CSVExportMixin:
    """
    Mixin that adds CSV export functionality to ListViews.
    Subclasses should define `csv_fields` as a list of (field_name, header_name) tuples.
    """
    csv_fields = []  # e.g., [('title', 'Title'), ('status', 'Status')]
    csv_filename = 'export.csv'

    def get_csv_fields(self) -> List[Tuple[str, str]]:
        """Return list of (field_name, header_name) tuples for CSV export."""
        return self.csv_fields

    def get_csv_filename(self) -> str:
        """Return the filename for the CSV export."""
        return self.csv_filename

    def render_to_response(self, context, **response_kwargs):
        """Check if export is requested and handle CSV export."""
        if self.request.GET.get('format') == 'csv':
            return self.export_csv()

        return super().render_to_response(context, **response_kwargs)

    def export_csv(self):
        """Generate and return CSV file response."""
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{self.get_csv_filename()}"'

        writer = csv.writer(response)
        fields = self.get_csv_fields()

        # Write header row
        writer.writerow([header for _, header in fields])

        # Write data rows
        for obj in self.get_queryset():
            row = []
            for field_name, _ in fields:
                # Handle nested attributes (e.g., 'user.username')
                value = obj
                for attr in field_name.split('.'):
                    value = getattr(value, attr, None)
                    if value is None:
                        value = ''
                        break
                row.append(str(value) if value not in (None, '') else '')
            writer.writerow(row)

        return response
