* static libraries: `foo`, `boo`
* shared library `bar` (depends on `foo` and `boo`) -> Framework
* application `baz` load shared library `bar`

Usage:
```bash
> ./jenkins.py --toolchain ios-8-2
```
