VERSION_FILE = make/__version__.py

.PHONY: version bump-patch bump-minor bump-major release build publish clean

version:
	@python3 -c "from make.__version__ import __version__; print(__version__)"

bump-patch:
	@python3 -c "\
f = '$(VERSION_FILE)'; \
content = open(f).read(); \
v = content.strip().split('=')[1].strip().strip(\"'\"); \
parts = v.split('.'); \
parts[2] = str(int(parts[2]) + 1); \
open(f, 'w').write(\"__version__ = '\" + '.'.join(parts) + \"'\\n\")"
	@$(MAKE) version

bump-minor:
	@python3 -c "\
f = '$(VERSION_FILE)'; \
content = open(f).read(); \
v = content.strip().split('=')[1].strip().strip(\"'\"); \
parts = v.split('.'); \
parts[1] = str(int(parts[1]) + 1); parts[2] = '0'; \
open(f, 'w').write(\"__version__ = '\" + '.'.join(parts) + \"'\\n\")"
	@$(MAKE) version

bump-major:
	@python3 -c "\
f = '$(VERSION_FILE)'; \
content = open(f).read(); \
v = content.strip().split('=')[1].strip().strip(\"'\"); \
parts = v.split('.'); \
parts[0] = str(int(parts[0]) + 1); parts[1] = '0'; parts[2] = '0'; \
open(f, 'w').write(\"__version__ = '\" + '.'.join(parts) + \"'\\n\")"
	@$(MAKE) version

release:
	$(eval V := $(shell $(MAKE) version))
	git add $(VERSION_FILE)
	git commit -m "Release v$(V)"
	git tag v$(V)
	git push
	git push --tags

build:
	python3 -m build

publish: build
	python3 -m twine upload dist/*

clean:
	rm -rf dist/ build/ *.egg-info
