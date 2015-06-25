cmake_minimum_required(VERSION 3.0)
project(Baz VERSION 1.2.3)

add_executable(baz baz.cpp)

target_compile_options(baz PUBLIC "-F" "${FRAMEWORK_DIR}")
target_link_libraries(baz "-F ${FRAMEWORK_DIR} -framework bar")

add_custom_command(
    TARGET baz
    PRE_BUILD
    COMMAND
        "${CMAKE_COMMAND}"
        -E
        copy_directory
        "${FRAMEWORK_DIR}/bar.framework"
        "$<TARGET_FILE_DIR:baz>/../Framework/bar.framework"
)
