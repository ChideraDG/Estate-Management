from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def paginateTenants(request, tenants, data_num):
    page = request.GET.get('page', 1)
    paginator = Paginator(tenants, data_num)

    try:
        tenants = paginator.page(page)
    except PageNotAnInteger:
        tenants = paginator.page(1)
    except EmptyPage:
        tenants = paginator.page(paginator.num_pages)

    leftIndex = max(1, int(page) - 4)
    rightIndex = min(paginator.num_pages + 1, int(page) + 5)

    custom_range = range(leftIndex, rightIndex)

    return custom_range, tenants
