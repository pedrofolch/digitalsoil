from .views import EngineAPIView, EngineRudView, MainEngineAPIView, MainEngineRudView, \
    CenterEngineAPIView, CenterEngineRudView, \
    PortEngineAPIView, PortEngineRudView, \
    PortEngine2APIView, PortEngine2RudView, PortEngine3APIView, PortEngine3RudView, \
    StarboardEngineAPIView, StarboardEngineRudView, Starboard2EngineAPIView, Starboard2EngineRudView, \
    Starboard3EngineAPIView, Starboard3EngineRudView, AuxiliaryEngineAPIView, AuxiliaryEngineRudView, \
    GensetEngineAPIView, GensetEngineRudView, Genset2EngineAPIView, Genset2EngineRudView, ToolsAPIView, ToolsRudView
from django.urls import path


app_name = 'api-engine_room'
urlpatterns = [
    path('', EngineAPIView.as_view(), name='create'),
    path('(<slug:slug>)', EngineRudView.as_view(), name='engine-rud'),

    path('main/', MainEngineAPIView.as_view(), name='main_create'),
    path('main/(<slug:slug>)', MainEngineRudView.as_view(), name='main_engine-rud'),

    path('center/', CenterEngineAPIView.as_view(), name='center_create'),
    path('center/(<slug:slug>)', CenterEngineRudView.as_view(), name='center_engine-rud'),

    path('port/', PortEngineAPIView.as_view(), name='port_create'),
    path('port/(<slug:slug>)', PortEngineRudView.as_view(), name='port_engine-rud'),

    path('port2/', PortEngine2APIView.as_view(), name='port_2_create'),
    path('port2/(<slug:slug>)', PortEngine2RudView.as_view(), name='engine-rud'),

    path('port3/', PortEngine3APIView.as_view(), name='port_3create'),
    path('port3/(<slug:slug>)', PortEngine3RudView.as_view(), name='port_3_engine-rud'),

    path('starboard', StarboardEngineAPIView.as_view(), name='starboard_create'),
    path('starboard/(<slug:slug>)', StarboardEngineRudView.as_view(), name='starboard_engine-rud'),

    path('starboard2/', Starboard2EngineAPIView.as_view(), name='starboard_2_create'),
    path('starboard2/(<slug:slug>)', Starboard2EngineRudView.as_view(), name='starboard_2_engine-rud'),

    path('starboard3/', Starboard3EngineAPIView.as_view(), name='starboard_3_create'),
    path('starboard3/(<slug:slug>)', Starboard3EngineRudView.as_view(), name='starboard_3_engine-rud'),

    path('auxiliary/', AuxiliaryEngineAPIView.as_view(), name='auxiliary_create'),
    path('auxiliary/(<slug:slug>)', AuxiliaryEngineRudView.as_view(), name='auxiliary_engine-rud'),

    path('genset', GensetEngineAPIView.as_view(), name='genset_create'),
    path('genset/(<slug:slug>)', GensetEngineRudView.as_view(), name='genset_engine-rud'),

    path('genset2/', Genset2EngineAPIView.as_view(), name='genset_2_create'),
    path('genset2/(<slug:slug>)', Genset2EngineRudView.as_view(), name='genset_2_engine-rud'),

    path('equipment/', ToolsAPIView.as_view(), name='starboard_3create'),
    path('equipment/(<slug:slug>)', ToolsRudView.as_view(), name='starboard_3_engine-rud'),
]
