import os

from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.views import APIView

from .models import City, IDC, Host
from .serializers import CitySerializer, IDCSerializer, HostSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
import subprocess


class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = [IsAuthenticated]


class IDCViewSet(viewsets.ModelViewSet):
    queryset = IDC.objects.all()
    serializer_class = IDCSerializer
    permission_classes = [IsAuthenticated]


class HostViewSet(viewsets.ModelViewSet):
    queryset = Host.objects.all()
    serializer_class = HostSerializer
    permission_classes = [IsAuthenticated]


class PingHostView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        host = get_object_or_404(Host, pk=pk)
        ip = host.ip

        try:
            command = ['ping', '-c', '2', ip] if not os.name == 'nt' else ['ping', '-n', '2', ip]
            result = subprocess.run(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=5
            )

            reachable = result.returncode == 0
            message = f"主机 {host.hostname} ({ip}) ping {'成功' if reachable else '失败'}！"

            return Response({
                "reachable": reachable,
                "message": message,
                "hostname": host.hostname,
                "ip": ip
            }, status=status.HTTP_200_OK)

        except subprocess.TimeoutExpired:
            return Response({
                "reachable": False,
                "message": f"ping 超时：主机 {host.hostname} ({ip}) 无响应。",
                "hostname": host.hostname,
                "ip": ip
            }, status=status.HTTP_408_REQUEST_TIMEOUT)

        except Exception as e:
            return Response({
                "reachable": False,
                "message": f"执行 ping 时发生错误：{str(e)}",
                "hostname": host.hostname,
                "ip": ip
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
