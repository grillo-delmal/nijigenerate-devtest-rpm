#!/usr/bin/bash

sed -i "s/%define nijigenerate_ver .*/%define nijigenerate_ver $1/" nijigenerate-devtest.spec
sed -i "s/%define nijigenerate_dist .*/%define nijigenerate_dist $2/" nijigenerate-devtest.spec
sed -i "s/%define nijigenerate_short .*/%define nijigenerate_short $3/" nijigenerate-devtest.spec
