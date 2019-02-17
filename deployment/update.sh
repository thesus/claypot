#!/bin/bash
QUIET=0
VERSION=master
while [[ $# -gt 0 ]]; do
    arg1="$1"
    case "$arg1" in
        -h|--help)
            echo Updates Claypot.
            echo
            echo "Usage:"
            echo "$(basename "$0") [--version VERSION]"
            echo
            echo "-h --help     Show this help message"
            echo "--version     Update to specified Docker image tag"
            echo "-q --quiet    Show no output on success"
            exit 0
            ;;
        --version)
            VERSION=$2
            shift
            shift
            ;;
        -q|--quit)
            QUIET=1
            shift
            ;;
        *)
            echo "Unknown parameter $arg1"
            exit 1
            ;;
    esac
done

cd "$(dirname $0)" || exit $?

if [ ! -f docker-compose.yml ]; then
    echo "docker-compose.yml not found in $(pwd)"
    exit 1
fi

if [ ! -f .env ]; then
    echo ".env not found in $(pwd)"
    exit 1
fi

export CLAYPOT_VERSION="$VERSION"

if [ "$QUIET" = "0" ]; then
    echo "Updating to Claypot version $CLAYPOT_VERSION..."
fi

docker-compose pull || exit $?
docker-compose up -d || exit $?
docker-compose run --rm claypot python manage.py migrate --no-input || exit $?

if [ "$QUIET" = "0" ]; then
    echo "Finished updating to Claypot version $CLAYPOT_VERSION."
fi
