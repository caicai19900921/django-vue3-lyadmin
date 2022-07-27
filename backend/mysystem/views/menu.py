# -*- coding: utf-8 -*-

"""
@Remark: 菜单模块
"""
from rest_framework import serializers

from mysystem.models import Menu, MenuButton, Button
from mysystem.views.menu_button import MenuButtonSerializer
from utils.jsonResponse import SuccessResponse
from utils.serializers import CustomModelSerializer
from utils.viewset import CustomModelViewSet
from django.db.models import Q
from rest_framework.decorators import action

from rest_framework.permissions import IsAuthenticated


class MenuSerializer(CustomModelSerializer):
    """
    菜单表的简单序列化器
    """
    menuPermission = serializers.SerializerMethodField(read_only=True)

    def get_menuPermission(self, instance):
        queryset = MenuButton.objects.filter(menu=instance.id).order_by('-name').values_list('name', flat=True)
        if queryset:
            return queryset
        else:
            return None

    class Meta:
        model = Menu
        fields = "__all__"
        # exclude = ('description', 'creator', 'modifier')
        read_only_fields = ["id"]


class MenuCreateSerializer(CustomModelSerializer):
    """
    菜单表的创建序列化器
    """
    name = serializers.CharField(required=False)

    class Meta:
        model = Menu
        fields = "__all__"
        #exclude = ('description', 'creator', 'modifier')
        read_only_fields = ["id"]


class MenuTreeSerializer(CustomModelSerializer):
    """
    菜单表的树形序列化器
    """
    children = serializers.SerializerMethodField(read_only=True)
    menuPermission_name = serializers.SerializerMethodField(read_only=True)
    menuPermission = MenuButtonSerializer(read_only=True,many=True)

    def get_children(self, instance):
        queryset = Menu.objects.filter(parent=instance.id).filter(status=1)
        if queryset:
            serializer = MenuTreeSerializer(queryset, many=True)
            return serializer.data
        else:
            return None

    def get_menuPermission_name(self, instance):
        queryset = MenuButton.objects.filter(menu=instance.id).values_list('name', flat=True)
        if queryset:
            return queryset
        else:
            return None

    class Meta:
        model = Menu
        fields = "__all__"
        read_only_fields = ["id"]


class WebRouterSerializer(CustomModelSerializer):
    """
    前端菜单路由的简单序列化器
    """
    path = serializers.CharField(source="web_path")
    title = serializers.CharField(source="name")
    menuPermission = serializers.SerializerMethodField(read_only=True)

    def get_menuPermission(self, instance):
        # 判断是否是超级管理员
        if self.request.user.is_superuser:
            return Button.objects.values_list('value', flat=True)
        else:
            # 根据当前角色获取权限按钮id集合
            permissionIds = list(self.request.user.role.values_list('permission', flat=True))
            #获取当前菜单的按钮权限vlaue
            queryset = MenuButton.objects.filter(id__in=permissionIds).filter(menu_id=instance.id).values_list('value', flat=True)
            if queryset:
                return queryset
            else:
                return None

    class Meta:
        model = Menu
        fields = "__all__"
        read_only_fields = ["id"]


class MenuViewSet(CustomModelViewSet):
    """
    菜单管理接口
    list:查询
    create:新增
    update:修改
    retrieve:单例
    destroy:删除
    """
    queryset = Menu.objects.all().order_by('sort')
    serializer_class = MenuSerializer
    create_serializer_class = MenuCreateSerializer
    update_serializer_class = MenuCreateSerializer
    filterset_fields = ['name', 'status','visible']
    search_fields = ['name','web_path']

    def menu_tree(self, request):
        """用于菜单添加修改中获取父级菜单"""
        queryset = Menu.objects.filter(parent=None)
        serializer = MenuTreeSerializer(queryset, many=True)
        return SuccessResponse(data=serializer.data, msg="获取成功")

    @action(methods=['get'],extra_filter_backends=[],detail=False)#会自动生成/api/system/menu/web_router/的路由
    def web_router(self, request):
        """用于前端获取当前角色的路由"""
        user = request.user
        # queryset = self.queryset.filter(status=1,visible=1)
        queryset = self.queryset.filter(status=1)
        if not user.is_superuser:
            menuIds = user.role.values_list('menu__id', flat=True)
            # queryset = Menu.objects.filter(id__in=menuIds,status=1,visible=1)
            queryset = Menu.objects.filter(id__in=menuIds,status=1)

        serializer = WebRouterSerializer(queryset, many=True, request=request)
        return SuccessResponse(data=serializer.data, msg="获取成功")
