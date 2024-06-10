DATABASE="mizdooni"

CONDITION=$(mysql -uroot -p$MYSQL_ROOT_PASSWORD -e "SHOW DATABASES LIKE '$DATABASE';" 2>&1)

if [[ $CONDITION == *"$DATABASE"* ]]; then
  echo "Database exists."
  exit 0
else
  echo "Database does not exist."
  exit 1
fi