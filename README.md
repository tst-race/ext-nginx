# NGINX for RACE

This repo provides scripts to custom-build the
[NGINX server](https://www.nginx.com/) with the
[Stream Real-Time Messaging Protocol (RTMP) module](https://www.nginx.com/products/nginx/modules/rtmp-media-streaming/)
for RACE.

## License

The NGINX server and RTMP module are licensed under the 2-Clause BSD license.

Only the build scripts in this repo are licensed under Apache 2.0.

## Dependencies

NGINX has no dependencies on any custom-built libraries.

## How To Build

The [ext-builder](https://github.com/tst-race/ext-builder) image is used to
build NGINX.

```
git clone https://github.com/tst-race/ext-builder.git
git clone https://github.com/tst-race/ext-nginx.git
./ext-builder/build.py \
    --target linux-x86_64 \
    ./ext-nginx
```

## Platforms

NGINX is built for the following platforms:

* `linux-x86_64`
* `linux-arm64-v8a`

## How It Is Used

NGINX is used by the <TO-BE-NAMED> channel.
