…or create a new repository on the command line
echo "# python" >> README.md
git init
git add README.md
git commit -m "first commit"
git remote add origin https://github.com/zhuby1973/python.git
git push -u origin master
                
…or push an existing repository from the command line
git remote add origin https://github.com/zhuby1973/python.git
git push -u origin master

…or import code from another repository
You can initialize this repository with code from a Subversion, Mercurial, or TFS project.
https://github.com/zhuby1973/python/import


https://stackoverflow.com/questions/10418975/how-to-change-line-ending-settings

Checkout Windows-style, commit Unix-style

Git will convert LF to CRLF when checking out text files. When committing text files, CRLF will be converted to LF. For cross-platform projects, this is the recommended setting on Windows ("core.autocrlf" is set to "true")

Checkout as-is, commit Unix-style

Git will not perform any conversion when checking out text files. When committing text files, CRLF will be converted to LF. For cross-platform projects this is the recommended setting on Unix ("core.autocrlf" is set to "input").

Checkout as-is, commit as-is

Git will not perform any conversions when checking out or committing text files. Choosing this option is not recommended for cross-platform projects ("core.autocrlf" is set to "false")

git config --global core.autocrlf true
git config --global --edit
