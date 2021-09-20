use actix_web::{web, HttpRequest, HttpResponse, Responder};
use serde::{Deserialize, Serialize};
use serde_json;
use sqlx::{FromRow, PgPool};


#[derive(Serialize, Deserialize, FromRow)]
pub struct User {
    id: i32,
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
    let recs = sqlx::query!("SELECT * FROM users")
        .fetch_all(pool)
        .await?;

    for rec in recs {
        users.push(User {
            id: rec.id,
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

    use actix_web::{web, http, test, App, Error};

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
        sqlx::query!("DELETE FROM users WHERE id IN (3001, 3002);")
            .execute(&pg_pool)
            .await
            .expect("Remove users from 'user' table.");

        sqlx::query!("INSERT INTO users (id) VALUES (3001), (3002);")
            .execute(&pg_pool)
            .await
            .expect("Insert users into 'user' table.");

        // get users using API
        let req = test::TestRequest::get().uri("/users").to_request();
        let result = test::read_response(&mut app, req).await;
        assert_eq!(result, web::Bytes::from_static(b"[{\"id\":3001},{\"id\":3002}]"));

        sqlx::query!("DELETE FROM users WHERE id IN (3001, 3002);")
            .execute(&pg_pool)
            .await
            .expect("Remove users from 'user' table.");

        Ok(())
    }
}
