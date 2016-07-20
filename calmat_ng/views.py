from functools import reduce
from operator import ior

from django.conf import settings
from django.core.paginator import PageNotAnInteger, Paginator, EmptyPage
from django.db.models import Q
from django.shortcuts import render

from business.models import Person
from pages.models import Article, Project


def search(request, template='search.html'):

    """
    Custom search view for CALmatters.
    """

    query = request.GET.get('q', '')

    # page = request.GET.get('page', 1)
    # per_page = settings.SEARCH_PER_PAGE
    # max_paging_links = settings.MAX_PAGING_LINKS

    article_qs = [
        reduce(ior,
               [Q(**{"%s__icontains" % f: query})
                for f in Article.SEARCH_FIELDS])]

    article_results = Article.objects.published().filter(reduce(ior, article_qs))

    # Separate external results for main results
    main_results = []
    external_results = []
    page_results = []
    if article_results:
        for i, r in enumerate(article_results):
            if r.custom_post_type == 'external':
                external_results.append(r)
            elif r.custom_post_type in ['articles']:
                main_results.append(r)

    # Search for authors
    author_terms = query.lower().split(' ')
    Q_list = []
    for term in author_terms:
        # build queries for User model
        Q_list.append(Q(user__first_name__icontains=term))
        Q_list.append(Q(user__last_name__icontains=term))
    author_query = reduce(ior, Q_list)
    authors = Person.objects.filter(author_query)
    author_results = Article.objects.published().filter(authors__in=authors)
    # get as list to concat with `main_results`
    author_results = [result for result in author_results]

    # concat lists and sort
    main_results = main_results + author_results
    main_results = list(set(sorted(
        main_results, key=lambda result: result.publish_date, reverse=True)))

    paginator = Paginator(main_results, settings.ARTICLES_PER_PAGE)

    try:
        articles = paginator.page(request.GET.get("page", 1))
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)

    has_results = True if main_results or page_results else False

    # Get Features and More Articles if no results or no query
    if not query or not has_results:
        # Features are "Story" pages, big landing pages for a subject
        features = Project.objects.published().order_by('order')[:3]
        more_stories = Article.objects.published().filter(image__isnull=False).order_by(
            'publish_date')[:3]
    else:
        features = False
        more_stories = False

    # post_ids = [r.id for r in results if r.__class__.__name__ is 'BlogPost']
    # related_people = BlogRelatedPerson.objects.filter(id__in=post_ids).distinct()

    # TODO: popular_results?
    # popular_results = ?

    context = {
        'query': query,
        'has_results': has_results,
        'article_results': articles,
        'features': features,
        'page_results': page_results,
        'more_stories': more_stories,
        'related_people': [],
        'popular_results': False,
        'external_results': external_results,
    }

    return render(request, template, context)