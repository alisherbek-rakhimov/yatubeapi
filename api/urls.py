import pprint
from rest_framework.authtoken import views

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import PostViewSet, CommentViewSet

router = DefaultRouter()
router.register('api/v1/posts', PostViewSet)
router.register(r'api/v1/posts/(?P<post_id>\d+)/comments', CommentViewSet, basename='comments')

# pp = pprint.PrettyPrinter(indent=4)
# pp.pprint(router.urls)


urlpatterns = [
    path('api/v1/api-token-auth/', views.obtain_auth_token),
    path('', include(router.urls))
]
