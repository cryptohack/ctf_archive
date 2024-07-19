use std::collections::HashSet;

use blake2::Digest;

use ark_bn254::{Bn254, Fr};
use ark_ff::{PrimeField, UniformRand};
use ark_groth16::{Groth16, Proof, ProvingKey, VerifyingKey};
use ark_r1cs_std::alloc::AllocVar;
use ark_r1cs_std::{eq::EqGadget, fields::fp::FpVar, R1CSVar};
use ark_relations::r1cs::{ConstraintSynthesizer, ConstraintSystemRef, SynthesisError};
use ark_serialize::{CanonicalDeserialize, CanonicalSerialize};
use ark_snark::SNARK;
use arkworks_native_gadgets::poseidon::{
    sbox::PoseidonSbox, FieldHasher, Poseidon, PoseidonParameters,
};
use arkworks_r1cs_gadgets::poseidon::{FieldHasherGadget, PoseidonGadget};
use arkworks_utils::{
    bytes_matrix_to_f, bytes_vec_to_f, poseidon_params::setup_poseidon_params, Curve,
};
use serde::Deserialize;
use serde::Serialize;

fn poseidon() -> Poseidon<Fr> {
    let data = setup_poseidon_params(Curve::Bn254, 5, 3).unwrap();

    let params = PoseidonParameters {
        mds_matrix: bytes_matrix_to_f(&data.mds),
        round_keys: bytes_vec_to_f(&data.rounds),
        full_rounds: data.full_rounds,
        partial_rounds: data.partial_rounds,
        sbox: PoseidonSbox(data.exp),
        width: data.width,
    };

    Poseidon::<Fr>::new(params)
}

#[derive(Serialize, Deserialize, Clone, Debug)]
pub struct Ticket {
    pub proof: String,
}

#[derive(Copy, Clone)]
pub struct TicketMaestroCircuit<F: PrimeField> {
    pub secret: Option<F>,
}

impl ConstraintSynthesizer<Fr> for TicketMaestroCircuit<Fr> {
    fn generate_constraints(self, cs: ConstraintSystemRef<Fr>) -> Result<(), SynthesisError> {
        // create the poseidon gadget
        let poseidon = PoseidonGadget::from_native(&mut cs.clone(), poseidon())?;

        // witness the secret
        let secret = FpVar::new_witness(cs.clone(), || Ok(self.secret.unwrap()))?;
        let hash = poseidon.hash(&[secret])?;

        // input the hash and enforce equality
        FpVar::new_input(cs.clone(), || hash.value())?.enforce_equal(&hash)?;
        Ok(())
    }
}

pub struct TicketMaestro {
    secret: Fr,
    digest: Fr,
    spent: HashSet<[u8; 32]>, // spent ticket ids
    pk: ProvingKey<Bn254>,    // proving key
    vk: VerifyingKey<Bn254>,  // verifying key
}

impl TicketMaestro {
    pub fn digest(&self) -> String {
        let mut bs = vec![];
        self.digest.serialize(&mut bs).unwrap();
        hex::encode(bs)
    }

    pub fn ticket_verify(&self, ticket: Ticket) -> Result<[u8; 32], anyhow::Error> {
        // deserialize the ticket
        let proof = hex::decode(ticket.proof)?;
        let proof = Proof::<Bn254>::deserialize(&proof[..])?;

        // verify the ticket
        if !Groth16::<Bn254>::verify(&self.vk, &[self.digest], &proof)? {
            return Err(anyhow::Error::msg("Invalid ticket"));
        }

        // compute the ticket id
        let mut ser = vec![];
        self.digest.serialize(&mut ser).unwrap();
        proof.serialize(&mut ser).unwrap();
        Ok(blake2::Blake2b::digest(&ser).into())
    }

    pub fn issue(&self) -> Result<Ticket, SynthesisError> {
        // create fresh ticket
        let circuit = TicketMaestroCircuit {
            secret: Some(self.secret),
        };
        let proof = Groth16::<Bn254>::prove(&self.pk, circuit, &mut rand::thread_rng())?;

        // serialize the proof
        let mut bs = vec![];
        proof.serialize(&mut bs).unwrap();
        Ok(Ticket {
            proof: hex::encode(bs),
        })
    }

    pub fn redeem(&mut self, ticket: Ticket) -> bool {
        match self.ticket_verify(ticket) {
            Ok(id) => self.spent.insert(id),
            Err(_) => false,
        }
    }

    pub fn setup() -> Self {
        let mut rng = rand::thread_rng();
        let circuit = TicketMaestroCircuit { secret: None };
        let (pk, vk) =
            Groth16::<Bn254>::circuit_specific_setup(circuit, &mut rand::thread_rng()).unwrap();
        let secret = Fr::rand(&mut rng);
        let digest = poseidon().hash(&[secret]).unwrap();
        Self {
            pk,
            vk,
            secret,
            digest,
            spent: HashSet::new(),
        }
    }

    pub fn pk(&self) -> String {
        let mut bs = vec![];
        self.pk.serialize(&mut bs).unwrap();
        hex::encode(bs)
    }

    pub fn vk(&self) -> String {
        let mut bs = vec![];
        self.vk.serialize(&mut bs).unwrap();
        hex::encode(bs)
    }
}

#[derive(Serialize, Deserialize, Debug)]
pub enum Request {
    Redeem(Ticket),
    Balance,
    BuyFlag,
    BuyTicket,
    ProvingKey,
    VerifyingKey,
    Digest,
}

#[derive(Serialize, Deserialize, Debug)]
pub enum Response {
    Hello(String),
    Ticket(Ticket),
    ProvingKey(String),
    VerifyingKey(String),
    GoodTicket,
    BadTicket,
    LolTooPoor,
    Balance(i64),
    Flag(String),
    Digest(String),
}

#[test]
fn test() {
    let mut maestro = TicketMaestro::setup();
    let ticket = maestro.issue().unwrap();
    assert!(maestro.redeem(ticket.clone()));
    assert!(!maestro.redeem(ticket.clone()));
}
