STATUS=`git status -s`

[ ${#STATUS} -ne 0 ] && echo "Changes need to be commited" && exit 1

cd doc
make html
cd ..

TEMPDIR=`mktemp -d -t "pyleasedoc"`

cp -r doc/_build/html $TEMPDIR/html

git checkout gh-pages
git reset HEAD~1
mv $TEMPDIR/html/* ./
touch .nojekyll

git add .
git commit -m "Autoupdate"
git push -f origin gh-pages

git checkout dev
