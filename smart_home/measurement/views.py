from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
import measurement.models
from measurement.models import Sensor, Measurement
from measurement.serializers import SensorSerializer


class SensorsView(ListAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer

    def post(self, request):
        r = request.data
        Sensor(name=r['name'], description=r['description']).save()
        return Response({'status': f'Датчик {r["name"]} - Добавлен'})


class SensorView(RetrieveAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer

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
    def post(self, request):
        r = request.data
        try:
            sensor_id = Sensor.objects.get(id=r['sensor'])
            Measurement(sensor_id=sensor_id.pk, temp=r['temperature']).save()
            return Response({'status:': f'Данные успешно добавлены. Датчик ID {r["sensor"]}'})

        except ObjectDoesNotExist:
            return Response({'status': 'Датчик не зарегистрирован!'})







