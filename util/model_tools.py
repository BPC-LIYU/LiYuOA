# coding=utf-8

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage, Page


def page_obj_query(query_set, page_index, page_size):
    """
    分页函数
    by:王健 at:2016-04-18
    :param query_set:
    :param page_index:
    :param page_size:
    :return:
    """
    p = Paginator(query_set, page_size)
    page_count = p.num_pages
    if page_count == 0:
        return Page([], 0, p)
    try:
        return p.page(page_index)
    except PageNotAnInteger:
        page_index = 1
        return p.page(page_index)
    except EmptyPage:
        page_index = p.num_pages
        return p.page(page_index)
