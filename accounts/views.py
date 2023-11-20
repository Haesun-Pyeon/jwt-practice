from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def mypage(request):
    content = {'message': f'반갑습니다, {str(request.user)}님!'}
    return Response(content)
