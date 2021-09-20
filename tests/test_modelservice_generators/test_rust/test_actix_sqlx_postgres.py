import os
import re
import shutil
import subprocess
import tempfile

import pytest

from http_request_codegen.modelservice.users.rust.actix4_sqlx_postgres import (
    create,
)


@pytest.mark.parametrize(
    ('no', 'add', 'table_name', 'expected_files_contents'),
    (
        pytest.param(
            [],
            [],
            None,
            {
                re.compile(r'^migrations/\d+_users\.up\.sql$'): (
                    '''create table if not exists users (
    id serial,
    username varchar(128) not null,
    password varchar(512) not null,
    email varchar(256) not null
);
'''
                ),
                re.compile(r'^migrations/\d+_users\.down\.sql$'): (
                    'drop table if exists users;\n'
                ),
            },
            id='default',
        ),
        pytest.param(
            ['username', 'email'],
            ['enabled'],
            'foo_table_name',
            {
                re.compile(r'^migrations/\d+_users\.up\.sql$'): (
                    '''create table if not exists foo_table_name (
    id serial,
    password varchar(512) not null,
    enabled boolean default true not null
);
'''
                ),
                re.compile(r'^migrations/\d+_users\.down\.sql$'): (
                    'drop table if exists foo_table_name;\n'
                ),
            },
            id='custom',
        ),
    ),
)
def test_user_rust_actix_sqlx_postgres(
    assert_files_contents,
    no,
    add,
    table_name,
    expected_files_contents,
):
    kwargs = {
        'no': no,
        'add': add,
    }
    if table_name is not None:
        kwargs['table_name'] = table_name

    return assert_files_contents(create(**kwargs), expected_files_contents)


@pytest.mark.skipif(
    not shutil.which('cargo'),
    reason='Cargo must be installed to execute the integration test.',
)
@pytest.mark.skipif(
    not shutil.which('sqlx'),
    reason='sqlx-cli must be installed to execute the integration test.',
)
@pytest.mark.skipif(
    'rust' not in os.environ.get('INTEGRATION_TESTS', ''),
    reason=(
        'The word "rust" must be included in "INTEGRATION_TESTS" environment'
        ' variable value to execute rust integration tests.'
    ),
)
def test_user_rust_actix_sqlx_postgres_integration(
    temporal_postgres_database,
    temporal_cwd,
    temporal_env_var,
):
    """Integration test to generate an API URL service with ACTIX, sqlx and
    PostgreSQL.
    """

    with tempfile.TemporaryDirectory() as tmpdirname, \
            temporal_postgres_database('rust_actix_sqlx_postgres') \
            as (db_name, db_conn), \
            temporal_cwd(tmpdirname):
        with open(os.path.join(tmpdirname, 'Cargo.toml'), 'w') as f:
            f.write('''[package]
name = "my-package"
version = "0.1.0"
edition = "2018"

[dependencies]
actix-web = "4.0.0-beta.9"
sqlx = { version = "0.5.7", features = ["macros", "postgres", "runtime-async-std-native-tls"] }
serde = "1.0.117"
serde_json = "1.0.59"
anyhow = "1.0.44"

[dev-dependencies]
rstest = "0.11.0"
async-std = {version = "1.9.0", features = ["attributes"]}
''')
        os.mkdir(os.path.join(tmpdirname, 'src'))

        with open(os.path.join(tmpdirname, 'src', 'main.rs'), 'w') as f:
            f.write('''mod users;

use std::env;

use actix_web::{middleware, web, App, HttpResponse, HttpServer};
use sqlx;

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    // configure host from environment variable
    let database_url = env::var("DATABASE_URL").expect("DATABASE_URL must be set!");
    let pool = sqlx::postgres::PgPoolOptions::new()
        .connect(&database_url)
        .await
        .expect("Failed to create database connections pool.");

    // start HTTP server
    HttpServer::new(move || {
        App::new()
            .wrap(middleware::Logger::default())
            .configure(users::init)
            .app_data(web::Data::new(pool.clone()))
            .default_service(web::route().to(HttpResponse::NotFound))
    })
    .bind(("127.0.0.1", 15876))?
    .run()
    .await
    .ok();

    Ok(())
}
''')
        files_contents = create()

        for filename, content in files_contents.items():
            os.makedirs(
                os.path.join(tmpdirname, os.path.dirname(filename)),
                exist_ok=True,
            )
            with open(os.path.join(tmpdirname, filename), 'w') as f:
                f.write(content)
                print(filename)
                print(content)
                print('-------------------------------')

        with temporal_env_var(
            'DATABASE_URL',
            f'postgres://postgres:postgres@localhost/{db_name}',
        ):
            exitcode = subprocess.call(['sqlx', 'migrate', 'run'])
            assert exitcode == 0

            exitcode = subprocess.call(['cargo', 'build'])
            assert exitcode == 0

            exitcode = subprocess.call(['cargo', 'test'])
            assert exitcode == 0
