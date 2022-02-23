

{
    email ${LETSENCRYPT_EMAIL}
    acme_ca https://acme-staging-v02.api.letsencrypt.org/directory
    local_certs
}

${ORIGIN_DOMAIN} {
    reverse_proxy frontend:3000
}

${API_DOMAIN}  {
    reverse_proxy backend:8001
}
