"""
日志 django中间件
"""
import json,re

from django.conf import settings
from django.utils.deprecation import MiddlewareMixin

from mysystem.models import OperationLog
from utils.request_util import get_request_user, get_request_ip, get_request_data, get_request_path, get_os,get_browser, get_verbose_name

from django.http import HttpResponseForbidden
from config import ALLOW_FRONTEND,FRONTEND_API_LIST
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from utils.jsonResponse import SuccessResponse,ErrorResponse
from utils.common import get_parameter_dic
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser, User
from channels.auth import AuthMiddlewareStack
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from django.db import close_old_connections
from jwt import decode as jwt_decode
from rest_framework_simplejwt.authentication import AUTH_HEADER_TYPE_BYTES
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import UntypedToken


IS_ALLOW_FRONTEND = ALLOW_FRONTEND

class ApiLoggingMiddleware(MiddlewareMixin):
    """
    用于记录API访问日志中间件
    """

    def __init__(self, get_response=None):
        super().__init__(get_response)
        self.enable = getattr(settings, 'API_LOG_ENABLE', None) or False
        self.methods = getattr(settings, 'API_LOG_METHODS', None) or set()
        self.request_modular = ""

    @classmethod
    def __handle_request(cls, request):
        request.request_ip = get_request_ip(request)
        request.request_data = get_request_data(request)
        request.request_path = get_request_path(request)

    def __handle_response(self, request, response):
        # request_data,request_ip由PermissionInterfaceMiddleware中间件中添加的属性
        body = getattr(request, 'request_data', {})
        # 请求含有password则用*替换掉(暂时先用于所有接口的password请求参数)
        if isinstance(body, dict) and body.get('password', ''):
            body['password'] = '*' * len(body['password'])
        if isinstance(body, dict) and body.get('oldPassword', '') and body.get('newPassword', '') and body.get('newPassword2', ''):
            body['oldPassword'] = '*' * len(body['oldPassword'])
            body['newPassword'] = '*' * len(body['newPassword'])
            body['newPassword2'] = '*' * len(body['newPassword2'])
        if not hasattr(response, 'data') or not isinstance(response.data, dict):
            response.data = {}
        try:
            if not response.data and response.content:
                content = json.loads(response.content.decode())
                response.data = content if isinstance(content, dict) else {}
        except Exception:
            return
        user = get_request_user(request)
        info = {
            'request_ip': getattr(request, 'request_ip', 'unknown'),
            'creator': user if not isinstance(user, AnonymousUser) else None,
            'dept_belong_id': getattr(request.user, 'dept_id', None),
            'request_method': request.method,
            'request_path': request.request_path,
            'request_body': body,
            'response_code': response.data.get('code'),
            'request_os': get_os(request),
            'request_browser': get_browser(request),
            'request_msg': request.session.get('request_msg'),
            'status': True if response.data.get('code') in [2000, ] else False,
            'json_result': {"code": response.data.get('code'), "msg": response.data.get('msg')},
        }
        temp_request_modular = ""
        if not self.request_modular and settings.API_MODEL_MAP.get(request.request_path, None):
            temp_request_modular = settings.API_MODEL_MAP[request.request_path]
        else:
            temp_request_modular = self.request_modular

        operation_log = OperationLog.objects.create(request_modular=temp_request_modular,request_ip=info['request_ip'],creator=info['creator'],dept_belong_id=info['dept_belong_id'],request_method=info['request_method'],request_path=info['request_path'],request_body=info['request_body'],response_code=info['response_code'],request_os=info['request_os'],request_browser=info['request_browser'],request_msg=info['request_msg'],status=info['status'],json_result=info['json_result'])

        self.request_modular = ""

    def process_view(self, request, view_func, view_args, view_kwargs):
        if hasattr(view_func, 'cls') and hasattr(view_func.cls, 'queryset'):
            if self.enable:
                if self.methods == 'ALL' or request.method in self.methods:
                    self.request_modular = get_verbose_name(view_func.cls.queryset)

        return None
    def process_request(self, request):
        self.__handle_request(request)

    def process_response(self, request, response):
        """
        主要请求处理完之后记录
        :param request:
        :param response:
        :return:
        """
        if self.enable:
            if self.methods == 'ALL' or request.method in self.methods:
                self.__handle_response(request, response)

        # 过滤前端接口关闭情况
        if not IS_ALLOW_FRONTEND:
            if FRONTEND_API_LIST:
                for i in FRONTEND_API_LIST:
                    if i in request.request_path:
                        return HttpResponseForbidden('<h1>Access Forbidden 301</h1>')

        return response

class OperateAllowFrontendView(APIView):
    """
    超级管理员动态启用/禁用/获取 禁止前端接口访问
    get:
    获取当前是否禁止前端访问的值
    【参数】无
    post:
    设置当前是否禁止前端访问
    【参数】is_allow = 1 允许访问  0 禁止访问
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        """
        获取当前是否禁止前端访问的值
        """
        data = {
            'is_allow':IS_ALLOW_FRONTEND
        }
        return SuccessResponse(data=data,msg='success')

    @swagger_auto_schema(operation_summary='设置当前是否禁止前端访问',
    request_body=openapi.Schema(#POST请求需要
        type=openapi.TYPE_OBJECT,
        required=['is_allow'],
        properties={
                'is_allow':openapi.Schema(type=openapi.TYPE_INTEGER,description="1允许访问,0 禁止访问"),
             },
        ),
    responses={200:'success'},
    )
    def post(self,request):
        """
        设置当前是否禁止前端访问
        """
        user = request.user
        if user.is_superuser:
            global IS_ALLOW_FRONTEND
            is_allow = int(get_parameter_dic(request)['is_allow'])

            if is_allow:
                IS_ALLOW_FRONTEND = True
            else:
                IS_ALLOW_FRONTEND = False
            data = {
                'is_allow': IS_ALLOW_FRONTEND
            }
            return SuccessResponse(data=data,msg='设置成功')
        else:
            return ErrorResponse(msg="您没有权限操作")

# ======================================================================= #
# ************** channels websocket使用simple-jwt 认证/权限验证中间件  ************** #
# ======================================================================= #
#该中间件可以在channels里通过 self.scope["user"] 获取到一个用户实例

@database_sync_to_async
def get_user(validated_token):
    try:
        user = get_user_model().objects.get(id=validated_token["user_id"])
        return user

    except User.DoesNotExist:
        return AnonymousUser()

def ValidationApi(reqApi, validApi):
    """
    验证当前用户是否有接口权限
    :param reqApi: 当前请求的接口
    :param validApi: 用于验证的接口
    :return: True或者False
    """
    if validApi is not None:
        valid_api = validApi.replace('{id}', '.*?')
        matchObj = re.match(valid_api, reqApi, re.M | re.I)
        if matchObj:
            return True
        else:
            return False
    else:
        return False

@database_sync_to_async
def has_permission(user, path):
    """
    接口地址、方法授权验证
    """
    # 判断是否是超级管理员
    if user.is_superuser:
        return True
    else:
        api = path  # 当前请求接口
        method = "WS"  # 当前请求方法
        methodList = ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS','WS']
        method = methodList.index(method)
        if not hasattr(user, "role"):
            return False
        userApiList = user.role.values('permission__api', 'permission__method')  # 获取当前用户的角色拥有的所有接口
        for item in userApiList:
            valid = ValidationApi(api, item.get('permission__api'))
            if valid and (method == item.get('permission__method')):
                return True
    return False

class JwtAuthMiddleware(BaseMiddleware):
    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        # 关闭旧的数据库连接，以防止使用超时的连接
        close_old_connections()
        # 自定义校验逻辑,获取子协议内容
        protocol = dict(scope['headers']).get(b'sec-websocket-protocol', b'')
        # print(protocol)
        if len(protocol) == 0:
            # Empty AUTHORIZATION header sent
            return None

        alltoken = protocol.split(b', ')

        if not len(alltoken) == 2:
            return None

        if not alltoken[0] == b'JWTLYADMIN':
            return None

        parts = alltoken[1].split(b'lybbn')
        if len(parts) == 0:
            return None

        if parts[0] not in AUTH_HEADER_TYPE_BYTES:
            # Assume the header does not contain a JSON web token
            return None

        if len(parts) != 2:
            return None

        token = parts[1]
        # Get the token
        # Try to authenticate the user
        try:
            # This will automatically validate the token and raise an error if token is invalid
            UntypedToken(token)
        except (InvalidToken, TokenError) as e:
            # Token is invalid
            # print(e,'InvalidToken,TokenError')
            return None
        else:
            #  Then token is valid, decode it
            decoded_data = jwt_decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            # print(decoded_data,'success decode token')
            # Will return a dictionary like -
            # {
            #     "token_type": "access",
            #     "exp": 1568770772,
            #     "jti": "5c15e80d65b04c20ad34d77b6703251b",
            #     "user_id": 6
            # }

            # Get the user using ID
            scope["user"] = await get_user(validated_token=decoded_data)
            user = scope['user']
            if isinstance(user, AnonymousUser):
                return None
            if not user.is_active:
                return None
            path = scope['path']
            haspermission = await has_permission(user,path)
            if not haspermission:
                return None

        return await super().__call__(scope, receive, send)

def JwtAuthMiddlewareStack(inner):
    return JwtAuthMiddleware(AuthMiddlewareStack(inner))
