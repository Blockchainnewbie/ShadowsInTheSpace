{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = with pkgs; [
    go
    python311
    python311Packages.pip
    python311Packages.alembic
    python311Packages.flask
    python311Packages.flask-limiter
    python311Packages.flask-cors
    python311Packages.flask-jwt-extended
    python311Packages.flask-migrate
    python311Packages.flask-sqlalchemy
    python311Packages.python-dotenv
    python311Packages.sqlalchemy
    python311Packages.werkzeug # Added explicitly
    python311Packages.argon2-cffi
    python311Packages.gunicorn
    python311Packages.pymysql
    nodejs_20
    nodePackages.nodemon
  ];
}
