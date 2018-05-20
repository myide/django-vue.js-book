# -*- coding:utf-8 -*-
from collections import OrderedDict
from rest_framework import serializers
from models import *

class BookSerializer(serializers.ModelSerializer):
    users = serializers.SerializerMethodField()
    groups = serializers.SerializerMethodField()
    class Meta:
        model = Book
        fields = ('id', 'name', 'note', 'price', 'users', 'groups')

    def get_users(self, obj):
        if not isinstance(obj, OrderedDict): return [{'id':user.id, 'name':user.username} for user in obj.user.all() ]

    def get_groups(self, obj):
        if not isinstance(obj, OrderedDict): return [{'id':group.id, 'name':group.name} for group in obj.group.all() ]

    def create(self, validated_data):
        userlist = validated_data.pop('users', [])
        grouplist = validated_data.pop('groups', [])
        instance = self.Meta.model.objects.create(**validated_data)
        instance.user.set(userlist)
        instance.group.set(grouplist)
        return instance

    def update(self, instance, validated_data):
        userlist = validated_data.pop('users', [])
        grouplist = validated_data.pop('groups', [])
        self.Meta.model.objects.filter(id=instance.id).update(**validated_data)
        instance.user.set(userlist)
        instance.group.set(grouplist)
        return instance

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name')

