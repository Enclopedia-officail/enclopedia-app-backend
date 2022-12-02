from rest_framework_simplejwt.authentication import JWTAuthentication

from rest_framework_simplejwt.exceptions import AuthenticationFailed, InvalidToken, TokenError
from rest_framework_simplejwt.settings import api_settings
from rest_framework import HTTP_HEADER_ENCODING

AUTH_HEADER_TYPES = api_settings.AUTH_HEADER_TYPES

if not isinstance(api_settings.AUTH_HEADER_TYPES, (list, tuple)):
    AUTH_HEADER_TYPES = (AUTH_HEADER_TYPES,)

AUTH_HEADER_TYPE_BYTES = set(
    h.encode(HTTP_HEADER_ENCODING)
    for h in AUTH_HEADER_TYPES
)

# authentcateをheaderのbearerから取得するのではなくcookieから取得したものをauthentcateに通すようにしなければならない


class MyJWTAuthentication(JWTAuthentication):
    """
    rewirte JWTauthentication for stacking jwt token in cookie
    """
    # cookieからtoken、user情報を取得するようにする

    def authenticate(self, request):
        access_token = self.get_cookie(request)
        if access_token is None:
            return None

        validated_token = self.get_validated_token(access_token)
        return self.get_user(validated_token), validated_token

    def get_cookie(self, request):
        """
        extracts the cookie containing the JSON web tokenform the given request.
        """

        cookie = request.COOKIES.get('user_token')
        if cookie is None:
            return None
        # cookieはaccesstokenの値を返すようになる
        return cookie

    # headerから取得する場合においてはsplitを用いてauthorizationから取得する必要性上がる
    def get_validated_token(self, access_token):
        """
        Validates an encoded JSON web token and returns a validated token
        wrapper object.
        """
        messages = []
        for AuthToken in api_settings.AUTH_TOKEN_CLASSES:
            try:
                return AuthToken(access_token)
            except TokenError as e:
                messages.append({'token_class': AuthToken.__name__,
                                 'token_type': AuthToken.token_type,
                                 'message': e.args[0]})

        raise InvalidToken({
            'detail': _('Given token not valid for any token type'),
            'messages': messages,
        })

    def get_user(self, validated_token):
        """
        Attempts to find and return a user using the given validated token.
        """
        try:
            user_id = validated_token[api_settings.USER_ID_CLAIM]
        except KeyError:
            raise InvalidToken(
                _('Token contained no recognizable user identification'))

        try:
            user = self.user_model.objects.get(
                **{api_settings.USER_ID_FIELD: user_id})
        except self.user_model.DoesNotExist:
            raise AuthenticationFailed(
                _('User not found'), code='user_not_found')

        if not user.is_active:
            raise AuthenticationFailed(
                _('User is inactive'), code='user_inactive')

        return user
