from django.urls import path, include, re_path
from rest_framework import routers
from demo.quickstart import views
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from django.contrib import admin
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

schema_view = get_schema_view(
    openapi.Info(
        title="Bibliotheque APIs",
        default_version='v1',
        description="La documentations des APIs du l'App Bibliotheque",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'auteurs',views.AuteurViewSet)
router.register(r'livres', views.LivreViewSet)
router.register(r'commentaires', views.CommentaireViewSet)
router.register(r'exemplaires', views.ExemplaireViewSet)
router.register(r'emprunts', views.EmpruntViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('admin/', admin.site.urls),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    re_path(r'^openapi\.json$', schema_view.without_ui(cache_timeout=0), name='schema-json'),

    path('', include(router.urls)),
    
]
