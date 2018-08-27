cmake_minimum_required(VERSION 3.5)
project(Bar VERSION 1.2.3)

find_package(Boo CONFIG REQUIRED)
find_package(Foo CONFIG REQUIRED)

add_library(bar SHARED bar.cpp bar.hpp)
target_link_libraries(bar PUBLIC Foo::foo Boo::boo)

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
generate_export_header(bar)

target_include_directories(
    bar PUBLIC "$<BUILD_INTERFACE:${CMAKE_CURRENT_BINARY_DIR}>"
)

set_target_properties(
    bar
    PROPERTIES
    CXX_VISIBILITY_PRESET hidden
    VISIBILITY_INLINES_HIDDEN ON
    XCODE_ATTRIBUTE_GCC_INLINES_ARE_PRIVATE_EXTERN YES
    XCODE_ATTRIBUTE_GCC_SYMBOLS_PRIVATE_EXTERN YES
)

set(config_install_dir "lib/cmake/${PROJECT_NAME}")
set(include_install_dir "include")

set(generated_dir "${CMAKE_CURRENT_BINARY_DIR}/generated")

set(version_config "${generated_dir}/${PROJECT_NAME}ConfigVersion.cmake")
set(project_config "${generated_dir}/${PROJECT_NAME}Config.cmake")
set(targets_export_name "${PROJECT_NAME}Targets")
set(namespace "${PROJECT_NAME}::")

include(CMakePackageConfigHelpers)

write_basic_package_version_file(
    "${version_config}" COMPATIBILITY SameMajorVersion
)

configure_file("cmake/Config.cmake.in" "${project_config}" @ONLY)

install(
    TARGETS bar
    EXPORT "${targets_export_name}"
    LIBRARY DESTINATION "lib"
    ARCHIVE DESTINATION "lib"
    RUNTIME DESTINATION "bin"
    INCLUDES DESTINATION "${include_install_dir}"
)

install(FILES "bar.hpp" DESTINATION "include/bar")

install(
    FILES "${project_config}" "${version_config}"
    DESTINATION "${config_install_dir}"
)

install(
    FILES "${CMAKE_CURRENT_BINARY_DIR}/bar_export.h"
    DESTINATION "${include_install_dir}"
)

install(
    EXPORT "${targets_export_name}"
    NAMESPACE "${namespace}"
    DESTINATION "${config_install_dir}"
)
