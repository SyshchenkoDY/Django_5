from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.decorators import APIView
from django.core.exceptions import ObjectDoesNotExist
from measurement.models import Sensor, Measurement
from measurement.serializers import SensorSerializer, MeasurementSerializer


# Получение датчиков
class SensorsView(ListAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer

    # Создание датчика
    def post(self, request):
        r = request.data
        Sensor(name=r['name'], description=r['description']).save()
        return Response({'status': f'Датчик {r["name"]} - Добавлен'})


class SensorView(APIView):
    # Получение информации по датчику
    def get(self, request, pk=None):
        values = Measurement.objects.filter(sensor_id=pk)
        values_serial = MeasurementSerializer(values, many=True)
        sensor = Sensor.objects.get(pk=pk)
        ser = SensorSerializer(sensor)
        return Response({'sensor': ser.data, 'measurements': values_serial.data})

    # Обновление датчика
    def patch(self, request, pk=None):
        r = request.data
        item = Sensor.objects.get(id=pk)
        serializer = SensorSerializer(item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data})
        else:
            return Response({"status": "error", "data": serializer.errors})


class MeasurementView(ListAPIView):
    # Добавление измерения
    def post(self, request):
        r = request.data
        try:
            sensor_id = Sensor.objects.get(id=r['sensor'])
            Measurement(sensor_id=sensor_id.pk, temp=r['temperature']).save()
            return Response({'status:': f'Данные успешно добавлены. Датчик ID {r["sensor"]}'})

        except ObjectDoesNotExist:
            return Response({'status': 'Датчик не зарегистрирован!'})
