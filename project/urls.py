from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt
from drf_spectacular.views import SpectacularSwaggerView, SpectacularAPIView
from graphene_django.views import GraphQLView

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/', include('application.artworks.urls', namespace='artworks')),
    path('api/', include('application.profiles.urls', namespace='profiles')),
    path('api/feeds/', include('application.feeds.urls', namespace='feeds')),
    path('api/auth/', include('djoser.urls')),
    path('api/auth/', include('djoser.urls.jwt')),
    path("graphql", csrf_exempt(GraphQLView.as_view(graphiql=True))),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
