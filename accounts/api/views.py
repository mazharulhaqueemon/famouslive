import random
from django.utils import timezone
from datetime import date
from django.core.mail import EmailMessage
from django.conf import settings

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from rest_framework.generics import (
    RetrieveAPIView,CreateAPIView,UpdateAPIView,
    ListAPIView, DestroyAPIView
    )
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,HTTP_203_NON_AUTHORITATIVE_INFORMATION,HTTP_204_NO_CONTENT,
    HTTP_207_MULTI_STATUS,HTTP_226_IM_USED,HTTP_208_ALREADY_REPORTED,HTTP_202_ACCEPTED,
    )
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .serializers import AuthTokenSerializer

from profiles.api.serializers import ProfileSerializer
from profiles.models import Profile
from accounts.models import User, PhoneOTP
from fcm.models import FCMDeviceToken

class CreateTokenView(ObtainAuthToken):
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response({},status=HTTP_204_NO_CONTENT)
        user_obj = serializer.validated_data['user']
        if not user_obj:
            return Response({},status=HTTP_204_NO_CONTENT)
        profile_serializer = ProfileSerializer(instance=user_obj.profile,context={"request": request})
     
        token, created = Token.objects.get_or_create(user=user_obj)
        return Response({'token': token.key,'profile':profile_serializer.data}, status=HTTP_200_OK)

class RegisterWithProfileCreateApiView(CreateAPIView):
    authentication_classes = []
    permission_classes = [] 

    def create(self, request, *args, **kwargs):
        data_obj = request.data

        full_name = data_obj.get('full_name',None)
        # birthday = data_obj.get('birthday',None) 
        email = data_obj.get('email',None)
        mobile_number = data_obj.get('mobile_number',None)
        password = data_obj.get('password',None)

        if full_name is None or email is None or mobile_number is None or password is None:
            return Response({},status=HTTP_204_NO_CONTENT)

        # 2014-08-14T00:00:00.000
        #birthday = birthday.split('T')[0]
        #birthday_list = birthday.split('-')
        #birthday = date(int(birthday_list[0]),int(birthday_list[1]),int(birthday_list[2]))
        
        try:
            new_user = User.objects.create_user(phone=mobile_number, password=password)
        except:
            pass
        if new_user is None:
            return Response({},status=HTTP_204_NO_CONTENT)
        
        profile_obj = Profile()
        profile_obj.user = new_user
        profile_obj.full_name = full_name
        profile_obj.email = email
        # profile_obj.birthday = birthday
        profile_obj.save()
              
        serializer_profile = ProfileSerializer(instance=new_user.profile,context={"request": request})
     
        token, created = Token.objects.get_or_create(user=new_user)
        return Response({'token': token.key,'profile':serializer_profile.data}, status=HTTP_201_CREATED)

class LogoutCreateApiView(CreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user_obj = request.user
        # Auth Token
        token_obj = Token.objects.filter(user=user_obj).first()
        if token_obj:
            token_obj.delete()
        # Firebase Cloud Messaging Token
        fcm_token_obj = FCMDeviceToken.objects.filter(user=user_obj).first()
        if fcm_token_obj:
            fcm_token_obj.delete()

        return Response(status=HTTP_201_CREATED)


# Change new Password
class ChangePasswordUpdateApiView(UpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        user_obj = request.user
        data_obj = request.data
        old_password = data_obj.get('old_password',None)
        new_password = data_obj.get('new_password',None)

        if old_password and new_password:
            is_password_exists = user_obj.check_password(old_password)
            if is_password_exists is True:
                # set user new password
                user_obj.set_password(new_password)
                user_obj.save()
                return Response({}, status=HTTP_200_OK,)
            else:
                return Response({},status=HTTP_203_NON_AUTHORITATIVE_INFORMATION)

        return Response({}, status=HTTP_204_NO_CONTENT,)

# Generate OPT
class PasswordResetOtpCreateApiView(CreateAPIView):
    authentication_classes = []
    permission_classes = []
 
    def create(self, request, *args, **kwargs):
        data_obj = request.data
        phone = data_obj.get('mobile',None)
        email = data_obj.get('email',None)

        # user = User.objects.filter(phone = phone).first()
        profile_obj = Profile.objects.filter(user__phone=phone,email=email).first()
        if profile_obj:
            code = random.randint(100000,999999)

            old = PhoneOTP.objects.filter(phone__iexact = phone)
            if old.exists():
                old = old.first()
                old.otp = code
                old.count = old.count + 1
                old.save()
            else:
                PhoneOTP.objects.create(
                    phone = phone,
                    otp = code,
                )
            # Implementing OTP email system
            subject = "Metazo password reset OTP"
            body = f'Your Password Reset OTP is: \n\n{code}'
            email_obj = EmailMessage(subject=subject,body=body,from_email=settings.EMAIL_HOST_USER,to=[email])
            email_obj.content_subtype = "html"
            try:
                email_obj.send(fail_silently=False)
            except:
                pass
            return Response(status=HTTP_201_CREATED,)

        return Response({},status=HTTP_203_NON_AUTHORITATIVE_INFORMATION)

# Reset Forget Password
class ResetPasswordUpdateApiView(UpdateAPIView):
    authentication_classes = []
    permission_classes = [] 

    def update(self, request, *args, **kwargs):
        data_obj = request.data
        phone = data_obj.get('mobile',None)
        password = data_obj.get('password',None)
        otp_sent = data_obj.get('otp',None)
        user_obj = User.objects.filter(phone = phone).first()
        old = PhoneOTP.objects.filter(phone__iexact=phone)

        if old.exists() and user_obj and password is not None:
            old = old.last()
            otp = old.otp
            if str(otp) == otp_sent:
                PhoneOTP.objects.filter(phone__iexact=phone).delete()
                # Reset password
                # set user new password
                user_obj.set_password(password)
                user_obj.save()
                return Response({},status=HTTP_200_OK)

            else:
                return Response({},status=HTTP_203_NON_AUTHORITATIVE_INFORMATION)

        return Response({},status=HTTP_204_NO_CONTENT)
