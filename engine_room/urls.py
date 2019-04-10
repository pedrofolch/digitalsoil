from django.urls import path, re_path

from .views import (
    engine_create, engine_detail, engine_list, engine_update, engine_delete,
    main_engine_create, main_engine_detail, main_engine_update, main_engine_delete,
    center_engine_create, center_engine_detail, center_engine_update, center_engine_delete,
    port_engine_create, port_engine_detail, port_engine_update, port_engine_delete,
    port_engine2_create, port_engine2_detail, port_engine2_update, port_engine2_delete,
    port_engine3_create, port_engine3_detail, port_engine3_update, port_engine3_delete,
    starboard_engine_create, starboard_engine_detail, starboard_engine_update, starboard_engine_delete,
    starboard_engine2_create, starboard_engine2_detail, starboard_engine2_update, starboard_engine2_delete,
    starboard_engine3_create, starboard_engine3_detail, starboard_engine3_update, starboard_engine3_delete,
    auxiliary_create, auxiliary_engine_detail, auxiliary_engine_update, auxiliary_engine_delete,
    genset_create, genset_engine_detail, genset_engine_update, genset_engine_delete,
    genset2_create, genset_engine2_detail, genset_engine2_update, genset_engine2_delete,
    tools_create, tool_detail, tool_engine_update, tool_engine_delete
)


app_name = 'engine_room'
urlpatterns = [
    path('', engine_list, name='list'),
    path('create/', engine_create, name='create'),
    path('(<slug:slug>)/', engine_detail, name='detail'),
    path('(<slug:slug>)/edit/', engine_update, name='update'),
    path('(<slug:slug>)/delete/', engine_delete, name='delete'),

    path('main_engine/', main_engine_create, name='main_engine_create'),
    re_path('main_engine/(<int:pk>)', main_engine_detail, name='main_engine_detail'),
    re_path('main_engine/(<int:pk>)/edit/', main_engine_update, name='main_engine_update'),
    re_path('main_engine/(<int:pk>)/delete', main_engine_delete, name='main_engine_delete'),

    re_path('center_engine/', center_engine_create, name='center_engine_create'),
    re_path('center_engine/(<int:pk>)', center_engine_detail, name='center_engine_detail'),
    re_path('center_engine/(<int:pk>)/edit/', center_engine_update, name='center_engine_update'),
    re_path('center_engine/(<int:pk>)/delete', center_engine_delete, name='center_engine_delete'),

    path('port_engine/create/', port_engine_create, name='port_engine_create'),
    re_path('port_engine/(<int:pk>)/', port_engine_detail, name='port_engine_detail'),
    re_path('port_engine/(<int:pk>)/edit/', port_engine_update, name='port_engine_update'),
    re_path('port_engine/(<int:pk>)/delete/', port_engine_delete, name='port_engine_delete'),

    path('port_engine2/', port_engine2_create, name='port_engine2_create'),
    re_path('port_engine2/(<int:pk>)', port_engine2_detail, name='port_engine2_detail'),
    re_path('port_engine2/(<int:pk>)/edit/', port_engine2_update, name='port_engine2_update'),
    re_path('port_engine2/(<int:pk>)/delete', port_engine2_delete, name='port_engine2_delete'),

    path('port_engine3/', port_engine3_create, name='port_engine3_create'),
    re_path('port_engine3/(<int:pk>)', port_engine3_detail, name='port_engine3_detail'),
    re_path('port_engine3/(<int:pk>)/edit/', port_engine3_update, name='port_engine3_update'),
    re_path('port_engine3/(<int:pk>)/delete', port_engine3_delete, name='port_engine3_delete'),

    path('starboard_engine/', starboard_engine_create, name='starboard_engine_create'),
    re_path('starboard_engine/(<int:pk>)/', starboard_engine_detail, name='starboard_engine_detail'),
    re_path('starboard_engine/(<int:pk>)/edit/', starboard_engine_update, name='starboard_engine_update'),
    re_path('starboard_engine/(<int:pk>)/delete/', starboard_engine_delete, name='starboard_engine_delete'),

    path('starboard_engine2/', starboard_engine2_create, name='starboard_engine2_create'),
    re_path('starboard_engine2/(<int:pk>)', starboard_engine2_detail, name='starboard_engine2_detail'),
    re_path('starboard_engine2/(<int:pk>)/edit/', starboard_engine2_update, name='starboard_engine2_update'),
    re_path('starboard_engine2/(<int:pk>)/delete', starboard_engine2_delete, name='starboard_engine2_delete'),

    path('starboard_engine3/', starboard_engine3_create, name='starboard_engine3_create'),
    re_path('starboard_engine3/(<int:pk>)', starboard_engine3_detail, name='starboard_engine3_detail'),
    re_path('starboard_engine3/(<int:pk>)/edit/', starboard_engine3_update, name='starboard_engine3_update'),
    re_path('starboard_engine3/(<int:pk>)/delete', starboard_engine3_delete, name='starboard_engine3_delete'),

    path('auxiliary/', auxiliary_create, name='auxiliary_create'),
    re_path('auxiliary/(<int:pk>)/', auxiliary_engine_detail, name='auxiliary_detail'),
    re_path('auxiliary/(<int:pk>)/edit/', auxiliary_engine_update, name='auxiliary_update'),
    re_path('auxiliary/(<int:pk>)/delete/', auxiliary_engine_delete, name='auxiliary_delete'),

    path('genset/', genset_create, name='genset_engine_create'),
    re_path('genset_engine/(<int:pk>)', genset_engine_detail, name='genset_engine_detail'),
    re_path('genset_engine/(<int:pk>)/edit/', genset_engine_update, name='genset_engine_update'),
    re_path('genset_engine/(<int:pk>)/delete', genset_engine_delete, name='genset_engine_delete'),

    path('genset2/', genset2_create, name='genset_engine2_create'),
    re_path('genset_engine2/(<int:pk>)', genset_engine2_detail, name='genset_engine2_detail'),
    re_path('genset_engine2/(<int:pk>)/edit/', genset_engine2_update, name='genset_engine2_update'),
    re_path('genset_engine2/(<int:pk>)/delete', genset_engine2_delete, name='genset_engine2_delete'),

    path('tool/', tools_create, name='tool_create'),
    re_path('tool/(<int:pk>)', tool_detail, name='tool_detail'),
    re_path('tool/(<int:pk>)/edit/', tool_engine_update, name='tool_update'),
    re_path('tool/(<int:pk>)/delete', tool_engine_delete, name='tool_delete'),
]
