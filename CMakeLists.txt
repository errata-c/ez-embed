cmake_minimum_required(VERSION 3.16)

project(EZ_EMBED
LANGUAGES CXX)

include(FetchContent)

FetchContent_Declare(
	ez-cmake
	GIT_REPOSITORY "https://github.com/errata-c/ez-cmake.git"
	GIT_TAG "main"
)
FetchContent_MakeAvailable(ez-cmake)


option(EZ_EMBED_BUILD_TESTS "Build the test for ez-embed")

# Find and use python for the embedding, this prevents any host -> target issues

if(EZ_EMBED_BUILD_TESTS)
	add_subdirectory("test")
endif()