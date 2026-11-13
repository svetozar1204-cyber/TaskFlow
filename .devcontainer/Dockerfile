
FROM mcr.microsoft.com/devcontainers/python:1-3.12-bookworm

RUN set -eux; \
    for file in /etc/apt/sources.list /etc/apt/sources.list.d/*; do \
        if [ -f "$file" ] && grep -q 'dl.yarnpkg.com' "$file"; then \
            rm -f "$file"; \
        fi; \
    done
