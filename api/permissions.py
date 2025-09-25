from rest_framework import permissions
from rest_framework.request import Request


class CustomerProfileAccessPermission(permissions.BasePermission):
    """
    CustomerProfileAccessPermission is a custom permission class that restricts access 
    to customer profile views based on the user's identity. It inherits from 
    permissions.BasePermission, which is part of the Django REST framework.
    Attributes:
        message (str): A message that is returned when permission is denied, indicating 
                       that adding customers is not allowed.
    Methods:
        has_permission(request, view):
            Determines whether the user has permission to access the view based on their 
            user ID and the user ID specified in the view's URL parameters.
            Args:
                request (Request): The HTTP request object containing the user information.
                view: The view that is being accessed, which contains the URL parameters.
            Returns:
                bool: True if the user is allowed to access the view (i.e., the user ID 
                      matches the user ID in the URL parameters), otherwise False.
    """
    message = 'Adding customers not allowed.'

    def has_permission(self, request: Request, view):
        """
        Checks if the user has permission to access a specific view based on their user ID.

        Args:
            request (Request): The HTTP request object containing user information.
            view: The view being accessed, which contains URL parameters.

        Returns:
            bool: True if the user's ID matches the ID in the URL parameters, False otherwise.
        """
        return str(request.user.id) == str(view.kwargs['pk']) 
