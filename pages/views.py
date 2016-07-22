import logging
from itertools import chain


from django.conf import settings
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.exceptions import PermissionDenied


from business.models import Partner, Person
from categories.models import Category
from pages.forms.contact_us import ContactUsForm
from pages.models import HomePage, Article, Atom, Project, About, ContactUs
from pages.models.about import AboutPartner
from pages.models.homepage import RelatedAtom, HomePartnerMap
from pages.models.project import (
    ProjectSortableQuotes, ProjectSortablePartners,
    ProjectSortableFeaturedArticle, ProjectSortableRelatedArticle,
    ProjectSortableExpertPerspectivesArticle,
    ProjectSortableReaderReactionsArticle, ProjectSortableUpdatesArticles,
    ProjectSortableVisualizations)

from pages.models.article import CUSTOM_POST_TYPE_CHOICES

logger = logging.getLogger(__name__)


def homepage_view(request, homepage_id=None, template='home.html'):

    if homepage_id:
        if request.user.is_staff:
            #  journalist previewing specific home page
            homepage_obj = HomePage.objects.get(id=homepage_id)
        else:
            raise PermissionDenied
    else:
        #  anyone viewing single published home page
        homepage_obj = HomePage.objects.get_live_object()

    related_atoms = RelatedAtom.objects.filter(homepage=homepage_obj)

    # Partner Mapbox map
    partner_map = HomePartnerMap()

    formatted_sharing_urls_dict = get_formatted_sharing_urls_default_dict(homepage_obj.get_absolute_url())

    context = {
        'home': homepage_obj,
        'related_atoms': related_atoms,
        'partner_map': partner_map,
        'formatted_sharing_urls_dict': formatted_sharing_urls_dict,
    }

    print(partner_map)

    return render(request, template, context)


def article_list(
        request, tag=None, year=None, month=None, username=None,
        custom_post_type=None, atom=None, partner=None, keyplayer=None,
        category=None, template="article_list.html"):
    """
    Display a list of blog posts that are filtered by tag, year, month,
    author or category. Custom templates are checked for using the name
    ``blog/article_list_XXX.html`` where ``XXX`` is either the
    category slug or author's username if given.
    """
    templates = []
    articles = Article.objects.published()
    if category is not None:
        category = get_object_or_404(Category, slug=category)
        articles = articles.filter(categories=category)
        templates.append(u"blog/article_list_%s.html" %
                         str(category.slug))
    if atom is not None:
        atom = get_object_or_404(Atom, slug=atom)
        articles = articles.filter(atoms=atom)
        templates.append(u"blog/article_list_%s.html" %
                          str(atom.slug))
    if partner is not None:
        partner = get_object_or_404(Partner, slug=partner)
        articles = articles.filter(partners=partner)
        templates.append(u"blog/article_list_%s.html" %
                          str(partner.slug))
    author = None
    if username is not None:
        author = get_object_or_404(User, username=username)
        articles = articles.filter(user=author)
        templates.append(u"blog/article_list_%s.html" % username)

    if custom_post_type is not None:
        # If not a valid custom_post_type, return 404 to move URL matching
        # to next match in mezzcms.urls
        cust_p_types = []
        for c in CUSTOM_POST_TYPE_CHOICES:
            cust_p_types.append(c[0])
        print(cust_p_types)

        if custom_post_type not in cust_p_types:
            print('Raise')
            raise Http404('Test')
        else:
            articles = articles.filter(custom_post_type=custom_post_type)
            # If no blogposts for the custom post type, 404
            # this catches any "fake" custom_post_type arguments
            if not articles:
                raise Http404()
    else:
        articles = articles.exclude(custom_post_type__in=['external', 'press'])

    prefetch = ("categories", "keywords__keyword")

    # prefetch_related(*prefetch)
    logger.debug("Article count:  {}".format(len(articles)))
    
    paginator = Paginator(articles, settings.ARTICLES_PER_PAGE)

    try:
        articles = paginator.page(request.GET.get("page", 1))
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)

    formatted_sharing_urls_dict = get_formatted_sharing_urls_default_dict("") #todo: make this share correct page instead of default homepage

    context = {
        'this_view_name': 'article_list',
        'articles': articles,
        'year': year,
        'month': month,
        'tag': tag,
        'category': category,
        'author': author,
        'custom_post_type': custom_post_type,
        'atom': atom,
        'partner': partner,
        'formatted_sharing_urls_dict': formatted_sharing_urls_dict,
    }
    templates.append(template)
    return render(request, templates, context)


def article_view(request, slug, template="article_two_column.html"):

    articles = Article.objects.published(
        for_user=request.user).select_related()
    article = get_object_or_404(articles, slug=slug)

    #  Note:  The article-article rel is used backward, hence using relate_name
    if request.user.is_staff:
        #  Admin logged in, so show all related articles
        more_articles = article.get_ordered_related_articles()
    else:
        #  regular user, probably anonymous, show only published.
        more_articles = article.get_published_ordered_related_articles()

    # subscribe = SubscribeForm(request.POST or None, article_slug=slug)

    formatted_sharing_urls_dict = get_formatted_sharing_urls_dict(article.title, article.social_title, article.get_absolute_url())

    context = {
        'this_view_name': 'article_detail',
        'article': article,
        'editable_obj': article,
        'more_articles': more_articles,
        'formatted_sharing_urls_dict': formatted_sharing_urls_dict,
        # 'CURRENT_HOST': CURRENT_HOST,
        # 'subscribe': subscribe,
    }

    try:
        authors = article.authors.all()
        url = authors[0].author.facebook_url
        if url:
            context['facebook_author_url'] = url
    except:
        pass

    templates = [template, ]

    # Use single column layout if: article is `newsanalysis` type
    # and layout == singlecolumn
    if article.layout == 'singlecolumn' and article.news_analysis:
        templates = ['article_one_column.html'] + templates
        # Add `Person` if attached to first User
        try:
            columnist = article.authors.all()
            context['columnist'] = columnist[0]
        except:
            context['columnist'] = False

    return render(request, templates, context)


def columns(request):
    """
    Redirect to first `columns_single` for first columnist.
    """

    first_published_columnist_author = None
    authors = Person.objects.all().order_by(
        'last_name', 'first_name')

    for author in authors:
        #  Todo:  Refactor into column object.  Column.getArticles()
        columnist_articles = Article.objects.published().filter(
            authors=author,
            custom_post_type='articles',
            news_analysis=True)
        if len(columnist_articles) > 0:
            first_published_columnist_author = author
            break

    assert first_published_columnist_author is not None,  "no authors found"

    slug = '{0}-{1}'.format(first_published_columnist_author.first_name.lower(),
                            first_published_columnist_author.last_name.lower())

    return HttpResponseRedirect(reverse('columns_single', kwargs={'slug': slug}))


def columns_single(request, slug=None, template='columns_single.html'):
    """
    Get a list of articles for a Article.authors for the provided slug.

    Slug is firstname-lastname, where firstname = User.first_name and
    lastname = User.last_name, and User is attached to BlogPost.authors M2M.

    Gets first User object with the first_name-last_name slug.
    """

    # TODO: Add a general User profile for CALmatters, then use that profile
    # with a slug a BlogPost.authors object,
    # require unique together on first/last

    if not slug:
        return HttpResponseRedirect('/')

    first_name = slug.split('-', 1)[0]  # first half of split a -
    first_name = first_name.capitalize()
    last_name = slug.split('-', 1)[1]  # remaining half of split a -
    last_name = last_name.capitalize()
    columnist = Person.objects.filter(
        user__first_name=first_name, user__last_name=last_name)
    columnist = columnist[0] if columnist else False

    if not columnist:
        return HttpResponseRedirect('/politics/')

    # Todo:  Refactor into column object.  Column.getArticles()
    articles = Article.objects.published().filter(
        authors=columnist,
        custom_post_type='articles',
        news_analysis=True
    )

    # need to fix the prev-next links first to filter out "unpublished"
    # columnists before uncommenting the next lines
    # if not articles:
    #    return HttpResponseRedirect('/politics/')

    paginator = Paginator(articles, settings.ARTICLES_PER_PAGE)

    try:
        articles = paginator.page(request.GET.get("page", 1))
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)

    # articles = paginate(
    #     articles, request.GET.get("page", 1),
    #     settings.article_PER_PAGE,
    #     settings.MAX_PAGING_LINKS)

    bio = columnist

    if not bio:
        return HttpResponseRedirect('/politics/')

    # Get prev/next columnists that have written newsanalysis articles
    authors = Person.objects.filter(
        authors_articles__custom_post_type='articles',
        authors_articles__news_analysis=True
    ).order_by(
        'user__last_name', 'user__first_name'
    ).distinct(
        'user__last_name', 'user__first_name'
    ).select_related(
        'user'
    ).values(
        'pk', 'user__last_name', 'user__first_name'
    )

    logger.debug(authors)
    index = 0
    for i, author_values_dict in enumerate(authors):
        if author_values_dict['pk'] == columnist.id:
            index = i
            break

    prev = False
    next = False

    if index != 0:
        idx = index - 1  # get previous Bio

        prev_slug = authors[idx]['user__first_name'].lower() + '-' + authors[idx]['user__last_name'].lower()
        prev_text = authors[idx]['user__first_name'] + ' ' + authors[idx]['user__last_name']
        prev = {'slug': prev_slug, 'text': prev_text}

    #  -1 since one less than total has not next in 0-index list
    if index < len(authors) - 1:
        idx = index + 1 # get next Bio
        next_slug = authors[idx]['user__first_name'].lower() + '-' + authors[idx]['user__last_name'].lower()
        next_text = authors[idx]['user__first_name'] + ' ' + authors[idx]['user__last_name']
        next = {'slug': next_slug, 'text': next_text}

    formatted_sharing_urls_dict = get_formatted_sharing_urls_default_dict("") #todo: make this share correct page instead of default homepage

    context = {
        'bio': bio,
        'columnist': columnist,
        'full_name': columnist.full_name,
        'articles': articles,
        'prev': prev,
        'next': next,
        'formatted_sharing_urls_dict': formatted_sharing_urls_dict,
    }

    return render(request, template, context)


def project_view(request, slug=None, template='project.html'):
    """
    Gets featured articles, related stories, atom

    Backfills currated articles and features based on categories set in the
    admin. If not categories are set, queries based on all categories.

    If no slug is given, redirect to first by `order` and `published`.
    """

    is_staff = request.user.is_staff

    if not slug:
        # redirect to `first` story
        if is_staff:
            project = Project.objects.all()[0]
        else:
            project = Project.objects.published()[0]

        return HttpResponseRedirect(
            reverse('project_details', args=(project.slug,)))

    if is_staff:
        project = Project.objects.get(slug=slug)
    else:
        project = Project.objects.published().get(slug=slug)

    # Set prev/next story by publish date
    prev = {}
    next = {}
    all_stories = Project.objects.published().values('slug', 'id', 'title')
    # If more than 1 story
    if len(all_stories) > 1:
        current_idx = 0
        for idx, a in enumerate(all_stories):
            if a['id'] == project.id:
                current_idx = idx

        if current_idx == 0:  # at the start
            # no prev
            next['slug'] = all_stories[current_idx + 1]['slug']
            next['text'] = all_stories[current_idx + 1]['title']
        elif current_idx < len(all_stories) - 1:
            prev['slug'] = all_stories[current_idx - 1]['slug']
            prev['text'] = all_stories[current_idx - 1]['title']
            next['slug'] = all_stories[current_idx + 1]['slug']
            next['text'] = all_stories[current_idx + 1]['title']
        else:
            prev['slug'] = all_stories[current_idx - 1]['slug']
            prev['text'] = all_stories[current_idx - 1]['title']
            # no next

    exclude = []
    categories = project.get_category_ids()

    # Get Quotes
    quotes = ProjectSortableQuotes.objects.ordered_for_project(project)
    quotes_len = len(quotes)
    quotes_column_width = 4
    if quotes_len == 1:
        quotes_column_width = 12
    elif quotes_len % 2 == 0:
        quotes_column_width = 6

    partners = ProjectSortablePartners.objects.ordered_for_project(project)

    mgr = ProjectSortableFeaturedArticle.objects
    featured_articles = mgr.ordered_for_project(project)

    # Get to related stories
    mgr = ProjectSortableRelatedArticle.objects
    related_articles = mgr.ordered_for_project(project)

    # Other Related

    ep_mgr = ProjectSortableExpertPerspectivesArticle.objects
    expert_perspectives_articles = ep_mgr.ordered_for_project(project)

    mgr = ProjectSortableReaderReactionsArticle.objects
    reader_reactions_articles = mgr.ordered_for_project(project)

    mgr = ProjectSortableUpdatesArticles.objects
    updates_articles = mgr.ordered_for_project(project)

    # Get visualizations
    mgr = ProjectSortableVisualizations.objects
    visualizations = mgr.ordered_for_project(project)

    # all together
    all_articles_sorted = sorted(
        chain(related_articles, visualizations, expert_perspectives_articles,
              reader_reactions_articles, updates_articles),
        key=lambda instance: instance.publish_date, reverse=True)

    formatted_sharing_urls_dict = get_formatted_sharing_urls_dict(project.title, project.title, project.get_absolute_url())

    context = {
        'project': project,
        'featured_articles': featured_articles[:3],
        #  referenced directly in the template
        # 'onramp': project.onramp,
        # 'atom': project.atom,
        'quotes': quotes,
        'quotes_column_width': quotes_column_width,
        'partners': partners,
        'all_articles_sorted': all_articles_sorted,
        'related_articles': related_articles,
        'visualizations': visualizations,
        'expert_perspectives_articles': expert_perspectives_articles,
        'reader_reactions_articles': reader_reactions_articles,
        'updates_articles': updates_articles,
        # 'related_people': related_people,
        # 'related_members': related_members,
        # 'related_others': related_others,
        # 'question': question,
        # 'answers': answers,
        # 'tweets': tweets,
        'prev': prev,
        'next': next,
        'formatted_sharing_urls_dict': formatted_sharing_urls_dict,
    }

    return render(request, template, context)


def atom_detail(request, slug, template="atom_post_detail.html"):

    try:
        atom_post = Atom.objects.published(for_user=request.user).get(slug=slug)
    except Atom.DoesNotExist:
        raise Http404

    more_atoms = atom_post.related.all()

    formatted_sharing_urls_dict = get_formatted_sharing_urls_dict(atom_post.headline, atom_post.get_social_title(), atom_post.get_absolute_url())

    context = {
        'this_view_name': 'atom_detail',
        'atom': atom_post,
        'editable_obj': atom_post,
        'CURRENT_HOST': request.get_host(),
        'more_atoms': more_atoms,
        'formatted_sharing_urls_dict': formatted_sharing_urls_dict,        
    }

    return render(request, template, context)


def about_view(request, template='pages/about.html'):

    about_instance = About.objects.all().order_by("-created")[0]
    recent_press = Article.objects.published().filter(
        custom_post_type="press").order_by("-publish_date")[:3]
    partner_logos = AboutPartner.objects.filter(about=about_instance)
    partner_logos = partner_logos.order_by('_order')

    formatted_sharing_urls_dict = get_formatted_sharing_urls_default_dict("") #todo: make this share correct page instead of default homepage

    context = dict(
        about=about_instance,
        recent_press=recent_press,
        partner_logos=partner_logos,
        staff=Person.objects.filter(staff_member=True),
        directors=Person.objects.filter(director_board_member=True),
        advisors = Person.objects.filter(advisory_board=True),
        formatted_sharing_urls_dict = formatted_sharing_urls_dict,
    )

    return render(request, template, context)


def about_partners_list(request, template='pages/about/partners.html'):

    partners = Partner.objects.all()

    context = dict(partners=partners)

    return render(request, template, context)


def team_list(request,
              team_filter,
              individual = None,
              template='pages/about/team/includes/list.html'):

    people = None
    articles = None
    if individual:
        people = Person.objects.filter(slug=individual)
        recent_articles = Article.objects.published().filter(
            authors=people).order_by('-publish_date')

        print(recent_articles)

        paginator = Paginator(recent_articles, 5)
        try:
            articles = paginator.page(request.GET.get("page", 1))
        except PageNotAnInteger:
            articles = paginator.page(1)
        except EmptyPage:
            articles = paginator.page(paginator.num_pages)

        template = 'pages/bio.html'

    if team_filter == 'staff':
        if not people:
            people = Person.objects.filter(staff_member=True)
        title = "Staff"
    elif team_filter == 'board-of-directors':
        if not people:
            people = Person.objects.filter(director_board_member=True)
        title = 'Board of Directors'
    elif team_filter == 'advisory-board':
        if not people:
            people = Person.objects.filter(advisory_board=True)
        title = 'Advisory Board'
    else:
        title = "Staff"

    formatted_sharing_urls_dict = get_formatted_sharing_urls_default_dict("") #todo: make this share correct page instead of default homepage

    context = dict(
        people=people,
        title=title,
        team_filter=team_filter,
        recent_articles=articles,
        formatted_sharing_urls_dict = formatted_sharing_urls_dict,    
    )

    return render(request, template, context)


def contact_us(request):

    if request.method == 'POST':

        form = ContactUsForm(request.POST)

        if form.is_valid():
            ContactUs.objects.create(**form.cleaned_data)

            return render(request, 'contact_us_thankyou.html', {'form': form})
    else:
        form = ContactUsForm()

    return render(request, 'contact_us.html', {'form': form})



# todo: move this to a utils file or something?  it's just a helper function used by multiple views
def get_formatted_sharing_urls_default_dict(url):
    return get_formatted_sharing_urls_dict("CALmatters", "A nonprofit, nonpartisan media venture explaining California's policies and politics", url)

def get_formatted_sharing_urls_dict(title, social_title, url):

    import urllib

    # clean up non-urlencode-able input values
    title = urllib.parse.quote_plus(title.encode("utf-8"))
    social_title = urllib.parse.quote_plus(social_title.encode("utf-8"))
    url = urllib.parse.quote_plus("https://calmatters.org" + url) # hard code to live site

    # set output
    return {
        "facebook": "http://facebook.com/sharer.php?u=" + url + "&t=via%40CALmatters%20" + social_title,
        "twitter": "http://twitter.com/home?status=" + social_title + "%20via%20%40CALmatters%20" + url,
        "email": "mailto:?subject=" + title + "&body=" + social_title + " via CALmatters%0A%0A" + url,
    }

# todo: move this to a utils file or something?  it's just a helper function used by multiple views
def debug_print_to_output(text):

    print ("******************************************************************************")
    
    for x in range(0, 30):
        print ("*")
    
    print (text)

    for x in range(0, 30):
        print ("*")
    print ("******************************************************************************")
    
