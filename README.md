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
