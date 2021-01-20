# usage: ./release.sh 0.3.x

VERSION=$1

# validate version parameter passed
[[ -z "$VERSION" ]] && { echo "VERSION is required" ; exit 1; }

# tag repository
echo "Tagging $VERSION"
git tag $VERSION -m "Bump version"
git push --tags origin master

# package and upload
echo "Releasing version $VERSION"
twine upload --skip-existing dist/trustar2-${VERSION}.tar.gz
