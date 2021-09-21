use actix_web::{web, HttpRequest, HttpResponse, Responder};
use serde::{Deserialize, Serialize};
use serde_json;
use sqlx::{Row, FromRow, PgPool};
use sqlx::postgres::PgRow;


#[derive(Serialize, Deserialize, FromRow)]
pub struct User {
    pub id: i32,
    pub username: String,
    pub password: String,
    pub email: String,
}

impl Responder for User {
    fn respond_to(self, _req: &HttpRequest) -> HttpResponse {
        let body = serde_json::to_string(&self).unwrap();
        HttpResponse::Ok()
            .content_type("application/json")
            .body(body)
    }
}

#[derive(Deserialize)]
struct GetUserParams {
    id: i32,
}

#[derive(Serialize, Deserialize)]
struct CreateUserParams {
    username: String,
    password: String,
    email: String,
}

async fn _get_all_users(pool: &PgPool) -> anyhow::Result<Vec<User>> {
    let mut users: Vec<User> = Vec::new();
    let recs = sqlx::query!("SELECT * FROM users")
        .fetch_all(pool)
        .await?;

    for rec in recs {
        users.push(User {
                id: rec.id,
                username: rec.username,
                password: rec.password,
                email: rec.email,

        });
    }

    Ok(users)
}

async fn _get_user_by_id(id: i32, pool: &PgPool) -> anyhow::Result<User> {
    let rec = sqlx::query!(
        "SELECT * FROM users WHERE id = $1",
        id
    )
    .fetch_one(&*pool)
    .await?;

    Ok(User {
        id: rec.id,
        username: rec.username,
        password: rec.password,
        email: rec.email,
    })
}

async fn _create_user(user: CreateUserParams, db_pool: web::Data<PgPool>) -> anyhow::Result<User> {
    let mut tx = db_pool.begin().await?;
    let user = sqlx::query("INSERT INTO users (username, password, email) VALUES ($1, $2, $3) RETURNING *")
        .bind(user.username)
        .bind(user.password)
        .bind(user.email)
        .map(|row: PgRow| {
            User {
                id: row.get(0),
                username: row.get(1),
                password: row.get(2),
                email: row.get(3),
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

// -----------------------------------------------------------------

pub async fn get_users(db_pool: web::Data<PgPool>) -> impl Responder {
    let result = _get_all_users(&db_pool).await;
    match result {
        Ok(users) => HttpResponse::Ok().json(users),
        _ => HttpResponse::BadRequest().body("Error trying to read all users from database"),
    }
}

async fn get_user(params: web::Path<GetUserParams>, db_pool: web::Data<PgPool>) -> impl Responder {
    let result = _get_user_by_id(params.id, &db_pool).await;
    match result {
        Ok(user) => HttpResponse::Ok().json(user),
        _ => HttpResponse::BadRequest().body("User not found"),
    }
}

async fn create_user(
    user: web::Json<CreateUserParams>,
    db_pool: web::Data<PgPool>,
) -> impl Responder {
    let result = _create_user(user.into_inner(), db_pool).await;
    match result {
        Ok(user) => HttpResponse::Ok().json(user),
        _ => HttpResponse::BadRequest().body("Error trying to create a new user."),
    }
}

async fn delete_user(params: web::Path<GetUserParams>, db_pool: web::Data<PgPool>) -> impl Responder {
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
    async fn test_users(#[future] pool: PgPool) -> Result<(), Error> {
        let pg_pool = pool.await;
        let app = App::new().configure(init).app_data(web::Data::new(pg_pool.clone()));
        let mut app = test::init_service(app).await;

        // GET /users
        // get users using API
        sqlx::query!("DELETE FROM users WHERE id IN (1, 2);")
            .execute(&pg_pool)
            .await
            .expect("Delete users from 'user' table.");

        sqlx::query!("INSERT INTO users (id, username, password, email) VALUES (1, 'foo_1', 'foo_1', 'foo_1'), (2, 'foo_2', 'foo_2', 'foo_2');")
            .execute(&pg_pool)
            .await
            .expect("Insert users into 'user' table.");

        let req = test::TestRequest::get().uri("/users").to_request();
        let result = test::read_response(&mut app, req).await;
        assert_eq!(result, web::Bytes::from_static(b"[{\"id\":1,\"username\":\"foo_1\",\"password\":\"foo_1\",\"email\":\"foo_1\"},{\"id\":2,\"username\":\"foo_2\",\"password\":\"foo_2\",\"email\":\"foo_2\"}]"));

        sqlx::query!("DELETE FROM users WHERE id IN (1, 2);")
            .execute(&pg_pool)
            .await
            .expect("Delete users from 'users' table.");

        // GET /user
        // get user using API
        sqlx::query!("INSERT INTO users (id, username, password, email) VALUES (1, 'foo_1', 'foo_1', 'foo_1');")
            .execute(&pg_pool)
            .await
            .expect("Insert user into 'users' table.");
        let req = test::TestRequest::get().uri("/users/1").to_request();
        let result = test::read_response(&mut app, req).await;
        assert_eq!(result, web::Bytes::from_static(b"{\"id\":1,\"username\":\"foo_1\",\"password\":\"foo_1\",\"email\":\"foo_1\"}"));

        sqlx::query!("DELETE FROM users WHERE id IN (1, 2);")
            .execute(&pg_pool)
            .await
            .expect("Delete user from 'users' table.");

        // POST /user
        // create user using API
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
                b"{\"id\":1,\"username\":\"foo_5\",\"password\":\"foo_5\",\"email\":\"foo_5\"}"
            ),
        );

        let req = test::TestRequest::get().uri("/users").to_request();
        let result = test::read_response(&mut app, req).await;
        assert_eq!(
            result,
            web::Bytes::from(
                "[{\"id\":1,\"username\":\"foo_5\",\"password\":\"foo_5\",\"email\":\"foo_5\"}]"
            ),
        );

        sqlx::query!("DELETE FROM users WHERE id = 1;")
            .execute(&pg_pool)
            .await
            .expect("Delete user from 'users' table.");

        // DELETE /user
        sqlx::query!("INSERT INTO users (id, username, password, email) VALUES (1, 'foo_1', 'foo_1', 'foo_1');")
            .execute(&pg_pool)
            .await
            .expect("Insert user into 'users' table.");
        let req = test::TestRequest::delete().uri("/users/1").to_request();
        let result = test::read_response(&mut app, req).await;
        assert_eq!(result, web::Bytes::from_static(b"Successfully deleted 1 user(s)"));

        let req = test::TestRequest::get().uri("/users").to_request();
        let result = test::read_response(&mut app, req).await;
        assert_eq!(result, web::Bytes::from_static(b"[]"));

        sqlx::query!("DELETE FROM users WHERE id = 1;")
            .execute(&pg_pool)
            .await
            .expect("Delete user from 'users' table.");

        Ok(())
    }
}
