#!/usr/bin/bash
# backup script for sqlite
# creates a dump file from the target database in the
# specified directory

# sqlite_dump.sh /var/sqlite/kpop_monday.db /opt/samba/db-bak/
# backup created will be [example] : /opt/samba/db-bak/kpop_monday.20260812.dump.gz
# to restore backup: zcat kpop_monday.20260812.dump.gz | sqlite3 /var/sqlite/kpop_monday_new.db

# Example dump command: sqlite3 ex1 .dump | gzip -c >ex1.dump.gz
source=$1
target_dir=$2

target=$target_dir$(basename $source .db)_`date +%Y%m%d_%H%M`.dump.gz
echo "source = $source"
echo "target_dir = $target_dir"
echo "target = $target"
echo "beginning backup..."
echo

# sqlite3 source .dump | gzip -c >$target
/usr/bin/sqlite3 $source .dump | gzip -c >$target
