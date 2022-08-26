{
    email ${letsencrypt_email}
    acme_ca https://acme-staging-v02.api.letsencrypt.org/directory
    local_certs
}

${frontend_domain} {
    reverse_proxy ${app_name}-frontend:3000
}

${backend_domain}  {
    reverse_proxy ${app_name}-backend:8001
}
