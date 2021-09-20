from collections import OrderedDict

from http_request_codegen.codegen.rust import DEFAULT_INDENT
from http_request_codegen.modelservice.utils import migration_format as MF


DEFAULT_FIELDS = OrderedDict({
    'id': {
        'postgres': 'serial',
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
    # create migration files
    added_fields = OrderedDict({})

    create_migration_content = f'create table if not exists {table_name} (\n'
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
        get_users_test_expected_response = '['
        create_users_values, ids_of_users_to_remove, _n_users = ('', [], 2)
        for n in range(1, _n_users + 1):
            create_users_values += '('
            get_users_test_expected_response += '{'
            for i, (field_name, value) in enumerate(added_fields.items()):
                if value['postgres'] == 'serial':
                    create_users_values += str(n)
                    ids_of_users_to_remove.append(str(n))
                    get_users_test_expected_response += f'\\"{field_name}\\":{n}'
                elif value['postgres'] == 'boolean':
                    create_users_values += 'true'
                    get_users_test_expected_response += f'\\"{field_name}\\":true'
                else:
                    create_users_values += f"'foo_{n}'"
                    get_users_test_expected_response += (
                        f'\\"{field_name}\\":\\"foo_{n}\\"'
                    )
                if i + 1 != len(added_fields):
                    create_users_values += ', '
                    get_users_test_expected_response += ','
            create_users_values += ')'
            get_users_test_expected_response += '}'
            if n != _n_users:
                create_users_values += ', '
                get_users_test_expected_response += ','
        get_users_test_expected_response += ']'
        remove_users_values = ', '.join(ids_of_users_to_remove)

        api_content = '''use actix_web::{web, HttpRequest, HttpResponse, Responder};
use serde::{Deserialize, Serialize};
use serde_json;
use sqlx::{FromRow, PgPool};


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

pub async fn get_users(db_pool: web::Data<PgPool>) -> impl Responder {
    let result = _get_all_users(&db_pool).await;
    match result {
        Ok(users) => HttpResponse::Ok().json(users),
        _ => HttpResponse::BadRequest().body("Error trying to read all users from database"),
    }
}

pub fn init(cfg: &mut web::ServiceConfig) {
    cfg.service(
        web::scope("/users")
            .service(
                web::resource("")
                    .route(web::get().to(get_users)),
            )
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

        // create users
        sqlx::query!("DELETE FROM %(table_name)s WHERE id IN (%(remove_users_values)s);")
            .execute(&pg_pool)
            .await
            .expect("Remove users from 'user' table.");

        sqlx::query!("INSERT INTO %(table_name)s (%(added_field_names)s) VALUES %(create_users_values)s;")
            .execute(&pg_pool)
            .await
            .expect("Insert users into 'user' table.");

        // get users using API
        let req = test::TestRequest::get().uri("/users").to_request();
        let result = test::read_response(&mut app, req).await;
        assert_eq!(result, web::Bytes::from_static(b"%(get_users_test_expected_response)s"));

        sqlx::query!("DELETE FROM %(table_name)s WHERE id IN (%(remove_users_values)s);")
            .execute(&pg_pool)
            .await
            .expect("Remove users from 'users' table.");

        Ok(())
    }
}
''' %   {
            'api_root': api_root[1],
            'user_struct': user_struct,
            'table_name': table_name,
            'get_all_users_response_struct': get_all_users_response_struct,
            'added_field_names': ', '.join(added_fields.keys()),
            'create_users_values': create_users_values,
            'remove_users_values': remove_users_values,
            'get_users_test_expected_response': get_users_test_expected_response,
        }

        response[api_root[0]] = api_content

    return response

"""
use crate::todo::{Todo, TodoRequest};
use actix_web::{delete, get, post, put, web, HttpResponse, Responder};
use sqlx::SqlitePool;

#[get("/todos")]
async fn find_all(db_pool: web::Data<SqlitePool>) -> impl Responder {
    let result = Todo::find_all(db_pool.get_ref()).await;
    match result {
        Ok(todos) => HttpResponse::Ok().json(todos),
        _ => HttpResponse::BadRequest()
            .body("Error trying to read all todos from database"),
    }
}

#[get("/todo/{id}")]
async fn find(id: web::Path<i32>, db_pool: web::Data<SqlitePool>) -> impl Responder {
    let result = Todo::find_by_id(id.into_inner(), db_pool.get_ref()).await;
    match result {
        Ok(todo) => HttpResponse::Ok().json(todo),
        _ => HttpResponse::BadRequest().body("Todo not found"),
    }
}

#[post("/todo")]
async fn create(
    todo: web::Json<TodoRequest>,
    db_pool: web::Data<SqlitePool>,
) -> impl Responder {
    let result = Todo::create(todo.into_inner(), db_pool.get_ref()).await;
    match result {
        Ok(todo) => HttpResponse::Ok().json(todo),
        _ => HttpResponse::BadRequest().body("Error trying to create new todo"),
    }
}

#[put("/todo/{id}")]
async fn update(
    id: web::Path<i32>,
    todo: web::Json<TodoRequest>,
    db_pool: web::Data<SqlitePool>,
) -> impl Responder {
    let result =
        Todo::update(id.into_inner(), todo.into_inner(), db_pool.get_ref()).await;
    match result {
        Ok(todo) => HttpResponse::Ok().json(todo),
        _ => HttpResponse::BadRequest().body("Todo not found"),
    }
}

#[delete("/todo/{id}")]
async fn delete(id: web::Path<i32>, db_pool: web::Data<SqlitePool>) -> impl Responder {
    let result = Todo::delete(id.into_inner(), db_pool.get_ref()).await;
    match result {
        Ok(rows) => {
            if rows > 0 {
                HttpResponse::Ok()
                    .body(format!("Successfully deleted {} record(s)", rows))
            } else {
                HttpResponse::BadRequest().body("Todo not found")
            }
        }
        _ => HttpResponse::BadRequest().body("Todo not found"),
    }
}

// function that will be called on new Application to configure routes for this module
pub fn init(cfg: &mut web::ServiceConfig) {
    cfg.service(find_all);
    cfg.service(find);
    cfg.service(create);
    cfg.service(update);
    cfg.service(delete);
}
"""
