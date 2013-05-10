<div class="pagination pagination-centered">
%try:
%    if num_results:
%        start = start or 0
%        num = num or 20
%        cur_page = int(start//num)
%        max_page = int(num_results//num)
%        skipl = 'disabled'
%        skipr = 'disabled'
%###################################TODO##################################
%#http://flask.pocoo.org/snippets/44/
%#http://codereview.stackexchange.com/questions/15235/how-to-generate-numbers-for-pagination
%        items = [cur_page-10, cur_page-2, cur_page-1, cur_page, cur_page+1, cur_page+2, cur_page+10, cur_page+50]
%        items = [item for item in items if item >= 0 and item <= max_page]
%        if cur_page > len(items):
%            skipl = ''
%        end
%        if cur_page < max_page-len(items):
%            skipr = ''
%        end
  <ul>
    <li class="{{skipl}}"><a href="?q={{q}}&num={{num}}&start={{cur_page-1*num}}">&laquo;</a></li>
%        for i in items:
%            if i==cur_page:
    <li class="active"><a href="?q={{q}}&num={{num}}&start={{i*num}}">{{i}}</a></li>
%            else:
    <li class=""><a href="?q={{q}}&num={{num}}&start={{i*num}}">{{i}}</a></li>
%            end
%        end
    <li class="{{skipr}}"><a href="?q={{q}}&num={{num}}&start={{cur_page+1*num}}">Next</a></li>
  </ul>
%    end
%except NameError:
%    pass
%end
</div> <!-- /pagination -->
