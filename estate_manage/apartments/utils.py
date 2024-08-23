from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def paginateApartments(request, apartments, data_num):
    page = request.GET.get('page', 1)
    paginator = Paginator(apartments, data_num)

    try:
        apartments = paginator.page(page)
    except PageNotAnInteger:
        apartments = paginator.page(1)
    except EmptyPage:
        apartments = paginator.page(paginator.num_pages)

    leftIndex = max(1, int(page) - 4)
    rightIndex = min(paginator.num_pages + 1, int(page) + 5)

    custom_range = range(leftIndex, rightIndex)

    return custom_range, apartments
