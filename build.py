#!/usr/bin/env python3

#
# Copyright 2023 Two Six Technologies
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

"""
Script to build nginx for RACE
"""

import logging
import os
import race_ext_builder as builder


def get_cli_arguments():
    """Parse command-line arguments to the script"""
    parser = builder.get_arg_parser(
        "nginx",
        "1.14.0",
        1,
        __file__,
        [builder.TARGET_LINUX_x86_64, builder.TARGET_LINUX_arm64_v8a],
    )
    return builder.normalize_args(parser.parse_args())


if __name__ == "__main__":
    args = get_cli_arguments()
    builder.make_dirs(args)
    builder.setup_logger(args)

    builder.install_packages(
        args,
        [
            ("libpcre3-dev", "2:8.39*", True),
            ("libssl-dev", "1.1.1*", True),
            ("zlib1g-dev", "1:1.2.11*", True),
        ],
    )

    logging.root.info("Copying nginx source")
    builder.copy(
        args, os.path.join(args.code_dir, f"nginx-{args.version}"), args.source_dir
    )
    builder.copy(
        args, os.path.join(args.code_dir, "nginx-rtmp-module"), args.source_dir
    )

    source_dir = os.path.join(args.source_dir, f"nginx-{args.version}")
    env = builder.create_standard_envvars(args)

    logging.root.info("Configuring build")
    builder.execute(
        args,
        [
            "./configure",
            "--prefix=/",
            "--with-http_ssl_module",
            f"--add-module={args.source_dir}/nginx-rtmp-module",
        ],
        cwd=source_dir,
        env=env,
    )

    logging.root.info("Manually removing -Werror")
    builder.find_and_replace(
        args,
        root_dir=source_dir,
        file_pattern="*Makefile*",
        regex="\-Werror",
        replacement="",
    )

    logging.root.info("Building")
    builder.execute(
        args,
        [
            "make",
            "-j",
            args.num_threads,
        ],
        cwd=source_dir,
        env=env,
    )
    builder.execute(
        args,
        [
            "make",
            f"DESTDIR={args.install_dir}",
            "install",
        ],
        cwd=source_dir,
        env=env,
    )

    builder.create_package(args)
