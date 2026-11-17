#!/bin/sh
# Build buku + metadata SEO (canonical, og:url, sitemap, robots).
set -e
cd "$(dirname "$0")"
mdbook build
python3 generate-seo.py https://rust-book-id.pages.dev/
