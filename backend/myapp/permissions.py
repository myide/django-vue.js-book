#coding=utf-8

from rest_framework import permissions

class AuthOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.id is not None

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
        objgroup = [g.name for g in obj.group.all()]
        usergroup = [g.name for g in request.user.groups.all()]
        return request.user.is_superuser or \
               list((set(objgroup).union(set(usergroup)))^(set(objgroup)^set(usergroup))) or \
               request.user in obj.user.all()
