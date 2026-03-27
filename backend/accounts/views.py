from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import RegisterSerializer, UserSerializer


@api_view(['POST'])
@permission_classes([AllowAny])  # Anyone can register — no auth required
def register(request):
    """
    Creates a new user account and returns JWT tokens immediately.

    WHY return tokens right after registration?
    It avoids forcing the user to log in again after signing up — better UX.
    The frontend can store the tokens and treat the user as logged in straight away.
    """
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': UserSerializer(user).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    """
    Blacklists the refresh token so it can no longer be used to get new access tokens.

    WHY do we need to blacklist?
    JWT access tokens can't be revoked — they're valid until they expire (15 min).
    But we CAN invalidate the refresh token so the user can't get new access tokens
    after logout. This is the standard pattern for JWT logout.
    """
    try:
        refresh_token = request.data.get('refresh')
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({'detail': 'Logged out successfully.'}, status=status.HTTP_200_OK)
    except Exception:
        return Response({'detail': 'Invalid token.'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def me(request):
    """Returns the currently authenticated user's profile."""
    return Response(UserSerializer(request.user).data)
