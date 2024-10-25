from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def paginateRequest(request, logged_request, data_num):
    page = request.GET.get('page', 1)
    paginator = Paginator(logged_request, data_num)

    try:
        logged_request = paginator.page(page)
    except PageNotAnInteger:
        logged_request = paginator.page(1)
    except EmptyPage:
        logged_request = paginator.page(paginator.num_pages)

    leftIndex = max(1, int(page) - 4)
    rightIndex = min(paginator.num_pages + 1, int(page) + 5)

    custom_range = range(leftIndex, rightIndex)

    return custom_range, logged_request