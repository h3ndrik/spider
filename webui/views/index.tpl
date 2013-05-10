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
%include header_template title=title
%include body_template title=title, filedetail=filedetail, results=results, q=q
</html>




