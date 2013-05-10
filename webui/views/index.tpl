<!DOCTYPE html>
<html lang="en">
%try:
%    if filedetail:
%        pass
%    end
%except NameError:
%    filedetail = None
%end
%include header_template title=title
%include body_template title=title, filedetail=filedetail
</html>




