* static libraries: `foo`, `boo`
* shared library `bar` (depends on `foo` and `boo`) -> Framework
* application `baz` load shared library `bar` (*not working, TODO*)

Usage:
```bash
> ./jenkins.py --toolchain ios-8-2
> ls _framework/*/bar.framework
```

### Adding framework to Xcode project

* Open your Xcode project
* Add framework to the project: "File" -> "Add Files to ..." -> *choose bar.framework*
* Copy framework: "Build Phases" -> "Copy Bundle Resources" -> "+" -> *choose bar.framework* -> "Add"
* Modify application RPATH: "Build Settings" -> "Runpath Search Paths" -> "+" -> "@executable_path"

### Visibility

Export all symbols (default):

```bash
> ./jenkins.py --toolchain ios-8-2-arm64
> nm -gU _framework/ios-8-2-arm64/bar.framework/bar
... T __Z3barv
... T __Z3boov # from static library boo
... T __Z3foov # from static library foo
```

Explicit export (export only BAR_EXPORT, all other symbols are hidden):

```bash
> ./jenkins.py --toolchain ios-8-2-arm64-hid
> nm -gU _framework/ios-8-2-arm64-hid/bar.framework/bar
... T __Z3barv # only bar visible
```

*(achieved by adding `-fvisibility=hidded` and `-fvisibility-inlines-hidded` to `CMAKE_CXX_FLAGS` in toolchain)*

`foo` and `boo` exist but not visible:
```bash
> otool -vt _framework/ios-8-2-arm64-hid/bar.framework/bar | grep "^__Z3\(foo\|boo\)"
__Z3foov:
__Z3boov:
```
