<div class="pagination pagination-centered">
%try:
%    if num_results:
%        start = start or 0
%        num = num or 20
%        num_pagenumbers = 7
%        cur_page = int(start//num)
%        max_page = int(num_results//num)
%        skipl = 'disabled'
%        skipr = 'disabled'
%#TODO
%#http://flask.pocoo.org/snippets/44/
%#http://codereview.stackexchange.com/questions/15235/how-to-generate-numbers-for-pagination
%        if cur_page < num_pagenumbers//2:
%            pagenumbers = range(0, min(max_page, num_pagenumbers))
%        elif cur_page > max_page-num_pagenumbers//2:
%            pagenumbers = range(max(0, max_page-num_pagenumbers+1), max_page+1)
%        else:
%            pagenumbers = range(max(0, cur_page-(num_pagenumbers//2)), min(max_page, cur_page+(num_pagenumbers//2))+1)
%        end
%        if cur_page > 0:
%            skipl = ''
%        end
%        if cur_page < max_page:
%            skipr = ''
%        end
  <ul>
    <li class="{{skipl}}"><a href="?q={{q}}&num={{num}}&start={{(cur_page-1)*num}}">&laquo;</a></li>
%        for i in pagenumbers:
%            if i==cur_page:
    <li class="active"><a href="?q={{q}}&num={{num}}&start={{i*num}}">{{i}}</a></li>
%            else:
    <li class=""><a href="?q={{q}}&num={{num}}&start={{i*num}}">{{i}}</a></li>
%            end
%        end
    <li class="{{skipr}}"><a href="?q={{q}}&num={{num}}&start={{(cur_page+1)*num}}">Next</a></li>
  </ul>
%    end
%except NameError:
%    pass
%end
</div> <!-- /pagination -->
