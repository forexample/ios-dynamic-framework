cmake_minimum_required(VERSION 3.5)
project(baz VERSION 1.2.3)

set(ios_dynamic_framework FALSE)
if(IOS AND BUILD_SHARED_LIBS)
  # TODO: This is not accurate
  set(ios_dynamic_framework TRUE)
endif()

if(ios_dynamic_framework)
  set(framework_dir "${CMAKE_PREFIX_PATH}")
  set(bar_framework_location ${framework_dir}/bar.framework)

  set_source_files_properties(
      "${bar_framework_location}"
      PROPERTIES
      GENERATED YES
      MACOSX_PACKAGE_LOCATION Frameworks
  )
else()
  set(bar_framework_location "")
endif()

add_executable(baz baz.cpp ${bar_framework_location})

if(ios_dynamic_framework)
  # {
  # Workaround for the error:
  #
  #   Attempting to use @rpath without CMAKE_SHARED_LIBRARY_RUNTIME_C_FLAG being
  #   set.  This could be because you are using a Mac OS X version less than 10.5
  #   or because CMake's platform configuration is corrupt.
  target_compile_options(baz PUBLIC "-F" "${framework_dir}")
  target_link_libraries(baz PUBLIC "-F ${framework_dir} -framework bar")
  # }

  set_target_properties(
      baz
      PROPERTIES
      XCODE_ATTRIBUTE_LD_RUNPATH_SEARCH_PATHS "@executable_path/Frameworks"
  )
else()
  find_package(bar CONFIG REQUIRED)
  target_link_libraries(baz PUBLIC bar::bar)
endif()
