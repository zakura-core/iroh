//! Authentication regressions for the retained published Dalek versions.
#![cfg(feature = "key")]

use data_encoding::HEXLOWER;
use iroh_base::{PublicKey, SecretKey, Signature};

#[test]
fn rfc8032_signature_and_mutations() {
    let seed: [u8; 32] = HEXLOWER
        .decode(b"9d61b19deffd5a60ba844af492ec2cc44449c5697b326919703bac031cae7f60")
        .unwrap()
        .try_into()
        .unwrap();
    let secret = SecretKey::from_bytes(&seed);
    assert_eq!(
        secret.public().to_string(),
        "d75a980182b10ab7d54bfed3c964073a0ee172f3daa62325af021a68f707511a"
    );
    let signature = secret.sign(b"");
    assert_eq!(
        HEXLOWER.encode(&signature.to_bytes()),
        "e5564300c360ac729086e2cc806e828a84877f1eb8e5d974d873e065224901555fb8821590a33bacc61e39701cf9b46bd25bf5f0595bbe24655141438e7a100b"
    );
    assert!(secret.public().verify(b"", &signature).is_ok());
    assert!(secret.public().verify(b"changed", &signature).is_err());
    assert!(
        SecretKey::from_bytes(&[7; 32])
            .public()
            .verify(b"", &signature)
            .is_err()
    );
    for index in 0..64 {
        let mut bytes = signature.to_bytes();
        bytes[index] ^= 0x80;
        assert!(
            secret
                .public()
                .verify(b"", &Signature::from_bytes(&bytes))
                .is_err()
        );
    }
}

#[test]
fn strict_verification_rejects_weak_keys_and_noncanonical_scalars() {
    let mut identity = [0; 32];
    identity[0] = 1;
    let public = PublicKey::from_bytes(&identity).unwrap();
    let mut forged = [0; 64];
    forged[..32].copy_from_slice(&identity);
    assert!(
        public
            .verify(b"unauthenticated", &Signature::from_bytes(&forged))
            .is_err()
    );
    let secret = SecretKey::from_bytes(&[42; 32]);
    let mut signature = secret.sign(b"message").to_bytes();
    signature[32..].fill(0xff);
    assert!(
        secret
            .public()
            .verify(b"message", &Signature::from_bytes(&signature))
            .is_err()
    );
    assert!(PublicKey::try_from(&[0; 31][..]).is_err());
    assert!(Signature::try_from(&[0; 63][..]).is_err());
}
