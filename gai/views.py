import hashlib

from django import forms
from django.http import Http404
from django.db.models import Sum
from django.http import (
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseForbidden,
)
from django.shortcuts import (
    get_object_or_404,
    redirect,
    render_to_response,
)
from django.template import RequestContext
from django.utils import simplejson as json

from gai.base56 import (
    mmi_hash,
    mmi_unhash,
)
from gai.models import (
    Url,
    AccessLog,
    UserAgent
)
from gai.settings import (
    MIN_LENGTH,
    SITE_TITLE,
    SITE_SUBTITLE,
    GAI_VERSION,
)


class UrlForm(forms.ModelForm):

    class Meta:
        model = Url
        fields = ('origin', )


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def default_redirect(request, short):
    if len(short) < MIN_LENGTH:
        return HttpResponseNotFound()
    try:
        pk = mmi_unhash(short)
    except:
        raise Http404
    url = get_object_or_404(Url, id=pk)
    ip = get_client_ip(request)
    ua_text = request.META.get('HTTP_USER_AGENT')
    ua_hash = hashlib.sha1(ua_text).hexdigest()
    ua, created = UserAgent.objects.get_or_create(hash=ua_hash,
        defaults={'text': ua_text})
    new_access_log = AccessLog.objects.create(url=url, ip=ip,
        useragent=ua)
    url.access_logs.add(new_access_log)
    url.access_count += 1
    url.save()
    return redirect(url.origin)


def shorten_url(request):
    if request.POST:
        form = UrlForm(request.POST)
        if form.is_valid():
            origin = form.cleaned_data['origin']
            url_hash = hashlib.sha1(origin).hexdigest()
            try:
                url = Url.objects.get(hash=url_hash)
                new = False
            except Url.DoesNotExist:
                new = True
                url = Url.objects.create(origin=origin, hash=url_hash,
                    created_by=get_client_ip(request))
                url.short= mmi_hash(url.id)
                url.save()
            return HttpResponse(json.dumps({'is_new': new, 'shorten': url.short}),
                mimetype="application/json")
        return HttpResponseBadRequest(form.errors['origin'])
    raise Http404


def index(request):
    site_title = SITE_TITLE
    site_subtitle = SITE_SUBTITLE
    version = GAI_VERSION
    form = UrlForm()
    amount_of_urls = Url.objects.count()
    total_access_count = Url.objects.aggregate(tc=Sum('access_count'))['tc']
    return render_to_response('index.html', locals(),
                              context_instance=RequestContext(request))
