cmake_minimum_required(VERSION 3.5)
project(Baz VERSION 1.2.3)

add_executable(baz baz.cpp)

target_compile_options(baz PUBLIC "-F" "${FRAMEWORK_DIR}")
target_link_libraries(baz "-F ${FRAMEWORK_DIR} -framework bar")

set_target_properties(
    baz
    PROPERTIES
    INSTALL_RPATH "@executable_path"
    BUILD_WITH_INSTALL_RPATH YES
)

add_custom_command(
    TARGET baz
    PRE_BUILD
    COMMAND
        "${CMAKE_COMMAND}"
        -E
        copy_directory
        "${FRAMEWORK_DIR}/bar.framework"
        "$<TARGET_FILE_DIR:baz>/bar.framework"
)
