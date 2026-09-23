# Governança

## Duas camadas de controle

Uma allowlist APM comprova a origem permitida, mas não prova sozinha que uma combinação de pasta e ref foi publicada oficialmente.

| Camada | Garantia |
|---|---|
| Policy APM | origem, dependências, profundidade, targets, MCPs e transportes permitidos |
| Checks corporativos | `repositório + pasta + SHA` corresponde a uma release oficial |

A policy de referência está em `policies/apm-policy.yml`. Para descoberta organizacional, publique-a em `nuclea/.github-private/apm-policy.yml` ou no repositório organizacional equivalente, conforme a edição do GitHub.

## Proteções de GitHub

Configure rulesets para:

- `main`: somente PR, ao menos uma revisão dos owners e checks obrigatórios;
- tags `*--v*`: criação somente pela identidade publicadora, sem update ou delete;
- `.github/**`, `tools/**`, `policies/**`, `atlas.yml` e `CODEOWNERS`: revisão obrigatória da plataforma;
- impedir force push e exigir que aprovações sejam descartadas após nova mudança relevante.

Os nomes de checks esperados são `Repository validation` e `APM package validation`.

## Policy APM

O baseline aplica:

- `enforcement: block`;
- dependências somente da origem aprovada;
- refs limitadas por tag, SHA ou faixa com teto;
- profundidade transitiva máxima 3;
- somente target Kiro no piloto;
- MCP SonarQube explícito, com `stdio` ou `http`;
- MCP transitivo não confiado automaticamente;
- `includes` explícito;
- auditoria no install e hashes de integridade.

O motor de policy deve ser tratado como uma camada de governança, não como controle do comportamento do agente. Ele não interpreta a intenção de `command`/`args` de um MCP personalizado. Por isso, o CI e a revisão continuam obrigatórios.

## Bypass

Opções locais de bypass do APM existem para depuração. Elas não são aceitas no CI protegido. Um consumidor só é considerado conforme quando o check obrigatório valida policy, lockfile e registro de releases oficiais.

## Registro do Atlas

Cada release publica `release-metadata.json` com pacote, versão, path, tag, SHA e URL. O Atlas deve ingerir apenas releases concluídas e manter também quais aplicações adotaram cada versão. Isso habilita atualização e rollback por PR.

