cmake_minimum_required(VERSION 3.5)
project(bar VERSION 1.2.3)

find_package(boo CONFIG REQUIRED)
find_package(foo CONFIG REQUIRED)

set(
    export_header
    "${CMAKE_CURRENT_BINARY_DIR}/${PROJECT_NAME}/BAR_EXPORT.h"
)

set(ios_framework FALSE)
if(IOS AND BUILD_SHARED_LIBS)
  set(ios_framework TRUE)
endif()

set(public_headers bar.hpp ${export_header})
add_library(bar bar.cpp ${public_headers})
target_link_libraries(bar PUBLIC foo::foo boo::boo)

if(ios_framework)
  list(LENGTH CMAKE_CONFIGURATION_TYPES len)
  if(NOT len EQUAL "1")
    message(FATAL_ERROR "Not supported")
  endif()

  set(
      bar_framework_location
      "${CMAKE_CURRENT_BINARY_DIR}/${CMAKE_CONFIGURATION_TYPES}-iphoneos/bar.framework"
  )

  set_source_files_properties(
      "${bar_framework_location}"
      PROPERTIES
      GENERATED YES
      MACOSX_PACKAGE_LOCATION Frameworks
  )

  set_target_properties(
      bar
      PROPERTIES
      FRAMEWORK TRUE
      PUBLIC_HEADER "${public_headers}"
      MACOSX_FRAMEWORK_INFO_PLIST "${CMAKE_CURRENT_LIST_DIR}/Info.plist"
      INSTALL_NAME_DIR "@rpath//"
      BUILD_WITH_INSTALL_NAME_DIR YES
  )
endif()

add_executable(roo roo.cpp ${bar_framework_location})
target_link_libraries(roo PUBLIC bar)

if(ios_framework)
  set_target_properties(
      roo
      PROPERTIES
      XCODE_ATTRIBUTE_LD_RUNPATH_SEARCH_PATHS "@executable_path/Frameworks"
  )
endif()

if(EXPORT_FILE)
  if(APPLE)
    target_link_libraries(
        bar
        PRIVATE
        "-Wl,-exported_symbols_list"
        "${CMAKE_CURRENT_LIST_DIR}/libbar.exports"
    )
  endif()
endif()

include(GenerateExportHeader)
generate_export_header(bar EXPORT_FILE_NAME ${export_header})

target_include_directories(
    bar
    PUBLIC
    "$<BUILD_INTERFACE:${CMAKE_CURRENT_BINARY_DIR}>"
    "$<BUILD_INTERFACE:${CMAKE_CURRENT_LIST_DIR}/..>"
)

set_target_properties(
    bar
    PROPERTIES
    CXX_VISIBILITY_PRESET hidden
    VISIBILITY_INLINES_HIDDEN ON
    XCODE_ATTRIBUTE_GCC_INLINES_ARE_PRIVATE_EXTERN YES
    XCODE_ATTRIBUTE_GCC_SYMBOLS_PRIVATE_EXTERN YES
)


# * CMAKE_INSTALL_LIBDIR
# * CMAKE_INSTALL_BINDIR
# * CMAKE_INSTALL_INCLUDEDIR
include(GNUInstallDirs)

set(config_install_dir "${CMAKE_INSTALL_LIBDIR}/cmake/${PROJECT_NAME}")
set(generated_dir "${CMAKE_CURRENT_BINARY_DIR}/generated")
set(version_config "${generated_dir}/${PROJECT_NAME}ConfigVersion.cmake")
set(project_config "${generated_dir}/${PROJECT_NAME}Config.cmake")
set(TARGETS_EXPORT_NAME "${PROJECT_NAME}Targets")
set(namespace "${PROJECT_NAME}::")

include(CMakePackageConfigHelpers)

write_basic_package_version_file(
    "${version_config}" COMPATIBILITY SameMajorVersion
)

# Use:
# * TARGETS_EXPORT_NAME
# * PROJECT_NAME
configure_package_config_file(
    "Config.cmake.in"
    "${project_config}"
    INSTALL_DESTINATION "${config_install_dir}"
)

install(
    TARGETS bar
    EXPORT "${TARGETS_EXPORT_NAME}"
    LIBRARY DESTINATION "${CMAKE_INSTALL_LIBDIR}"
    ARCHIVE DESTINATION "${CMAKE_INSTALL_LIBDIR}"
    RUNTIME DESTINATION "${CMAKE_INSTALL_BINDIR}"
    FRAMEWORK DESTINATION "."
    INCLUDES DESTINATION "${CMAKE_INSTALL_INCLUDEDIR}"
)

if(ios_framework)
  # Headers are part of the installed framework
else()
  install(
      FILES ${public_headers}
      DESTINATION "${CMAKE_INSTALL_INCLUDEDIR}/${PROJECT_NAME}"
  )
endif()

install(
    FILES "${project_config}" "${version_config}"
    DESTINATION "${config_install_dir}"
)

install(
    EXPORT "${TARGETS_EXPORT_NAME}"
    NAMESPACE "${namespace}"
    DESTINATION "${config_install_dir}"
)
