from collections import OrderedDict

from http_request_codegen.codegen.rust import DEFAULT_INDENT
from http_request_codegen.modelservice.utils import migration_format as MF


DEFAULT_FIELDS = OrderedDict({
    'id': {
        'postgres': 'serial primary key',
        'rust': 'i32',
    },
    'username': {
        'postgres': 'varchar(128) not null',
        'rust': 'String',
    },
    'password': {
        'postgres': 'varchar(512) not null',
        'rust': 'String',
    },
    'email': {
        'postgres': 'varchar(256) not null',
        'rust': 'String',
    },
})

ADD_FIELDS = {
    'enabled': {
        'postgres': 'boolean default true not null',
        'struct': 'boolean',
    },
}

def create(
    no=[],
    add=[],
    table_name='users',
    indent=DEFAULT_INDENT,
    api=True,
    api_root=['src/users.rs', 'users/'],
):
    added_fields = OrderedDict({})

    create_migration_content = f'create table if not exists {table_name} (\n'
    _primary_key_ignored = False
    for field, value in DEFAULT_FIELDS.items():
        if field in no:
            continue
        pg_type = value['postgres']
        create_migration_content += f'{indent}{field} {pg_type},\n'
        added_fields[field] = value

    for field in add:
        if field in ADD_FIELDS:
            pg_type = ADD_FIELDS[field]['postgres']

            create_migration_content += (
                f'{indent}{field} {pg_type},\n'
            )
            added_fields[field] = value
    create_migration_content = create_migration_content.rstrip('\n').rstrip(',')
    create_migration_content += '\n);\n'

    remove_migration_content = f'drop table if exists {table_name};\n'

    response = {
        MF('migrations/users.up.sql'): create_migration_content,
        MF('migrations/users.down.sql'): remove_migration_content,
    }

    if api:
        user_struct = ''
        for field, value in added_fields.items():
            rust_type = value['rust']
            user_struct += f'{indent}pub {field}: {rust_type},\n'

        get_all_users_response_struct = ''
        for field in added_fields:
            get_all_users_response_struct += (
                f'                {field}: rec.{field},\n'
            )

        # data for users tests
        get_user_test_expected_response = '{'
        get_users_test_expected_response, tests_insert_user_values = ('[', '')
        insert_users_values, ids_of_users_to_remove, _n_users = ('', [], 2)
        for n in range(1, _n_users + 1):
            insert_users_values += '('
            get_users_test_expected_response += '{'
            for i, (field_name, value) in enumerate(added_fields.items()):
                if (
                    value['postgres'] == 'serial' or
                    value['postgres'].startswith('serial ')
                ):
                    pg_value = str(n)
                    json_value = f'\\"{field_name}\\":{n}'

                    insert_users_values += pg_value
                    ids_of_users_to_remove.append(pg_value)
                    get_users_test_expected_response += json_value
                    if n == 1:
                        tests_insert_user_values += pg_value
                        get_user_test_expected_response += json_value
                elif value['postgres'] == 'boolean':
                    pg_value = 'true'
                    json_value = f'\\"{field_name}\\":true'

                    insert_users_values += pg_value
                    get_users_test_expected_response += json_value
                    if n == 1:
                        tests_insert_user_values += pg_value
                        get_user_test_expected_response += json_value
                else:
                    pg_value = f"'foo_{n}'"
                    json_value = f'\\"{field_name}\\":\\"foo_{n}\\"'

                    insert_users_values += pg_value
                    get_users_test_expected_response += json_value
                    if n == 1:
                        tests_insert_user_values += pg_value
                        get_user_test_expected_response += json_value
                if i + 1 != len(added_fields):
                    insert_users_values += ', '
                    get_users_test_expected_response += ','
                    if n == 1:
                        tests_insert_user_values += ', '
                        get_user_test_expected_response += ','
            insert_users_values += ')'
            get_users_test_expected_response += '}'
            if n != _n_users:
                insert_users_values += ', '
                get_users_test_expected_response += ','
        get_users_test_expected_response += ']'
        delete_users_values = ', '.join(ids_of_users_to_remove)
        get_user_test_expected_response += '}'

        added_field_names = ', '.join(added_fields.keys())

        # data for API generation
        create_user_params_struct, insert_user_field_names = ('', [])
        create_user_binds, create_user_response = ('', '')
        n_not_null_fields = 0

        for i, (field_name, value) in enumerate(added_fields.items()):
            if 'primary key' in value['postgres']:
                continue
            if 'not null' in value['postgres']:
                n_not_null_fields += 1

                create_user_params_struct += (
                    f'    {field_name}: {value["rust"]},\n'
                )
                insert_user_field_names.append(field_name)
                create_user_binds += f'        .bind(user.{field_name})\n'
                create_user_response += (
                    f'                {field_name}: row.get({n_not_null_fields}),\n'
                )

        create_user_binds = create_user_binds.rstrip('\n')
        create_user_params_struct = create_user_params_struct.rstrip('\n')
        create_user_response = create_user_response.rstrip('\n')

        api_content = '''use actix_web::{web, HttpRequest, HttpResponse, Responder};
use serde::{Serialize, Deserialize};
use serde_json;
use sqlx::{Row, FromRow, PgPool};
use sqlx::postgres::PgRow;

#[derive(Serialize, Deserialize, FromRow)]
pub struct User {
%(user_struct)s
}

// implementation of Actix Responder for User struct so we can return User
// from action handler
impl Responder for User {
    fn respond_to(self, _req: &HttpRequest) -> HttpResponse {
        let body = serde_json::to_string(&self).unwrap();
        HttpResponse::Ok()
            .content_type("application/json")
            .body(body)
    }
}

#[derive(Deserialize)]
pub struct GetUserParams {
    id: i32,
}

#[derive(Serialize, Deserialize)]
pub struct CreateUserParams {
%(create_user_params_struct)s
}

async fn _get_all_users(pool: &PgPool) -> anyhow::Result<Vec<User>> {
    let mut users: Vec<User> = Vec::new();
    let recs = sqlx::query!("SELECT * FROM %(table_name)s")
        .fetch_all(pool)
        .await?;

    for rec in recs {
        users.push(User {
%(get_all_users_response_struct)s
        });
    }

    Ok(users)
}

async fn _get_user_by_id(id: i32, pool: &PgPool) -> anyhow::Result<User> {
    let rec = sqlx::query!(
        "SELECT * FROM %(table_name)s WHERE id = $1",
        id
    )
    .fetch_one(&*pool)
    .await?;

    Ok(User {
%(get_all_users_response_struct)s
    })
}

async fn _create_user(user: CreateUserParams, db_pool: web::Data<PgPool>) -> anyhow::Result<User> {
    let mut tx = db_pool.begin().await?;
    let user = sqlx::query("INSERT INTO %(table_name)s (%(insert_user_field_names)s) VALUES (%(insert_user_values)s) RETURNING *")
%(create_user_binds)s
        .map(|row: PgRow| {
            User {
                id: row.get(0),
%(create_user_response)s
            }
        })
        .fetch_one(&mut tx)
        .await?;

    tx.commit().await?;
    Ok(user)
}

async fn _delete_user(id: i32, pool: &PgPool) -> anyhow::Result<u64> {
    let mut tx = pool.begin().await?;
    sqlx::query("DELETE FROM users WHERE id = $1")
        .bind(id)
        .execute(&mut tx)
        .await?;

    tx.commit().await?;
    Ok(1)
}

// ------ PUBLIC ------

pub async fn get_users(db_pool: web::Data<PgPool>) -> impl Responder {
    let result = _get_all_users(&db_pool).await;
    match result {
        Ok(users) => HttpResponse::Ok().json(users),
        _ => HttpResponse::BadRequest().body("Error trying to read all users from database."),
    }
}

pub async fn get_user(params: web::Path<GetUserParams>, db_pool: web::Data<PgPool>) -> impl Responder {
    let result = _get_user_by_id(params.id, &db_pool).await;
    match result {
        Ok(user) => HttpResponse::Ok().json(user),
        _ => HttpResponse::BadRequest().body("User not found."),
    }
}

pub async fn create_user(
    user: web::Json<CreateUserParams>,
    db_pool: web::Data<PgPool>,
) -> impl Responder {
    let result = _create_user(user.into_inner(), db_pool).await;
    match result {
        Ok(user) => HttpResponse::Ok().json(user),
        _ => HttpResponse::BadRequest().body("Error trying to create a new user."),
    }
}

pub async fn delete_user(params: web::Path<GetUserParams>, db_pool: web::Data<PgPool>) -> impl Responder {
    let result = _delete_user(params.id, &db_pool).await;
    match result {
        Ok(n_rows) => {
            if n_rows > 0 {
                HttpResponse::Ok()
                    .body(format!("Successfully deleted {} user(s)", n_rows))
            } else {
                HttpResponse::BadRequest().body("User not found")
            }
        }
        _ => HttpResponse::BadRequest().body("User not found"),
    }
}

pub fn init(cfg: &mut web::ServiceConfig) {
    cfg.service(
        web::scope("/users")
            .service(
                web::resource("")
                    .route(web::get().to(get_users))
                    .route(web::post().to(create_user)),
            )
            .service(
                web::resource("/{id}")
                    .route(web::get().to(get_user))
                    .route(web::delete().to(delete_user))
            ),
    );
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::env;

    use actix_web::{web, test, App, Error};

    use rstest::*;

    #[fixture]
    async fn pool() -> PgPool {
        PgPool::connect(&env::var("DATABASE_URL").expect("'DATABASE_URL' not set!"))
            .await
            .expect("Failed to create database connections pool.")
    }

    #[rstest]
    async fn test_get_users(#[future] pool: PgPool) -> Result<(), Error> {
        let pg_pool = pool.await;
        let app = App::new().configure(init).app_data(web::Data::new(pg_pool.clone()));
        let mut app = test::init_service(app).await;

        // GET /users
        sqlx::query!("DELETE FROM %(table_name)s WHERE id IN (%(delete_users_values)s);")
            .execute(&pg_pool)
            .await
            .expect("Delete users from 'user' table.");

        sqlx::query!("INSERT INTO %(table_name)s (%(added_field_names)s) VALUES %(insert_users_values)s;")
            .execute(&pg_pool)
            .await
            .expect("Insert users into 'user' table.");

        let req = test::TestRequest::get().uri("/users").to_request();
        let result = test::read_response(&mut app, req).await;
        assert_eq!(result, web::Bytes::from_static(b"%(get_users_test_expected_response)s"));

        sqlx::query!("DELETE FROM %(table_name)s WHERE id IN (%(delete_users_values)s);")
            .execute(&pg_pool)
            .await
            .expect("Delete users from '%(table_name)s' table.");

        // GET /user/{id}
        sqlx::query!("INSERT INTO %(table_name)s (%(added_field_names)s) VALUES (%(tests_insert_user_values)s);")
            .execute(&pg_pool)
            .await
            .expect("Insert user into '%(table_name)s' table.");

        let req = test::TestRequest::get().uri("/users/1").to_request();
        let result = test::read_response(&mut app, req).await;
        assert_eq!(result, web::Bytes::from_static(b"%(get_user_test_expected_response)s"));

        sqlx::query!("DELETE FROM %(table_name)s WHERE id = 1;")
            .execute(&pg_pool)
            .await
            .expect("Delete user from '%(table_name)s' table.");

        // POST /users
        let user : CreateUserParams = CreateUserParams {
            username: "foo_5".to_string(),
            email: "foo_5".to_string(),
            password: "foo_5".to_string(),
        };
        let req = test::TestRequest::post()
            .uri("/users")
            .set_json(&user)
            .to_request();
        let result = test::read_response(&mut app, req).await;
        assert_eq!(
            result,
            web::Bytes::from_static(
                b"{\\"id\\":1,\\"username\\":\\"foo_5\\",\\"password\\":\\"foo_5\\",\\"email\\":\\"foo_5\\"}"
            ),
        );

        let req = test::TestRequest::get().uri("/users").to_request();
        let result = test::read_response(&mut app, req).await;
        assert_eq!(
            result,
            web::Bytes::from(
                "[{\\"id\\":1,\\"username\\":\\"foo_5\\",\\"password\\":\\"foo_5\\",\\"email\\":\\"foo_5\\"}]"
            ),
        );

        sqlx::query!("DELETE FROM users WHERE id = 1;")
            .execute(&pg_pool)
            .await
            .expect("Delete user from '%(table_name)s' table.");

        // DELETE /users/{id}
        sqlx::query!("INSERT INTO users (%(added_field_names)s) VALUES (%(tests_insert_user_values)s);")
            .execute(&pg_pool)
            .await
            .expect("Insert user into '%(table_name)s' table.");
        let req = test::TestRequest::delete().uri("/users/1").to_request();
        let result = test::read_response(&mut app, req).await;
        assert_eq!(result, web::Bytes::from_static(b"Successfully deleted 1 user(s)"));

        let req = test::TestRequest::get().uri("/users").to_request();
        let result = test::read_response(&mut app, req).await;
        assert_eq!(result, web::Bytes::from_static(b"[]"));

        Ok(())
    }
}
''' %   {
            'api_root': api_root[1],
            'user_struct': user_struct,
            'table_name': table_name,
            'get_all_users_response_struct': get_all_users_response_struct,
            'added_field_names': added_field_names,
            'insert_users_values': insert_users_values,
            'delete_users_values': delete_users_values,
            'get_users_test_expected_response': get_users_test_expected_response,
            'tests_insert_user_values': tests_insert_user_values,
            'get_user_test_expected_response': get_user_test_expected_response,
            'create_user_params_struct': create_user_params_struct,
            'insert_user_field_names': ', '.join(insert_user_field_names),
            'insert_user_values': ', '.join([
                f'${n}' for n in range(1, len(insert_user_field_names) + 1)
            ]),
            'create_user_binds': create_user_binds,
            'create_user_response': create_user_response,
        }

        response[api_root[0]] = api_content

        response['Cargo.toml'] = '''[package]
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
'''

    return response
