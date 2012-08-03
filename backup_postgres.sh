#!/bin/bash

# http://www.commandprompt.com/blogs/joshua_drake/2010/07/a_better_backup_with_postgresql_using_pg_dump/
# Puedes ver la fecha de la fecha  en la cabecera de los .sqlc:
# pg_restore -l backupu.sqlc | head -n 15

# Echo: "Ejecutar este script como usuario con permisos (postgres)"

BKPDIR=postgres-backup-${DATE}
RSTFILE=restore.README
USER=postgres
GLOBALS=globals.sql

DATE=`date +%Y%m%d-%Hh%M`
mkdir postgres-backup-${DATE}
cd postgres-backup-${DATE}
pg_dumpall -g -U $USER --file=$GLOBALS;

echo "#--- Date: $DATE" >> $RSTFILE
echo "#---restore globals: " >> $RSTFILE
echo "psql -U postgres < $GLOBALS : " >> $RSTFILE

psql -AtU $USER -c "SELECT datname FROM pg_database \
                          WHERE NOT datistemplate"| \
while read f;
   do
   output=$f.sqlc
   echo "Backup of $f to $output"
   pg_dump -U$USER --format=c --file=${output} $f;
   echo "#---restore $f" >> $RSTFILE
   echo "pg_restore -U postgres --dbname=$f $output" >> $RSTFILE
   echo "" >> $RSTFILE
done;
cd ..
