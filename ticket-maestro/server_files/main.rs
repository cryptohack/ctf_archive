use serde_json::from_str;
use std::env;

mod maestro;

use maestro::{Request, Response, TicketMaestro};

const BALANCE: i64 = 10;
const COST_OF_FLAG: i64 = 2 * BALANCE;
const COST_OF_TICKET: i64 = 2;
const VALUE_OF_TICKET: i64 = 1;

macro_rules! respond {
    ($resp:expr) => {
        println!("{}", serde_json::to_string(&$resp).unwrap());
    };
}

fn main() {
    let mut balance: i64 = BALANCE;
    let mut maestro = TicketMaestro::setup();

    // greeting
    respond!(Response::Hello("Welcome to ticket maestro!".to_string()));

    // request/response loop
    loop {
        let mut line = String::new();
        std::io::stdin().read_line(&mut line).unwrap();

        // parse
        let req: Request = match from_str(&line) {
            Ok(req) => req,
            Err(_) => {
                break;
            }
        };

        // process
        match req {
            Request::BuyTicket => {
                if balance > 0 {
                    let ticket = maestro.issue().unwrap();
                    balance -= COST_OF_TICKET;
                    respond!(Response::Ticket(ticket));
                } else {
                    respond!(Response::LolTooPoor);
                }
            }
            Request::ProvingKey => {
                respond!(Response::ProvingKey(maestro.pk()));
            }
            Request::VerifyingKey => {
                respond!(Response::VerifyingKey(maestro.vk()));
            }
            Request::Redeem(ticket) => {
                if maestro.redeem(ticket) {
                    balance += VALUE_OF_TICKET;
                    respond!(Response::GoodTicket);
                } else {
                    respond!(Response::BadTicket);
                }
            }
            Request::BuyFlag => {
                if balance >= COST_OF_FLAG {
                    balance -= COST_OF_FLAG;
                    respond!(Response::Flag(env::var("FLAG").unwrap()));
                } else {
                    respond!(Response::LolTooPoor);
                }
            }
            Request::Balance => {
                respond!(Response::Balance(balance));
            }
            Request::Digest => {
                respond!(Response::Digest(maestro.digest()));
            }
        }
    }
}
