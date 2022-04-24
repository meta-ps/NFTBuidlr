from django.urls import path
from api.views import LayersModelAPIGET,ImagesModelAPIGET,ProjectModelAPIGET, ArchivedProjectModelAPIGET, saveuser,clear,login


urlpatterns = [
    path('api/layer/',LayersModelAPIGET.as_view(),name='layerapi'),
    path('api/image/',ImagesModelAPIGET.as_view(),name='imageapi'),
    path('api/project/',ProjectModelAPIGET.as_view(),name='projectapi'),
    path('api/projects/',ArchivedProjectModelAPIGET.as_view(),name='projectsapi'),
    path('api/user',saveuser,name='saveuser'),
    path('api/login/',login,name='login'),
    path('api/clear',clear,name='clear')
]
