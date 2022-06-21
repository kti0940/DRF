from rest_framework.permissions import BasePermission
from datetime import datetime, timedelta
from django.utils import timezone
from rest_framework.exceptions import APIException
from rest_framework import status

class GenericAPIException(APIException):
    def __init__(self, status_code, detail=None, code=None):
        self.status_code=status_code
        super().__init__(detail=detail, code=code)
        
class IsAdminOrIsAuthenticatedReadOnly(BasePermission):
    """
    admin 사용자는 모두 가능, 로그인 사용자는 조회만 가능
    """
    SAFE_METHODS = ('GET', )
    message = '접근 권한이 없습니다.'

    def has_permission(self, request, view):
        user = request.user
        
        # 로그인 하지 않은 사람에게 띄워줄 메시지를 만들기 위해 따로 만듦
        if not user.is_authenticated:
            response ={
                    "detail": "서비스를 이용하기 위해 로그인 해주세요.",
                }
            raise GenericAPIException(status_code=status.HTTP_401_UNAUTHORIZED, detail=response)

        if user.is_authenticated and user.is_admin:
            return True
            
        if user.is_authenticated and request.method in self.SAFE_METHODS:
            return True
        
        if user.is_authenticated and request.user.join_date < (timezone.now() - timedelta(days=7)):
            return True
        
        return False       

# class RegistedMoreThanAMinuteUser(BasePermission):
    # """
    # Allows access only to authenticated users.
    # """

    # def has_permission(self, request, view):
    #     user = request.user
    #     if not request.user or not request.user.is_authenticated:
    #         return False
        
    #     print(f"user join date : {user.join_date}")
    #     return bool(user.join_date < (timezone.now() - timedelta(minutes=3)))
