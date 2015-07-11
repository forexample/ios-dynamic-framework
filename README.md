* Static libraries: `foo`, `boo`
* Shared library `bar` (depends on `foo` and `boo`) -> Framework
* Application `baz` load shared library `bar` (*not working for iOS, TODO*)
* Native Xcode iOS project `DynamicFrameworkUsageExample` use `bar.framework`

Usage:
```bash
> ./jenkins.py --toolchain ios-8-2
> ls _framework/*/bar.framework
```

### Adding framework to Xcode project

* Open your Xcode project
* Add framework to the project: "File" -> "Add Files to ..." -> *choose bar.framework*
* Copy framework: "Build Phases" -> "New Copy Files Phase" -> Set "Destination" to "Frameworks" -> "+" -> *choose bar.framework* -> "Add"

### Visibility

#### Default

Export all symbols (default):

```bash
> ./jenkins.py --toolchain ios-8-2-arm64
> nm -gU _framework/ios-8-2-arm64/bar.framework/bar
... T __Z3barv
... T __Z3boov # from static library boo
... T __Z3foov # from static library foo
```

#### File with exports

Exported symbols can be listed explicitly in file using `-exported_symbols_list` option:

```bash
> cat Bar/libbar.exports
__Z3barv
> ./jenkins.py --toolchain ios-8-2 --export-file
> nm -gU _framework/ios-8-2/bar.framework/bar
... T __Z3barv
```

#### Toolchain

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

### App Store Submittion

Exclude simulator architectures (i386, x86_64) from framework by adding extra option `--device` (this will add `--framework-device` to `build.py` script) and open Xcode project:

```bash
> ./jenkins.py --device --toolchain ios-8-2
> open DynamicFrameworkUsageExample/DynamicFrameworkUsageExample.xcodeproj
```

Build, archive and submit application.

### More

* [Hunter (package manager)](https://github.com/ruslo/hunter)
* [Polly (toolchains)](https://github.com/ruslo/polly)
