# Checklist de revisão

Use apenas as categorias pertinentes ao diff.

## Estado e ciclo de vida

- Backend remoto, locking, criptografia e separação por ambiente.
- `moved`, `import`, `prevent_destroy` e mudanças de endereço que evitam recriação acidental.
- Substituições, deleções e mudanças de retenção visíveis no plano.

## Segurança

- IAM com privilégio mínimo, sem curingas desnecessários.
- Tráfego, portas, CIDRs, exposição pública, TLS e criptografia em repouso.
- Segredos fora do código e outputs sensíveis marcados adequadamente.
- Logs e dados que possam vazar informação protegida.

## Confiabilidade

- Multi-AZ/região quando exigido, health checks, timeouts, retry e limites.
- Backup, restore, retenção e proteção contra exclusão.
- Dependências implícitas, condições de corrida e ordem de substituição.

## Manutenção e custo

- Providers e módulos com constraints compatíveis e lockfile.
- Variáveis tipadas, validação de entrada e defaults seguros.
- Tags obrigatórias, naming, ownership e impactos de custo material.

