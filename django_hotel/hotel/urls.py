from django.urls import include, path

from .views import hotel, customers, employers

urlpatterns = [
    path('', hotel.home, name='home'),

    path('customers/', include(([
        path('', customers.RoomListView.as_view(), name='room_list'),
        path('interests/', customers.CustomerInterestsView.as_view(), name='customer_interests'),
        path('taken/', customers.TakenRoomListView.as_view(), name='taken_room_list'),
    ], 'hotel'), namespace='customers')),

    path('employers/', include(([
        path('', employers.RoomListView.as_view(), name='room_change_list'),
        path('room/add/', employers.RoomCreateView.as_view(), name='room_add'),
        path('room/<int:pk>/', employers.RoomUpdateView.as_view(), name='room_change'),
        path('room/<int:pk>/delete/', employers.RoomDeleteView.as_view(), name='room_delete'),
    ], 'hotel'), namespace='employers')),
]
