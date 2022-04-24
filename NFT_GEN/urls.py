from django.urls import path
from NFT_GEN.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('home/',homeView,name='genhome'),
    path('layoutP/',LayerPost,name='layoutP'),
    path('app/',LayerGet,name='LayerGet'),
    path('upload/<int:pkk>',uploadImage,name='uploadImage'),
    path('generate/',GenerateImg,name='GenerateImg'),
   #path('login/',login,name='login'),
    path('download/',download,name='download'),
    path('uploadnft/',uploadnft,name='uploadnft'),
    path('setrarity/<int:k>',setrarity,name='setrarity'),
    path('addproj/',add_proj,name='add_proj'),
    path('editproj/<int:pk>',edit_proj,name='edit_proj'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
