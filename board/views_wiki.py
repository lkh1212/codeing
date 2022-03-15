from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render
from django.views import View
from django_request_mapping import request_mapping
from board.models import Board, User, Wiki, Revision, Comment
from django.utils import timezone

@request_mapping("")
class WikiView(View):
    @request_mapping("/wiki/wiki", method="get")
    def wiki(self, request):
        return render(request, 'wiki/wiki.html');

    @request_mapping("/wiki/post", method="get")  # 공지사항
    def wikipost(self, request):
        return render(request, 'wiki/post.html');

    @request_mapping("/wiki/wiki/p", method="post")  # 질문
    def wiki_insert(self, request):
        title = request.POST['wiki_title'];
        text = request.POST['content'];
        revitext = request.POST['revi_content'];
        kind = request.POST['kind']
        userid = User.objects.get(user_id=request.session['sessionid'])
        try:
            wikiall = Wiki.objects.all();
            for i in wikiall:
                if i.wiki_title == title:  # 제목이 이미 있으면
                    print(i.wiki_title)
                    raise Exception;  # 에러발생

        except:
            return render(request, 'wiki/postfail.html');

        try:
            data2 = Revision(revi_title=title, revi_content=revitext, user_id=userid.user_id)
            data2.save()
            revi1 = Revision.objects.get(revi_title=title)
            data = Wiki(wiki_title=title, wiki_kind=kind, wiki_content=text, revi_id=revi1.revi_id);
            data.save()
            return render(request, 'wiki/postok.html');
        except:  # id 값이 없으므로 에러가 남
            return render(request, 'postfail.html');


    # 위키 검색
    @request_mapping("/wiki/search", method="get")
    def wikisearch(self, request):
        context = [];
        search_word = request.GET['q']
        wiki_list = Wiki.objects.select_related('revi');

        if search_word:
            if len(search_word) > 1:
                search_wiki_list = wiki_list.filter(wiki_title__icontains=search_word)

                context = {
                    'search_wikis': search_wiki_list,
                    'search_term': search_word
                }
            else:
                context = {'message': '검색어는 2글자 이상 입력해주세요.'}
                # messages.error(self.request, '검색어는 2글자 이상 입력해주세요.')
        return render(request, 'search_wiki.html', context);
