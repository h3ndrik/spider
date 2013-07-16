<!DOCTYPE html>
<html lang="en">
%try:
%    if filedetail:
%        pass
%    end
%except NameError:
%    filedetail = None
%end
%try:
%    if results:
%        pass
%    end
%except NameError:
%    results = None
%end
%try:
%    if q:
%        pass
%    end
%except NameError:
%    q = None
%end
%try:
%    if start:
%        pass
%    end
%except NameError:
%    start = None
%end
%try:
%    if num:
%        pass
%    end
%except NameError:
%    num = None
%end
%include header_template title=title
%include body_template title=title, filedetail=filedetail, results=results, q=q, start=start, num=num
</html>




