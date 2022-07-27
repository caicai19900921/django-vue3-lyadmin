# -*- coding: utf-8 -*-

"""
@Remark: 角色管理
"""
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated

from mysystem.models import Role, Menu
from mysystem.views.dept import DeptSerializer
from mysystem.views.menu import MenuSerializer
from mysystem.views.menu_button import MenuButtonSerializer
from utils.jsonResponse import SuccessResponse
from utils.serializers import CustomModelSerializer
from utils.validator import CustomUniqueValidator
from utils.viewset import CustomModelViewSet


class RoleSerializer(CustomModelSerializer):
    """
    角色-序列化器
    """

    class Meta:
        model = Role
        fields = "__all__"
        read_only_fields = ["id"]


class RoleCreateUpdateSerializer(CustomModelSerializer):
    """
    角色管理 创建/更新时的列化器
    """
    menu = MenuSerializer(many=True, read_only=True)
    dept = DeptSerializer(many=True, read_only=True)
    permission = MenuButtonSerializer(many=True, read_only=True)
    key = serializers.CharField(max_length=50,
                                validators=[CustomUniqueValidator(queryset=Role.objects.all(), message="权限字符必须唯一")])
    name = serializers.CharField(max_length=50, validators=[CustomUniqueValidator(queryset=Role.objects.all())])

    def validate(self, attrs: dict):
        return super().validate(attrs)

    def save(self, **kwargs):
        data = super().save(**kwargs)
        data.dept.set(self.initial_data.get('dept', []))
        data.menu.set(self.initial_data.get('menu', []))
        data.permission.set(self.initial_data.get('permission', []))
        return data

    class Meta:
        model = Role
        fields = '__all__'


class MenuPermissonSerializer(CustomModelSerializer):
    """
    菜单的按钮权限
    """
    menuPermission = MenuButtonSerializer(many=True, read_only=True)

    class Meta:
        model = Menu
        fields = '__all__'


class RoleViewSet(CustomModelViewSet):
    """
    角色管理接口
    list:查询
    create:新增
    update:修改
    retrieve:单例
    destroy:删除
    """
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    create_serializer_class = RoleCreateUpdateSerializer
    update_serializer_class = RoleCreateUpdateSerializer
    filterset_fields = ['status']
    search_fields = ('name', 'key')

    def roleId_to_menu(self, request, *args, **kwargs):
        """通过角色id获取该角色用于的菜单"""
        # instance = self.get_object()
        # queryset = instance.menu.all()
        queryset = Menu.objects.filter(status=1).all()
        serializer = MenuPermissonSerializer(queryset, many=True)
        return SuccessResponse(data=serializer.data)

    def role_data(self,request,*args,**kwargs):
        instance = self.get_object()
        serializer = RoleSerializer(instance)
        return SuccessResponse(data=serializer.data)

class PermissionViewSet(CustomModelViewSet):
    """
    角色管理-权限管理接口
    list:查询
    create:新增
    update:修改
    retrieve:单例
    destroy:删除
    """
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    create_serializer_class = RoleCreateUpdateSerializer
    update_serializer_class = RoleCreateUpdateSerializer
    filterset_fields = ['status']