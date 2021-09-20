mod users;

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
