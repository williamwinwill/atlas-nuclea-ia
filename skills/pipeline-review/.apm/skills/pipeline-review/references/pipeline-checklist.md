# Checklist de pipeline

## Gatilhos e confiança

- `pull_request_target` executando código ou checkout de fork não confiável.
- Inputs, nomes de branch, artefatos e outputs usados em shell sem delimitação segura.
- Aprovação de environment antes de produção.

## Permissões e secrets

- `permissions` no menor escopo por job.
- OIDC com audience e subject limitados; evite credenciais estáticas long-lived.
- Secrets indisponíveis a código de PR não confiável.
- Mascaramento não substitui evitar impressão de dados sensíveis.

## Supply chain e reprodutibilidade

- Actions de terceiros fixadas por SHA completo e atualizadas por processo revisado.
- Toolchains, imagens e dependências versionadas.
- Build gera uma vez; promoção reutiliza o mesmo artefato e sua proveniência.
- Release usa o SHA exato do evento e nunca uma branch que possa ter avançado.

## Confiabilidade

- `concurrency` e cancelamento coerentes com deploys.
- Timeouts, retry limitado e rollback observável.
- Cache com chave segura e sem dados executáveis cruzando fronteiras de confiança.

