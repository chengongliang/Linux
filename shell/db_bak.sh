#!/bin/bash
mysql_home="/usr/local/mysql/"
binlog_home="/usr/local/mysql/binlog"
binlog_index="${binlog_home}/binlog.index"
syn_home="/data/mysql_db_back/"
databases=(edu_auth smartmatch)

last_log_file=`awk 'NR==1{print $1}' $syn_home'syn.pos'`
last_log_position=`awk 'NR==1{print $2}' $syn_home'syn.pos'`
new_log_file=`tail -1 $binlog_index `
new_log_position=`ls -l $new_log_file | awk '{print $5}'`

rm -rf ${syn_home}*.sql
while true
do
   if [ $new_log_file == $last_log_file ]
   then
      for db in ${databases[@]}
      do
         $mysql_home"bin/mysqlbinlog" --database=$db  --set-charset=utf8  --start-position=$last_log_position  --stop-position=$new_log_position $last_log_file >> $syn_home$db".sql"
      done
      echo "$new_log_file	$new_log_position" > $syn_home"syn.pos"
      break
   else
      for db in ${databases[@]}
      do
         $mysql_home"bin/mysqlbinlog" --database=$db  --set-charset=utf8  --start-position=$last_log_position  $last_log_file >> $syn_home$db".sql"
      done
      curr=` grep -n $last_log_file $binlog_index `
      curr_nr=${curr%:*}
      next_nr=` expr $curr_nr + 1 `
      last_log_file=`awk 'NR=='$next_nr'{print $1}' $binlog_index `
      last_log_position=4 
   fi
done
