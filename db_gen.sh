#!/bin/bash

DB_FILE="flask_app/db.sqlite"
if [ -f "$DB_FILE" ]; then
  echo "Data Base exists at: $DB_FILE"
else
  python -c "from flask_app import db, create_app; db.create_all(app=create_app())"
  echo "Data Base was successfully generated!"
fi
