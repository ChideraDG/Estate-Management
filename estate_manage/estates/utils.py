from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def paginateEstates(request, estates, data_num):
    page = request.GET.get('page', 1)
    paginator = Paginator(estates, data_num)

    try:
        estates = paginator.page(page)
    except PageNotAnInteger:
        estates = paginator.page(1)
    except EmptyPage:
        estates = paginator.page(paginator.num_pages)

    leftIndex = max(1, int(page) - 4)
    rightIndex = min(paginator.num_pages + 1, int(page) + 5)

    custom_range = range(leftIndex, rightIndex)

    return custom_range, estates
