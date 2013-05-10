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
%    if query:
%        pass
%    end
%except NameError:
%    query = None
%end
%include header_template title=title
%include body_template title=title, filedetail=filedetail, results=results, query=query
</html>




