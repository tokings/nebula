# Copyright (c) 2020 vesoft inc. All rights reserved.
#
# This source code is licensed under Apache 2.0 License.

nebula_add_library(
    time_obj OBJECT
    detail/TscHelper.cpp
    Duration.cpp
    WallClock.cpp
)

nebula_add_library(
    time_utils_obj OBJECT
    TimeUtils.cpp
    TimezoneInfo.cpp
    TimeConversion.cpp
)

nebula_add_subdirectory(test)
