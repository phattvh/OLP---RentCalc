#!/usr/bin/env bash
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Phat Tran Vu Hoa - RentCalc
set -e
mkdir -p app/static/css
npx -y tailwindcss@3 -c ./ui/tailwind.config.js -i ./ui/input.css -o ./app/static/css/app.css --minify
echo "Biên dịch thành công: app/static/css/app.css"