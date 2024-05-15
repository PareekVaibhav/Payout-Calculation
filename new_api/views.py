from django.http import HttpResponse, JsonResponse
from rest_framework import status

from new_api.models import CRMOpp, CRMLed, CRMPil, MASSlm
from django.db.models import Sum
from rest_framework.decorators import api_view
from new_api.serializers import CRMLedSerializer, MASSlmSerializer


# storing same 11 percentage in all CRMPil model
CRMPil.objects.all().update(probability_percent=11)


@api_view(['GET'])
def get_crmled(request):
    crm_objs = CRMLed.objects.all()
    serializer = CRMLedSerializer(crm_objs, many=True).data
    return HttpResponse(serializer, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_mass(request):
    all_objects = MASSlm.objects.all()
    serializer = MASSlmSerializer(all_objects, many=True).data
    return HttpResponse(serializer, status=status.HTTP_200_OK)


def calculate_probability(request):
    all_pipe_objs = CRMPil.objects.all()
    for pipe_obj in all_pipe_objs:
        crm_opp = CRMOpp.objects.filter(pipeline_stage=pipe_obj)
        if crm_opp.exists():
            crm_opp = crm_opp.first()
            crm_opp.probability = crm_opp.amount * pipe_obj.probability_percent
            crm_opp.save()

    crm_closed_objects = CRMOpp.objects.filter(closed_on__isnull=True)
    forecast_value = crm_closed_objects.aggregate(Sum('probability'))['probability__sum']

    month_mapping = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June', 7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'}
    forecast_mapping = {}

    for month_number, month_name in month_mapping.items():
        monthly_forecast_value = crm_closed_objects.filter(target_date__month=month_number).aggregate(Sum('probability'))['probability__sum']
        if monthly_forecast_value is None:
            monthly_forecast_value = 0
        forecast_mapping.update({month_name: monthly_forecast_value})

    return JsonResponse(forecast_mapping, status=status.HTTP_200_OK)



# from new_api.models import CRMCnt
# cm_cnt = CRMCnt.objects.create(contact='9044596343')
# print(cm_cnt.id)


# from new_api.models import CRMEvt
# cm_evt = CRMEvt.objects.create(event='Name', destination='Destination')



# from new_api.models import CRMPil
# for i in range(0, 10):
#     crmpil = CRMPil.objects.create(pipeline_name='NEW' + str(i+1), target_days=10+i)
#     print(str(crmpil.id))
