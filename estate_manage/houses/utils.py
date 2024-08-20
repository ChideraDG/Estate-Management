from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def paginateHouses(request, houses, data_num):
    page = request.GET.get('page', 1)
    paginator = Paginator(houses, data_num)

    try:
        houses = paginator.page(page)
    except PageNotAnInteger:
        houses = paginator.page(1)
    except EmptyPage:
        houses = paginator.page(paginator.num_pages)

    leftIndex = max(1, int(page) - 1)
    rightIndex = min(paginator.num_pages + 1, int(page) + 5)

    custom_range = range(leftIndex, rightIndex)

    return custom_range, houses
