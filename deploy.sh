#!/bin/sh

# Deployment script
# Execute as normal user, it will ask for permissions as needed
# Configure the following variables

DIR=`dirname $0`

# Skip steps if already done, set to "yes"
##### CONFIGURE THESE #####
SKIP_PACKAGE_INSTALLATION="no"
SKIP_NPM_INSTALL="no"
SKIP_NPM_BUILD="no"
SKIP_PGRES_CREATE_DB_AND_USER="no"
SKIP_PGRES_DISABLE_FORCED_SSL="no"
SKIP_SETUP_VENV="no"
SKIP_UPDATE_HOSTS="no"

# Virtual environment folder
VENV="$DIR/test_venv"
PIP="$VENV/bin/pip"
PYTHON="$VENV/bin/python"

# 100% secure
# CAREFUL: will destroy previous db and user with this name
# Don't change if you dont know what you are doing
DB_NAME="asoures2"
DB_PASS="password"

if [ "x$SKIP_PACKAGE_INSTALLATION" != "xyes" ] ; then
    echo "Installing packages..."
    sudo apt-get update -y
    sudo apt-get install postgresql postgresql-contrib postgis python3 python3-pip apache2 apache2-dev libapache2-mod-wsgi nodejs npm -y
fi

if [ "x$SKIP_NPM_INSTALL" != "xyes" ]; then
    echo "Installing node_modules"
    cd $DIR/project/client && npm install
fi

if [ "x$SKIP_NPM_BUILD" != "xyes" ]; then
    echo "Building front-end"
    cd $DIR/project/client && npm run build
fi

if [ "x$SKIP_PGRES_CREATE_DB_AND_USER" != "xyes" ]; then
    echo "Creating database"
    sudo -u postgres dropdb $DB_NAME --if-exists
    sudo -u postgres dropuser $DB_NAME --if-exists
    sudo userdel $DB_NAME

    echo "Enter password '$DB_PASS' below:"
    echo $DB_PASS >> $DIR/.tmp
    echo $DB_PASS >> $DIR/.tmp
    sudo -u postgres createuser --superuser -P $DB_NAME
    sudo -u postgres createdb $DB_NAME
    sudo useradd -M -s /usr/sbin/nologin $DB_NAME
    sudo passwd $DB_NAME < $DIR/.tmp
    rm $DIR/.tmp
fi

if [ "x$SKIP_PGRES_DISABLE_FORCED_SSL" != "xyes" ]; then
    echo "Disabling postgresql forced SSL option"

    postgresql_conf="/etc/postgresql/10/main/postgresql.conf"
    if [ -f $postgresql_conf ]; then
        echo "Config file: $postgresql_conf"
        sudo cp "$postgresql_conf" "${postgresql_conf}.bak"
        cat $postgresql_conf | sed "s,ssl\s*=\s*on,ssl = off,g" > $DIR/.conf
        sudo cp $DIR/.conf $postgresql_conf
        rm $DIR/.conf
        echo "Updated successfully"
    else
        echo "WARNING: postgresql.conf not found, manually edit and set option 'ssl = off'"
    fi
fi

[ -e $DIR/asoures.egg-info ] && echo "Removing old asoures.egg-info" && rm -rf $DIR/asoures.egg-info
rm -rf 
if [ "x$SKIP_SETUP_VENV" != "xyes" ]; then
    echo "Installing virtualenv"
    pip3 install --user virtualenv

    echo "Setting up python virtual environment in $VENV"
    [ -e "$VENV" ] && rm -rf "$VENV" # trust me
    mkdir -p "$VENV"
    ~/.local/bin/virtualenv "$VENV"

    echo "Installing django and other dependencies"
    cd $DIR && $PIP install -e .[dev]
fi

echo -n "Updating environment file "
echo "DATABASE_URL=postgis://$DB_NAME:$DB_PASS@localhost/$DB_NAME" > $DIR/.env
if [ "x$DEBUG" != "xyes" ]; then
    echo "(release)"
    echo "DEBUG=false" >> $DIR/.env
    echo "SECRET_KEY=asdfhqweughkjhbkjgiuqwerhfbwergtqwiureyt" >> $DIR/.env
    echo "ALLOWED_HOSTS=*" >> $DIR/.env
else
    echo "(debug)"
    echo "DEBUG=true" >> $DIR/.env
fi

echo "Running migrations"
cd $DIR && $PYTHON $DIR/manage.py migrate

if [ "x$SKIP_UPDATE_HOSTS" != "xyes" ]; then
    echo "Updating hosts"
    sudo -- sh -c "echo '\n\n127.0.0.1 asoures.gr' >> /etc/hosts"
fi

echo ""
echo ""
echo "-----------------"
echo "Done. Next steps:"
echo "-----------------"
echo ""
echo "0) Activate environment (REQUIRED)"
echo "    source $VENV/bin/activate && cd $DIR"
echo ""
echo "1) Run unit tests:"
echo "    python manage.py test"
echo ""
echo "2) Run integration tests:"
echo "    python manage.py integration_test"
echo ""
echo "3) Start development server:"
echo "    export REACT_APP_API_URL='http://localhost:8000/observatory/api/'"
echo "    python manage.py runserver 8000            (Django)"
echo "    cd project/client && npm run start         (ReactJS only)"
echo ""
echo "4) Start apache server:"
echo "    python manage.py runserver 8443"
echo ""
echo ""
