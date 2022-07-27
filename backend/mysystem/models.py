from django.contrib.auth.models import AbstractUser
from django.db import models

from utils.modles import CoreModel, table_prefix

#自定义

GENDER_CHOICES = (
        (0, "女"),
        (1, "男"),
    )

class Users(AbstractUser, CoreModel):
    IDENTITY_CHOICES = (
        (0, "超级管理员"),
        (1, "系统管理员"),
        (2, "前端用户"),

    )
    username = models.CharField(max_length=50, unique=True, db_index=True, verbose_name='用户账号', help_text="用户账号")
    email = models.EmailField(max_length=60, verbose_name="邮箱", null=True, blank=True, help_text="邮箱")
    mobile = models.CharField(max_length=11,verbose_name="电话", null=True, blank=True, help_text="电话")
    avatar = models.CharField(max_length=200,verbose_name="头像", null=True, blank=True, help_text="头像")
    name = models.CharField(max_length=40, verbose_name="姓名", help_text="姓名")
    nickname = models.CharField(max_length=100, help_text="用户昵称", verbose_name="用户昵称",default="")
    gender = models.SmallIntegerField(choices=GENDER_CHOICES, verbose_name="性别", null=True, blank=True, help_text="性别")
    post = models.ManyToManyField(to='Post', verbose_name='关联岗位', db_constraint=False, help_text="关联岗位")
    role = models.ManyToManyField(to='Role', verbose_name='关联角色', db_constraint=False, help_text="关联角色")#这个就是保留跨表查询的便利(双下划线跨表查询```),但是不用约束字段了,一般公司都用false,这样就省的报错,因为没有了约束(Field字段对象,既约束,又建立表与表之间的关系
    dept = models.ForeignKey(to='Dept', verbose_name='所属部门', on_delete=models.PROTECT, db_constraint=False, null=True,
                             blank=True, help_text="关联部门")

    # 自定义
    # 自定义
    identity = models.SmallIntegerField(choices=IDENTITY_CHOICES, verbose_name="身份标识", null=True, blank=True, default=1,help_text="身份标识")
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='钱包余额')  # 钱包余额
    # vipid = models.CharField(max_length=100, unique=True, help_text="会员id", verbose_name="会员id", null=True, blank=True)
    is_delete = models.BooleanField(default=False, verbose_name="是否逻辑删除", help_text="是否逻辑删除")

    class Meta:
        db_table = table_prefix + "users"
        verbose_name = '用户表'
        verbose_name_plural = verbose_name
        ordering = ('-create_datetime',)


class Post(CoreModel):
    name = models.CharField(null=False, max_length=64, verbose_name="岗位名称", help_text="岗位名称")
    code = models.CharField(max_length=32, verbose_name="岗位编码", help_text="岗位编码")
    sort = models.IntegerField(default=1, verbose_name="岗位顺序", help_text="岗位顺序")
    STATUS_CHOICES = (
        (0, "离职"),
        (1, "在职"),
    )
    status = models.IntegerField(choices=STATUS_CHOICES, default=1, verbose_name="岗位状态", help_text="岗位状态")

    class Meta:
        db_table = table_prefix + "post"
        verbose_name = '岗位表'
        verbose_name_plural = verbose_name
        ordering = ('sort',)


class Role(CoreModel):
    name = models.CharField(max_length=64, verbose_name="角色名称", help_text="角色名称")
    key = models.CharField(max_length=64, verbose_name="权限字符", help_text="权限字符")
    sort = models.IntegerField(default=1, verbose_name="角色顺序", help_text="角色顺序")
    STATUS_CHOICES = (
        (0, "禁用"),
        (1, "启用"),
    )
    status = models.SmallIntegerField(choices=STATUS_CHOICES, default=1, verbose_name="角色状态", help_text="角色状态")
    ADMIN_CHOICES = (
        (0, "否"),
        (1, "是"),
    )
    admin = models.SmallIntegerField(choices=ADMIN_CHOICES, default=0, verbose_name="是否为admin", help_text="是否为admin")
    DATASCOPE_CHOICES = (
        (0, "仅本人数据权限"),
        (1, "本部门数据权限"),
        (2, "本部门及以下数据权限"),
        (3, "全部数据权限"),
        (4, "自定数据权限"),
    )
    data_range = models.SmallIntegerField(default=0, choices=DATASCOPE_CHOICES, verbose_name="数据权限范围", help_text="数据权限范围")
    remark = models.TextField(verbose_name="备注", help_text="备注", null=True, blank=True)
    dept = models.ManyToManyField(to='Dept', verbose_name='数据权限-关联部门', db_constraint=False, help_text="数据权限-关联部门")#自定义数据权限时，即data_range=4时会用到，可以关联多个部门
    menu = models.ManyToManyField(to='Menu', verbose_name='关联菜单', db_constraint=False, help_text="关联菜单")
    permission = models.ManyToManyField(to='MenuButton', verbose_name='关联菜单的接口按钮', db_constraint=False,
                                        help_text="关联菜单的接口按钮")

    class Meta:
        db_table = table_prefix + 'role'
        verbose_name = '角色表'
        verbose_name_plural = verbose_name
        ordering = ('sort',)


class Dept(CoreModel):
    name = models.CharField(max_length=64, verbose_name="部门名称", help_text="部门名称")
    sort = models.IntegerField(default=1, verbose_name="显示排序", help_text="显示排序")
    owner = models.CharField(max_length=32, verbose_name="负责人", null=True, blank=True, help_text="负责人")
    phone = models.CharField(max_length=32, verbose_name="联系电话", null=True, blank=True, help_text="联系电话")
    email = models.EmailField(max_length=32, verbose_name="邮箱", null=True, blank=True, help_text="邮箱")
    STATUS_CHOICES = (
        (0, "禁用"),
        (1, "启用"),
    )
    status = models.SmallIntegerField(choices=STATUS_CHOICES, default=1, verbose_name="部门状态", null=True, blank=True,
                                 help_text="部门状态")
    parent = models.ForeignKey(to='Dept', on_delete=models.CASCADE, default=False, verbose_name="上级部门",
                               db_constraint=False, null=True, blank=True, help_text="上级部门")

    class Meta:
        db_table = table_prefix + "dept"
        verbose_name = '部门表'
        verbose_name_plural = verbose_name
        ordering = ('sort',)


class Button(CoreModel):
    name = models.CharField(max_length=64, verbose_name="权限名称", help_text="权限名称")
    value = models.CharField(max_length=64, verbose_name="权限值", help_text="权限值")

    class Meta:
        db_table = table_prefix + "button"
        verbose_name = '权限标识表'
        verbose_name_plural = verbose_name
        ordering = ('-name',)


class Menu(CoreModel):
    parent = models.ForeignKey(to='Menu', on_delete=models.CASCADE, verbose_name="上级菜单", null=True, blank=True,
                               db_constraint=False, help_text="上级菜单")
    icon = models.CharField(max_length=64, verbose_name="菜单图标", null=True, blank=True, help_text="菜单图标")
    name = models.CharField(max_length=64, verbose_name="菜单名称", help_text="菜单名称")
    sort = models.IntegerField(default=1, verbose_name="显示排序", null=True, blank=True, help_text="显示排序")
    ISLINK_CHOICES = (
        (0, "否"),
        (1, "是"),
    )
    is_link = models.SmallIntegerField(choices=ISLINK_CHOICES, default=0, verbose_name="是否外链", help_text="是否外链")
    web_path = models.CharField(max_length=128, verbose_name="路由地址", null=True, blank=True, help_text="路由地址")
    component = models.CharField(max_length=128, verbose_name="组件地址", null=True, blank=True, help_text="组件地址")
    component_name = models.CharField(max_length=50, verbose_name="组件名称", null=True, blank=True, help_text="组件名称")
    STATUS_CHOICES = (
        (0, "禁用"),
        (1, "启用"),
    )
    status = models.SmallIntegerField(choices=STATUS_CHOICES, default=1, verbose_name="菜单状态", help_text="菜单状态")
    isautopm_CHOICES=(
        (0,'不自动创建'),
        (1,"自动创建")
    )
    isautopm = models.SmallIntegerField(choices=isautopm_CHOICES, default=1, verbose_name="自动创建按钮权限", help_text="自动创建按钮权限")
    CACHE_CHOICES = (
        (0, '禁用'),
        (1, "启用")
    )
    cache = models.SmallIntegerField(choices=CACHE_CHOICES, default=0, verbose_name="是否页面缓存", help_text="是否页面缓存")
    VISIBLE_CHOICES=(
        (0,'不可见'),
        (1,"可见")
    )
    visible = models.SmallIntegerField(choices=CACHE_CHOICES, default=1, verbose_name="侧边栏中是否显示", help_text="侧边栏中是否显示")

    class Meta:
        db_table = table_prefix + "menu"
        verbose_name = '菜单表'
        verbose_name_plural = verbose_name
        ordering = ('sort',)


class MenuButton(CoreModel):
    menu = models.ForeignKey(to="Menu", db_constraint=False, related_name="menuPermission", on_delete=models.CASCADE,
                             verbose_name="关联菜单", help_text='关联菜单')
    name = models.CharField(max_length=64, verbose_name="名称", help_text="名称")
    value = models.CharField(max_length=64, verbose_name="权限值", help_text="权限值")
    api = models.CharField(max_length=64, verbose_name="接口地址", help_text="接口地址")
    METHOD_CHOICES = (
        (0, "GET"),
        (1, "POST"),
        (2, "PUT"),
        (3, "DELETE"),
    )
    method = models.SmallIntegerField(default=0, verbose_name="接口请求方法", null=True, blank=True, help_text="接口请求方法")

    class Meta:
        db_table = table_prefix + "menu_button"
        verbose_name = '菜单权限表'
        verbose_name_plural = verbose_name
        ordering = ('-name',)


class Dictionary(CoreModel):
    code = models.CharField(max_length=100, unique=True, blank=True, null=True, verbose_name="编码", help_text="编码")
    name = models.CharField(max_length=100, blank=True, null=True, verbose_name="名称", help_text="名称")
    STATUS_CHOICES = (
        (0, "禁用"),
        (1, "启用"),
    )
    status = models.SmallIntegerField(choices=STATUS_CHOICES, default=1, verbose_name="状态", help_text="状态")
    sort = models.IntegerField(default=1, verbose_name="显示排序", null=True, blank=True, help_text="显示排序")
    parent = models.ForeignKey(to="Dictionary", db_constraint=False, on_delete=models.PROTECT, blank=True, null=True,
                               verbose_name="父级", help_text="父级")
    remark = models.CharField(max_length=255, blank=True, null=True, verbose_name="备注", help_text="备注")

    class Meta:
        db_table = table_prefix + 'dictionary'
        verbose_name = "字典表"
        verbose_name_plural = verbose_name
        ordering = ('sort',)


class SysDictionarylist(CoreModel):
    code = models.CharField(max_length=100, blank=True, null=True, verbose_name="编码", help_text="编码")
    label = models.CharField(max_length=100, blank=True, null=True, verbose_name="显示名称", help_text="显示名称")
    value = models.CharField(max_length=100, blank=True, null=True, verbose_name="实际值", help_text="实际值")
    dict = models.ForeignKey(to='Dictionary', db_constraint=False, on_delete=models.PROTECT, blank=True, null=True,
                             verbose_name="关联主表", help_text="关联主表")
    STATUS_CHOICES = (
        (0, "禁用"),
        (1, "启用"),
    )
    status = models.SmallIntegerField(choices=STATUS_CHOICES, default=1, verbose_name="状态", help_text="状态")
    remark = models.CharField(max_length=255, blank=True, null=True, verbose_name="备注", help_text="备注")

    class Meta:
        db_table = table_prefix + 'dictionary_detail'
        verbose_name = "字典详细表"
        verbose_name_plural = verbose_name
        ordering = ('code',)


class OperationLog(CoreModel):
    request_modular = models.CharField(max_length=64, verbose_name="请求模块", null=True, blank=True, help_text="请求模块")
    request_path = models.TextField(verbose_name="请求地址", null=True, blank=True, help_text="请求地址")
    request_body = models.TextField(verbose_name="请求参数", null=True, blank=True, help_text="请求参数")
    request_method = models.CharField(max_length=8, verbose_name="请求方式", null=True, blank=True, help_text="请求方式")
    request_msg = models.TextField(verbose_name="操作说明", null=True, blank=True, help_text="操作说明")
    request_ip = models.CharField(max_length=32, verbose_name="请求ip地址", null=True, blank=True, help_text="请求ip地址")
    request_browser = models.CharField(max_length=64, verbose_name="请求浏览器", null=True, blank=True, help_text="请求浏览器")
    response_code = models.CharField(max_length=32, verbose_name="响应状态码", null=True, blank=True, help_text="响应状态码")
    request_os = models.CharField(max_length=64, verbose_name="操作系统", null=True, blank=True, help_text="操作系统")
    json_result = models.TextField(verbose_name="返回信息", null=True, blank=True, help_text="返回信息")
    status = models.BooleanField(default=False, verbose_name="响应状态", help_text="响应状态")

    class Meta:
        db_table = table_prefix + 'operation_log'
        verbose_name = '操作日志'
        verbose_name_plural = verbose_name
        ordering = ('-create_datetime',)


class LoginLog(CoreModel):
    LOGIN_TYPE_CHOICES = (
        (1, '后台登录'),
    )
    username = models.CharField(max_length=32, verbose_name="登录用户名", null=True, blank=True, help_text="登录用户名")
    ip = models.CharField(max_length=32, verbose_name="登录ip", null=True, blank=True, help_text="登录ip")
    agent = models.CharField(max_length=1500,verbose_name="agent信息", null=True, blank=True, help_text="agent信息")
    browser = models.CharField(max_length=200, verbose_name="浏览器名", null=True, blank=True, help_text="浏览器名")
    os = models.CharField(max_length=150, verbose_name="操作系统", null=True, blank=True, help_text="操作系统")
    login_type = models.IntegerField(default=1, choices=LOGIN_TYPE_CHOICES, verbose_name="登录类型", help_text="登录类型")

    class Meta:
        db_table = table_prefix + 'login_log'
        verbose_name = '登录日志'
        verbose_name_plural = verbose_name
        ordering = ('-create_datetime',)