from typing import Dict, Tuple
from urllib.parse import quote
import json

from django.conf import settings
from django.http.request import HttpRequest, QueryDict, MultiValueDict
from django.urls import resolve, reverse
from django.utils.translation import gettext as _
from django.views.generic.base import TemplateView

from .models import Recipe


def cache_query(
    request: "django.http.request.HttpRequest",
    url_name: str,
    url_args: Tuple[str] = (),
    url_kwargs: Dict[str, str] = {},
    path_args: Dict[str, str] = {},
) -> Dict[str, str]:
    """
    build mockups of a HTTP request and return the content of the response.
    This is used to include responses of known subsequent requests into the
    first HTTP response.

    This only works if the response content can be encoded in UTF-8.

    :param request: The first HTTP request. It is used to copy cookies,
        session, etc. to "sub"-requests.
    :param url_name: Name of the view in the urlconfig.
    :param url_args: positional args for the URL resolver.
    :param url_kwargs: keyword args for the URL resolver.
    :param path_args: Query parameters for the final URL.
    :return: dictionary fit to be fed into :py:meth:`dict.update` for
        :py:meth:`SinglePageAppView.get_query_results`.
    """
    url = reverse(url_name, args=url_args, kwargs=url_kwargs)
    resolution = resolve(url)
    req = HttpRequest()
    req.GET = QueryDict(mutable=True)
    if len(path_args) > 0:
        req.GET.update(path_args)
    req.POST = QueryDict(mutable=True)
    req.COOKIES = {}
    req.COOKIES.update(request.COOKIES)
    req.META = {}
    for k in (
        "SERVER_NAME",
        "SERVER_PORT",
        "REMOTE_HOST",
        "REMOTE_ADDR",
        "HTTP_HOST",
        "HTTP_ACCEPT_LANGUAGE",
        "HTTP_COOKIE",
        "HTTP_UPGRADE_INSECURE_REQUESTS",
    ):
        if k in request.META:
            req.META[k] = request.META[k]
    req.FILES = MultiValueDict()

    req.path = url
    req.path_info = url
    req.method = "GET"
    req.resolver_match = resolution
    req.content_type = None
    req.content_params = None
    response = resolution.func(request=req, *url_args, **url_kwargs)
    if hasattr(response, "render"):
        response = response.render()
    if not (200 <= response.status_code < 300):
        # only cache successful requests
        return {}
    full_url = url
    if len(path_args) > 0:
        full_url += "?" + "&".join(
            f"{quote(key)}={quote(value)}" for key, value in path_args.items()
        )
    return {full_url: response.content.decode("utf-8")}


class SinglePageAppView(TemplateView):
    template_name = "claypot/index.html"

    def get_context_data(self, **kwargs) -> dict:
        result = super().get_context_data(**kwargs)
        result["page_title"] = self.get_page_title()
        result["HTML_LANGUAGE_CODE"] = settings.HTML_LANGUAGE_CODE
        result["injected_data"] = self.get_injected_data()
        result["og_tags"] = self.get_og_tags()
        return result

    def get_injected_data(self) -> dict:
        return {
            "query_results": self.get_query_results(),
        }

    def get_og_tags(self) -> Dict[str, str]:
        return {
            "og:title": self.get_og_title(),
            "og:description": self.get_og_description(),
            "og:image": self.get_og_image(),
            "og:type": self.get_og_type(),
        }

    def get_og_title(self) -> str:
        # 95 is the maximum length allowed
        return self.get_page_title()[:95]

    def get_og_description(self) -> str:
        return ""

    def get_og_image(self) -> str:
        return ""

    def get_og_type(self) -> str:
        return ""

    def get_page_title(self) -> str:
        return "claypot"

    def get_query_results(self) -> Dict[str, str]:
        result = {}
        result.update(
            cache_query(self.request, "sentry-config")
        )
        # if self.request.user.is_authenticated:
        #     result.update(
        #         cache_query(
        #             self.request,
        #             "api:accounts-detail",
        #             url_kwargs={"pk": self.request.user.pk},
        #         )
        #     )
        return result


class IndexView(SinglePageAppView):
    def get_page_title(self) -> str:
        return "claypot"

    def get_og_type(self) -> str:
        return "website"

    def get_query_results(self) -> Dict[str, str]:
        result = super().get_query_results()
        result.update(
            cache_query(
                self.request,
                "api:recipe-list",
                path_args={"page": self.request.GET.get("page", "1")},
            )
        )
        return result


class RecipeDetailView(SinglePageAppView):
    def get_cached_serialized_recipe(self) -> Dict[str, str]:
        # We cache this, because it contains all the info we need for the rest
        # of this view and we would rather not make additional database queries
        # to get the same information.
        if not hasattr(self, "_recipe_query_result"):
            self._recipe_query_result = cache_query(
                self.request, "api:recipe-detail", url_kwargs={"pk": self.kwargs["pk"]}
            )
        return self._recipe_query_result

    def get_object(self) -> dict:
        """
        :returns: serialized :py:class:`claypot.models.Recipe` object
        """
        # parses the JSON from :py:meth:`get_cached_serialized_recipe`.
        # Burns CPU cycles here for deserialization, but saves some on the
        # other side by not querying the database again. Not sure, if it
        # is a good trade-off. :shrug:
        if not hasattr(self, "_recipe"):
            self._recipe = json.loads(
                list(self.get_cached_serialized_recipe().values())[0]
            )
        return self._recipe

    def get_og_type(self) -> str:
        return "article"

    def get_og_image(self) -> str:
        # Extract thumbnail info from JSON object.
        # Maybe the thumbnail is not the perfect size for this.
        recipe = self.get_object()
        if len(recipe["images"]) == 0:
            return super().get_og_image()
        image = recipe["images"][0]
        if (
            image is not None
            and image.get("thumbnail") is not None
            and image["thumbnail"].get("image_file") is not None
        ):
            return image["thumbnail"]["image_file"]
        else:
            return super().get_og_image()

    def get_page_title(self) -> str:
        return _("{recipe_title} - Recipe - claypot").format(
            recipe_title=self.get_object()["title"]
        )

    def get_query_results(self) -> Dict[str, str]:
        result = super().get_query_results()
        result.update(self.get_cached_serialized_recipe())
        result.update(
            cache_query(
                self.request,
                "api:reciperelation-list",
                path_args={"recipe": str(self.kwargs["pk"]), "page": "1"},
            )
        )
        return result
