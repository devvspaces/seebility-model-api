from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Seebility LLM API",
        default_version='v1',
        description="Api documentation for Seebility LLM API",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="support@seebility.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path(
        "api/v1/",
        include(
            [
                path('chat/', include('chat.api.base.urls')),
                path(
                    'docs/',
                    schema_view.with_ui('swagger', cache_timeout=0),
                    name='schema-swagger-ui'),
            ]
        )
    ),

]


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
